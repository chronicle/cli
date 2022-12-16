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
"""Get a collector."""

from typing import Any

import click

from common import api_utility
from common import chronicle_auth
from common import commands_utility
from common import exception_handler
from common import options
from common.constants import key_constants
from common.constants import status
from forwarders import forwarder_utility
from forwarders.collectors import collector_utility
from forwarders.constants import schema


@click.command(help="Get a collector using forwarder and collector ID.")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def get(credential_file: Any, verbose: bool, region: str, url: str) -> None:
  """Gets collector details using Forwarder and Collector ID.

  Args:
    credential_file (str): Path of Service Account JSON.
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
    click.echo("Forwarder ID not provided. Please enter forwarder ID.")
    return

  collector_id = click.prompt(
      "Enter Collector ID", default="", show_default=False)
  if not collector_id:
    click.echo("Collector ID not provided. Please enter collector ID.")
    return

  url = commands_utility.lower_or_none(url)
  client = chronicle_auth.initialize_http_session(credential_file)
  method = "GET"

  click.echo("\nFetching collector details...")
  collector_response, collector_url = get_collector(region, url, method, client,
                                                    forwarder_id, collector_id)

  if collector_response:
    collector_response.update({schema.KEY_NAME: collector_id})

    collector_details = commands_utility.convert_dict_keys_to_human_readable(
        forwarder_utility.change_dict_keys_order(collector_response))

    display_output = {}
    # Capitalize keyword ID to display output on console.
    if collector_details.get(schema.KEY_ID.capitalize()):
      display_output[schema.KEY_ID] = collector_details.pop(
          schema.KEY_ID.capitalize())
    display_output.update(collector_details)

    click.echo("\nCollector Details:\n")
    click.echo(commands_utility.convert_dict_to_yaml(display_output))
    if verbose:
      api_utility.print_request_details(collector_url, method, None,
                                        collector_response)


def get_collector(region: str, url: str, method: str, client: Any,
                  forwarder_id: str, collector_id: str) -> Any:
  """Gets collector details using Forwarder and Collector ID.

  Args:
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    url (str): Base URL to be used for API calls.
    method (str): Method to be used for API calls.
    client (Any): HTTP session object to send authorized requests and receive
      responses.
    forwarder_id (str): ID of the forwarder.
    collector_id (str): Id of the collector.

  Returns:
    Any: Collector response, collector_url.
  """
  collector_url = (
      f"{collector_utility.get_collector_url(region, url, forwarder_id)}"
      f"/{collector_id}")

  get_collector_response = client.request(method, collector_url)
  collector_response = api_utility.check_content_type(
      get_collector_response.text)
  status_code = get_collector_response.status_code

  if status_code == status.STATUS_OK:
    return collector_response, collector_url
  elif status_code == status.STATUS_NOT_FOUND:
    click.echo("Collector does not exist.")
  elif status_code == status.STATUS_BAD_REQUEST:
    click.echo("Invalid Collector ID. Please enter valid Collector ID.")
  else:
    error_message = collector_response[key_constants.KEY_ERROR][
        key_constants.KEY_MESSAGE]
    click.echo(
        f"\nError while fetching collector.\nResponse Code: {status_code}"
        f"\nError: {error_message}")
  return None, None
