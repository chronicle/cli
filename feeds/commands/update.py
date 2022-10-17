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
"""Update feed."""

import dataclasses
import json
import os
from typing import Any, Dict, Optional

import click

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

UPDATE_BACKUP_FILE = os.path.join(chronicle_auth.CHRONICLE_CLI_ROOT_DIR,
                                  "feeds", "update_backup.json")


@click.command(help="Update feed details using Feed ID")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def update(credential_file: str, verbose: bool, region: str, url: str) -> None:
  """Update feed.

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

  feed_id = click.prompt("Enter Feed ID", default="", show_default=False)
  if not feed_id:
    click.echo("Feed ID not provided. Please enter Feed ID.")
    return
  # Checking condition that backup file exists for any pending feed.
  if os.path.exists(
      UPDATE_BACKUP_FILE) and os.path.getsize(UPDATE_BACKUP_FILE) != 0:
    with open(UPDATE_BACKUP_FILE, "r") as file:
      backup_data = json.load(file)

    retry_template_str = feed_templates.retry_template.substitute(
        source_type=backup_data[schema.KEY_DISPLAY_SOURCE_TYPE],
        log_type=backup_data[schema.KEY_DISPLAY_LOG_TYPE])

    backup_id = backup_data.get(schema.KEY_NAME)[6:]

    # Checking that ID provided by user matches with the backup ID.
    # If ID not matches, then the retry will remain default as "n".
    if backup_id == feed_id:
      retry = click.confirm(f"{retry_template_str}", default=None)
    if not retry:
      file_utility.remove_file(UPDATE_BACKUP_FILE)

  # Here we set the backup data to the process for taking existing values.
  if retry:
    selected_source_type = backup_data[schema.KEY_FEED_SOURCE_TYPE]
    selected_log_type = backup_data[key_constants.KEY_LOG_TYPE]
    feed_display_name = backup_data.get(schema.KEY_DISPLAY_NAME)
    flattened_response = backup_data
  else:
    request_data = fetch_feed_request_data(feed_schema, region, url, feed_id)
    if request_data.error:
      return
    selected_log_type = request_data.selected_log_type
    selected_source_type = request_data.selected_source_type
    feed_display_name = request_data.feed_display_name
    flattened_response = request_data.flattened_response

  detail_schema = feed_schema.get_detailed_schema(selected_source_type,
                                                  selected_log_type)
  if detail_schema.error:
    click.echo(detail_schema.error)
    return

  click.echo("Press Enter if you don't want to update.")

  feed_display_name = click.prompt(
      f"\nEnter feed display name[{feed_display_name}]",
      show_default=False,
      default=feed_display_name)
  # "flattened_response" is received along with the response body,
  # for storing the existing data into the backup file.
  updated_body, flattened_response = feed_schema.prepare_request_body(
      detail_schema.log_type_schema, selected_source_type, selected_log_type,
      flattened_response, feed_display_name)

  full_url = f"{feed_utility.get_feed_url(region, url)}/{feed_id}"
  method = "PATCH"
  update_feeds_response = feed_schema.client.request(method, full_url,
                                                     updated_body)

  update_response = api_utility.check_content_type(update_feeds_response.text)

  if update_feeds_response.status_code != status.STATUS_OK:
    error_msg = update_response[key_constants.KEY_ERROR][
        key_constants.KEY_MESSAGE]
    click.echo("\nError occurred while updating feed. Response code: "
               f"{update_feeds_response.status_code}.\nError: "
               f"{error_msg}")

    # "flattened_response" is updated with the Source Type and Log Type
    # and written to the backup file in case of failure to update feed.
    feed_utility.write_backup(
        UPDATE_BACKUP_FILE, flattened_response,
        detail_schema.display_source_type, selected_source_type,
        detail_schema.log_type_schema[schema.KEY_DISPLAY_NAME],
        selected_log_type, feed_display_name)
    return

  click.echo("\nFeed updated successfully with Feed ID: "
             f"{update_response[schema.KEY_NAME][6:]}")
  file_utility.remove_file(UPDATE_BACKUP_FILE)

  if verbose:
    api_utility.print_request_details(full_url, method, updated_body,
                                      update_response)


@dataclasses.dataclass
class RequestData:
  """Dataclass for preparing update request body."""
  selected_log_type: Optional[str]
  selected_source_type: Optional[str]
  feed_display_name: Optional[str]
  flattened_response: Optional[Dict[str, Any]]
  error: Optional[str]


def fetch_feed_request_data(feed_schema: Any, region: str, url: str,
                            feed_id: str) -> Any:
  """Remove backup file if exists and fetch data for API request body.

  Args:
    feed_schema (object): Object of the FeedSchema class.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    url (str): Base URL to be used for API calls.
    feed_id (str): ID of the Feed to be updated.

  Returns:
    request_data (dataclass): Contains selected log type, selected source type
      and flattened response of get feed.
  """
  get_feed_response = feed_schema.client.request(
      "GET", f"{feed_utility.get_feed_url(region, url)}/{feed_id}")
  response = api_utility.check_content_type(get_feed_response.text)

  status_code = get_feed_response.status_code
  if status_code != status.STATUS_OK:
    error_msg = response[key_constants.KEY_ERROR][key_constants.KEY_MESSAGE]
    click.echo("\nError occurred while updating feed. Response code: "
               f"{get_feed_response.status_code}.\nError = "
               f"{error_msg}")
    return RequestData(None, None, None, None, error_msg)

  flattened_response = feed_utility.flatten_dict(response)
  selected_source_type = response[schema.KEY_DETAILS][
      schema.KEY_FEED_SOURCE_TYPE]
  selected_log_type = response[schema.KEY_DETAILS][key_constants.KEY_LOG_TYPE]
  feed_display_name = response.get(schema.KEY_DISPLAY_NAME)
  return RequestData(selected_log_type, selected_source_type, feed_display_name,
                     flattened_response, None)
