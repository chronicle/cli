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
"""Update a collector."""

import os

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
from forwarders.collectors import collector_utility
from forwarders.collectors.commands.get import get_collector
from forwarders.constants import schema

BACKUP_FILE_NAME = "update_backup.json"
UPDATE_COLLECTOR_BACKUP_FILE = os.path.join(
    chronicle_auth.CHRONICLE_CLI_ROOT_DIR, schema.KEY_COLLECTORS,
    BACKUP_FILE_NAME)


@click.command(
    name="update", help="Update a collector using forwarder and collector ID.")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def update(credential_file: str, verbose: bool, region: str, url: str) -> None:
  """Updates a collector.

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
  forwarder_id = click.prompt(
      "Enter Forwarder ID", default="", show_default=False)
  if not forwarder_id:
    click.echo("Forwarder ID not provided. Please enter Forwarder ID.")
    return

  collector_id = click.prompt(
      "Enter Collector ID", default="", show_default=False)
  if not collector_id:
    click.echo("Collector ID not provided. Please enter Collector ID.")
    return

  url = commands_utility.lower_or_none(url)
  client = chronicle_auth.initialize_http_session(credential_file)
  collector_url = (
      f"{collector_utility.get_collector_url(region, url, forwarder_id)}"
      f"/{collector_id}")

  # Check whether backup file exists for given collector ID.
  backup_request_body = forwarder_utility.read_backup(
      UPDATE_COLLECTOR_BACKUP_FILE, collector_id)

  # If backup file does not exist then fetch collector details using API.
  if not backup_request_body:
    method = "GET"
    collector_response, collector_url = get_collector(region, url, method,
                                                      client, forwarder_id,
                                                      collector_id)
    if not collector_response and not collector_url:
      return
    backup_request_body = commands_utility.convert_nested_dict_keys_to_snake_case(
        collector_response)

  click.echo(
      f"\n{forwarder_utility.PRINT_SEPARATOR}\nPress Enter if you don't want to update.\n{forwarder_utility.PRINT_SEPARATOR}"
  )

  # "flattened_response" is received along with the response body,
  # for storing the existing data into the backup file.
  collector_schema = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA,
                                           backup_request_body)
  request_body = collector_schema.prepare_request_body()
  flattened_response = commands_utility.flatten_dict(request_body)

  # Prepare update mask.
  updated_fields = list(flattened_response.keys())
  repeated_fields = list(collector_schema.repeated_message_fields)
  update_mask = forwarder_utility.prepare_update_mask(updated_fields,
                                                      repeated_fields)
  params = {"update_mask": ",".join(update_mask)}
  method = "PATCH"

  forwarder_utility.preview_changes(request_body)
  selected_choice = click.confirm(
      "\nDo you want to update collector with this configuration?",
      default=False)

  if selected_choice:
    click.echo("\nUpdating collector...")
    updated_collector_response = client.request(
        method, collector_url, params=params, json=request_body)

    response = api_utility.check_content_type(updated_collector_response.text)

    if updated_collector_response.status_code != status.STATUS_OK:
      click.echo(
          "\nError occurred while updating collector.\nResponse Code: "
          f"{updated_collector_response.status_code}.\nError: "
          f"{response[key_constants.KEY_ERROR][key_constants.KEY_MESSAGE]}")

      # "request_body" written to the backup file in case of
      # failure to update collector.
      forwarder_utility.write_backup(UPDATE_COLLECTOR_BACKUP_FILE, request_body,
                                     collector_id)
      return

    click.echo(
        f"\nCollector updated successfully with Collector ID: {collector_id}")
    file_utility.remove_file(UPDATE_COLLECTOR_BACKUP_FILE)
    if verbose:
      api_utility.print_request_details(collector_url, method, request_body,
                                        response)
