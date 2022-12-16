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
"""Create a collector."""

import json
import os.path
from typing import Any

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
from forwarders.collectors import collector_utility
from forwarders.constants import schema
from forwarders.schema_utility import Schema

CREATE_COLLECTOR_BACKUP_FILE = os.path.join(
    chronicle_auth.CHRONICLE_CLI_ROOT_DIR, "collectors", "create_backup.json")


@click.command(name="create", help="Create a collector.")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def create(credential_file: str, verbose: bool, region: str, url: str) -> None:
  """Creates a collector.

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

  forwarder_id = click.prompt(
      "\nEnter Forwarder ID", default="", show_default=False)
  if not forwarder_id:
    click.echo("Forwarder ID not provided. Please enter Forwarder ID.")
    return

  url = commands_utility.lower_or_none(url)
  client = chronicle_auth.initialize_http_session(credential_file)
  create_collector(forwarder_id, url, client, verbose, region)


def create_collector(forwarder_id: str, url: str, client: Any, verbose: bool,
                     region: str):
  """Creates collector.

  Args:
    forwarder_id (str): Id of forwarder.
    url (str): Base URL to be used for API calls.
    client (Any): HTTP session object.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
  """

  collector_url = collector_utility.get_collector_url(region, url, forwarder_id)
  method = "POST"

  # Check whether backup file exists and if it exists,
  # read the response from the file to use it further
  # to show default values in prompts.
  backup_request_body = forwarder_utility.read_backup(
      CREATE_COLLECTOR_BACKUP_FILE, forwarder_id)

  collector_schema = Schema(schema.KEY_COLLECTOR_SCHEMA, backup_request_body)

  request_body = collector_schema.prepare_request_body()

  forwarder_utility.preview_changes(request_body)
  selected_choice = click.confirm(
      "\nDo you want to create collector with this configuration?")

  if selected_choice:
    click.echo("\nCreating collector...")
    create_collector_response = client.request(method, collector_url,
                                               json.dumps(request_body))

    response = api_utility.check_content_type(create_collector_response.text)

    if create_collector_response.status_code != status.STATUS_OK:
      click.echo(
          "\nError occurred while creating collector.\nResponse Code: "
          f"{create_collector_response.status_code}.\nError: "
          f"{response[key_constants.KEY_ERROR][key_constants.KEY_MESSAGE]}")

      # "request_body" written to the backup file in case of
      # failure to create collector.
      forwarder_utility.write_backup(CREATE_COLLECTOR_BACKUP_FILE,
                                     request_body, forwarder_id)
      return

    collector_id = forwarder_utility.get_resource_id(response)
    click.echo(
        f"Collector created successfully with Collector ID: {collector_id}")
    file_utility.remove_file(CREATE_COLLECTOR_BACKUP_FILE)
    if verbose:
      api_utility.print_request_details(collector_url, method, request_body,
                                        response)
