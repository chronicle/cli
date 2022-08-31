# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Create a feed using source type, log type and other input parameters."""

import dataclasses
import json
import os.path
from typing import Any, Dict

import click
from click._compat import WIN

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import file_utility
from common import options
from common.constants import key_constants
from common.constants import status
from feeds import feed_schema_utility
from feeds import feed_templates
from feeds import feed_utility
from feeds.constants import schema

CREATE_BACKUP_FILE = os.path.join(chronicle_auth.CHRONICLE_CLI_ROOT_DIR,
                                  "feeds", "create_backup.json")


@click.command(help="Create a feed")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def create(credential_file: str, verbose: bool, region: str, url: str) -> None:
  """Create feed.

  Args:
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    url (str): Base URL to be used for API calls.

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  url = feed_utility.lower_or_none(url)
  feed_schema = feed_schema_utility.FeedSchema(credential_file, region, url)
  retry = False
  properties_map = feed_schema.get_log_source_map()
  flattened_response = {}

  # Checking condition that backup file exists for any pending feed.
  if os.path.exists(CREATE_BACKUP_FILE) and (
      os.path.getsize(CREATE_BACKUP_FILE)) != 0:
    with open(CREATE_BACKUP_FILE, "r") as file:
      backup_data = json.load(file)
    retry_template_str = feed_templates.retry_template.substitute(
        source_type=backup_data[schema.KEY_DISPLAY_SOURCE_TYPE],
        log_type=backup_data[schema.KEY_DISPLAY_LOG_TYPE])
    retry = click.confirm(f"{retry_template_str}", default=None)
    if not retry:
      file_utility.remove_file(CREATE_BACKUP_FILE)

  # Here we set the backup data to the process for taking existing values.
  if retry:
    selected_source_type = backup_data[schema.KEY_FEED_SOURCE_TYPE]
    selected_log_type = backup_data[key_constants.KEY_LOG_TYPE]
    flattened_response = backup_data
  else:
    properties = log_source_types_from_user(properties_map)
    selected_source_type = properties.selected_source_type
    selected_log_type = properties.selected_log_type

  feed_detailed_schema = feed_schema.get_detailed_schema(
      selected_source_type, selected_log_type)

  if feed_detailed_schema.error:
    click.echo(feed_detailed_schema.error)
    return
  click.echo(f"{feed_templates.input_parameters_template.template}")

  # "flattened_response" is received along with the response body,
  # for storing the existing data into the backup file.
  request_body, flattened_response = feed_schema.prepare_request_body(
      feed_detailed_schema.log_type_schema, selected_source_type,
      selected_log_type, flattened_response)

  full_url = feed_utility.get_feed_url(region, url)
  method = "POST"
  api_response = feed_schema.client.request(method, full_url, request_body)
  response = api_utility.check_content_type(api_response.text)

  if api_response.status_code != status.STATUS_OK:
    click.echo(
        "\nError occurred while creating feed.\nResponse Code: "
        f"{api_response.status_code}.\nError: "
        f"{response[key_constants.KEY_ERROR][key_constants.KEY_MESSAGE]}")

    # "flattened_response" is updated with the Source Type and Log Type
    # and written to the backup file in case of failure to create feed.
    feed_utility.write_backup(
        CREATE_BACKUP_FILE, flattened_response,
        properties_map[selected_source_type].get(schema.KEY_DISPLAY_NAME),
        selected_source_type,
        feed_detailed_schema.log_type_schema[schema.KEY_DISPLAY_NAME],
        selected_log_type)
    return

  click.echo("\nFeed created successfully with Feed ID: "
             f"{response[schema.KEY_NAME][6:]}")
  file_utility.remove_file(CREATE_BACKUP_FILE)
  if verbose:
    api_utility.print_request_details(full_url, method, request_body, response)


@dataclasses.dataclass
class Properties:
  """Properties dataclass."""
  selected_log_type: str
  selected_source_type: str


def log_source_types_from_user(properties_map: Dict[str, Any]) -> Any:
  """Remove backup file if exists and fetch data for API request body.

  Args:
    properties_map (Dict): Mapping dictionary of source and related log types.

  Returns:
    properties (dataclass): Contains selected log type and source type.
  """
  click.echo(f"{feed_templates.properties_template.template}")
  click.echo("\nList of Source types:")

  for index, each_source in enumerate(list(properties_map.values())):
    click.echo(f"{index + 1}. {each_source.get(schema.KEY_DISPLAY_NAME)}")

  choice = click.prompt(
      "\n[Source type] Enter your choice",
      type=click.types.IntRange(1, len(properties_map)))

  selected_source_type = list(properties_map.keys())[choice - 1]
  click.echo("\nYou have selected " + click.style(
      f"{properties_map[selected_source_type].get(schema.KEY_DISPLAY_NAME)}",
      bold=True))

  log_types = properties_map[selected_source_type].get(schema.KEY_LOG_TYPES)
  out_str = f"{feed_templates.log_type_template.template}"
  if WIN:
    out_str = f"{feed_templates.log_type_template_win.template}"
  for index, log_type in enumerate(log_types):
    out_str = out_str + f"{index + 1}. {log_type[1]} ({log_type[0]})\n"

  choice = 0
  while choice == 0:
    click.echo_via_pager(out_str)
    choice = click.prompt(
        "\n[Log type] Enter your choice",
        default=0,
        show_default=False,
        type=click.types.IntRange(0, len(log_types)))

  selected_log_type = log_types[choice - 1][0]
  click.echo("\nYou have selected " +
             click.style(f"{log_types[choice - 1][1]}", bold=True))
  return Properties(selected_log_type, selected_source_type)
