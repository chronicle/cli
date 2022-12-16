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
"""Create a Forwarder."""

import json
import os.path

import click

from common import api_utility
from common import chronicle_auth
from common import commands_utility
from common import exception_handler
from common import file_utility
from common import options
from common.constants import key_constants
from common.constants import status
from forwarders import forwarder_utility
from forwarders import schema_utility
from forwarders.collectors.commands import create as create_collector
from forwarders.constants import schema

CREATE_FORWARDER_BACKUP_FILE = os.path.join(
    chronicle_auth.CHRONICLE_CLI_ROOT_DIR, schema.KEY_FORWARDERS,
    "create_backup.json")


@click.command(help="Create a Forwarder")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def create(credential_file: str, verbose: bool, region: str, url: str) -> None:
  """Creates forwarder.

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
  instruction_str = (
      "Press Enter if you want to use the default value mentioned besides "
      "field description in [] brackets.")
  click.echo(
      f"{forwarder_utility.PRINT_SEPARATOR}\n{instruction_str}\n{forwarder_utility.PRINT_SEPARATOR}"
  )

  url = commands_utility.lower_or_none(url)
  client = chronicle_auth.initialize_http_session(credential_file)
  forwarder_url = forwarder_utility.get_forwarder_url(region, url)
  method = "POST"

  # Check whether backup file exists and if it exists,
  # read the response from the file to use it further
  # to show default values in prompts.
  backup_request_body = forwarder_utility.read_backup(
      CREATE_FORWARDER_BACKUP_FILE)

  # "backup_request_body" is received along with the response body,
  # for storing the existing data into the backup file.
  forwarder_schema = schema_utility.Schema(schema.KEY_FORWARDER_SCHEMA,
                                           backup_request_body)

  request_body = forwarder_schema.prepare_request_body()
  # Preview changes.
  forwarder_utility.preview_changes(request_body)
  selected_choice = click.confirm(
      "\nDo you want to create forwarder with this configuration?",
      default=False)

  if selected_choice:
    click.echo("\nCreating forwarder...")
    create_forwarder_response = client.request(method, forwarder_url,
                                               json.dumps(request_body))

    response = api_utility.check_content_type(create_forwarder_response.text)

    if create_forwarder_response.status_code != status.STATUS_OK:
      click.echo(
          "\nError occurred while creating forwarder.\nResponse Code: "
          f"{create_forwarder_response.status_code}.\nError: "
          f"{response[key_constants.KEY_ERROR][key_constants.KEY_MESSAGE]}")

      # "request_body" written to the backup file in case of
      # failure to create forwarder.
      forwarder_utility.write_backup(CREATE_FORWARDER_BACKUP_FILE, request_body)
      return

    forwarder_id = forwarder_utility.get_resource_id(response)
    click.echo(
        f"Forwarder created successfully with Forwarder ID: {forwarder_id}")
    file_utility.remove_file(CREATE_FORWARDER_BACKUP_FILE)
    if verbose:
      api_utility.print_request_details(forwarder_url, method, request_body,
                                        response)

    # Configure collectors for this forwarder.
    selected_choice = click.confirm(
        "\nWould you like to configure collectors for this forwarder?",
        default=False)

    while selected_choice:
      create_collector.create_collector(forwarder_id, url, client, verbose,
                                        region)
      selected_choice = click.confirm(
          "\nWould you like to add more collectors?", default=False)
