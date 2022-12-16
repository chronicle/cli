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
"""Update a forwarder."""

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
from forwarders.commands.get import get_forwarder
from forwarders.constants import schema

BACKUP_FILE_NAME = "update_backup.json"
UPDATE_FORWARDER_BACKUP_FILE = os.path.join(
    chronicle_auth.CHRONICLE_CLI_ROOT_DIR, schema.KEY_FORWARDERS,
    BACKUP_FILE_NAME)


@click.command(help="Update a forwarder using Forwarder ID")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def update(credential_file: str, verbose: bool, region: str, url: str) -> None:
  """Updates forwarder.

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

  url = commands_utility.lower_or_none(url)
  client = chronicle_auth.initialize_http_session(credential_file)
  forwarder_url = forwarder_utility.get_forwarder_url(region, url)
  full_url = f"{forwarder_url}/{forwarder_id}"
  forwarder_response = {}

  # Check whether backup file exists for given forwarder ID.
  backup_request_body = forwarder_utility.read_backup(
      UPDATE_FORWARDER_BACKUP_FILE, forwarder_id)

  # If backup file does not exist then fetch forwarder details using API.
  if not backup_request_body:
    method = "GET"

    # We only need the forwarder information without the relevant collectors.
    get_forwarder_response = get_forwarder(region, url, method, client,
                                           forwarder_id)
    forwarder_url = getattr(get_forwarder_response, "forwarder_url", None)
    forwarder_response = getattr(get_forwarder_response, "forwarder_response",
                                 None)

    backup_request_body = commands_utility.convert_nested_dict_keys_to_snake_case(
        forwarder_response)

  if key_constants.KEY_ERROR not in forwarder_response:
    click.echo(
        f"\n{forwarder_utility.PRINT_SEPARATOR}\nPress Enter if you don't want to update.\n{forwarder_utility.PRINT_SEPARATOR}\n"
    )

    # "backup_request_body" is received along with the response body,
    # for storing the existing data into the backup file.
    forwarder_schema = schema_utility.Schema(schema.KEY_FORWARDER_SCHEMA,
                                             backup_request_body)
    request_body = forwarder_schema.prepare_request_body()
    flattened_response = commands_utility.flatten_dict(request_body)

    # Prepare update mask.
    updated_fields = list(flattened_response.keys())
    repeated_fields = list(forwarder_schema.repeated_message_fields)
    update_mask = forwarder_utility.prepare_update_mask(updated_fields,
                                                        repeated_fields)
    params = {"update_mask": ",".join(update_mask)}
    method = "PATCH"

    forwarder_utility.preview_changes(request_body)
    selected_choice = click.confirm(
        "\nDo you want to update forwarder with this configuration?",
        default=False)

    if selected_choice:
      click.echo("\nUpdating forwarder...")
      updated_forwarder_response = client.request(
          method, full_url, params=params, json=request_body)

      response = api_utility.check_content_type(updated_forwarder_response.text)

      if updated_forwarder_response.status_code == status.STATUS_OK:
        click.echo(
            f"\nForwarder updated successfully with Forwarder ID: {forwarder_id}"
        )
        file_utility.remove_file(UPDATE_FORWARDER_BACKUP_FILE)
      else:
        click.echo(
            "\nError occurred while updating forwarder.\nResponse Code: "
            f"{updated_forwarder_response.status_code}.\nError: "
            f"{response[key_constants.KEY_ERROR][key_constants.KEY_MESSAGE]}")

        # "request_body" written to the backup file in case of
        # failure to update forwarder.
        forwarder_utility.write_backup(UPDATE_FORWARDER_BACKUP_FILE,
                                       request_body, forwarder_id)

  if verbose:
    if forwarder_response:
      api_utility.print_request_details(full_url, method, None,
                                        forwarder_response)
    # Print verbose details for update if get forwarder successful.
    if key_constants.KEY_ERROR not in forwarder_response:
      api_utility.print_request_details(full_url, method, request_body,
                                        response)
