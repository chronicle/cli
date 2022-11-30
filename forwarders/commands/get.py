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
"""Get forwarder details using forwarder ID."""

from typing import Any, AnyStr, Dict

import click

from common import api_utility
from common import chronicle_auth
from common import commands_utility
from common import exception_handler
from common import options
from common.constants import key_constants
from common.constants import status
from forwarders import collector_utility
from forwarders import forwarder_utility
from forwarders.constants import schema


@click.command(help="Get forwarder details using Forwarder ID")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def get(credential_file: AnyStr, verbose: bool, region: str, url: str) -> None:
  """Gets forwarder details using Forwarder ID.

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
    click.echo("Forwarder ID not provided. Please enter Forwarder ID.")
    return

  url = commands_utility.lower_or_none(url)
  client = chronicle_auth.initialize_http_session(credential_file)
  forwarder_url = f"{forwarder_utility.get_forwarder_url(region, url)}/{forwarder_id}"
  method = "GET"

  click.echo("\nFetching forwarder and its all associated collectors...")
  get_forwarder_response = client.request(method, forwarder_url)
  forwarder_response = api_utility.check_content_type(
      get_forwarder_response.text)
  status_code = get_forwarder_response.status_code

  if status_code == status.STATUS_OK:
    collector_verbose_list = list_collectors(region, url, forwarder_response,
                                             method, client)
  elif status_code == status.STATUS_NOT_FOUND:
    click.echo("Forwarder does not exist.")
  elif status_code == status.STATUS_BAD_REQUEST:
    click.echo("Invalid Forwarder ID. Please enter valid Forwarder ID.")
  else:
    error_message = forwarder_response[key_constants.KEY_ERROR][
        key_constants.KEY_MESSAGE]
    click.echo(
        f"\nError while fetching forwarder details.\nResponse Code: {status_code}"
        f"\nError: {error_message}")
    return

  if verbose:
    api_utility.print_request_details(forwarder_url, method, None,
                                      forwarder_response)
    for collector_response in collector_verbose_list:
      api_utility.print_request_details(
          collector_response.get("url", ""), method, None,
          collector_response.get("response", {}))


def list_collectors(region: str, url: str, forwarder: Dict[str, Any],
                    method: str, client: Any) -> list[Any]:
  """List all collectors for forwarder.

  Args:
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    url (str): Base URL to be used for API calls.
    forwarder (Dict): Forwarder to fetch its associated collectors.
    method (str): Method to be used for API calls.
    client (Any): HTTP session object to send authorized requests and receive
      responses.

  Returns:
    list (Any): List of dictionary with for verbose console output.
  """
  collector_verbose_list = []

  forwarder_id = forwarder_utility.get_resource_id(forwarder)
  forwarder.update({schema.KEY_NAME: forwarder_id})
  collector_url = collector_utility.get_collector_url(region, url, forwarder_id)

  # Fetches collectors for respective forwarders.
  collectors_response_verbose, collectors_response = collector_utility.fetch_collectors(
      collector_url, method, client)

  collector_verbose_list.append({
      "url": collector_url,
      "response": collectors_response_verbose
  })

  for collector in collectors_response_verbose.get(schema.KEY_COLLECTORS, []):

    if "error" not in collector:

      # Converts list of collectors to nested dictionary object
      # with "Collector [<collector_uuid>]" key name for easy readability
      # in yaml output.
      # example-{"collectors":{"Collector [<collector_uuid>]":{"name":""}}}
      collector_id = forwarder_utility.get_resource_id(collector)
      collector.update({schema.KEY_NAME: collector_id})

      collectors_response[schema.KEY_COLLECTORS][
          f"Collector [{collector_id}]"] = forwarder_utility.change_dict_keys_order(
              collector)

  click.echo("\nForwarder Details:\n")
  click.echo(
      commands_utility.convert_dict_to_yaml(
          commands_utility.convert_dict_keys_to_human_readable(
              forwarder_utility.change_dict_keys_order(forwarder))))
  click.echo(
      commands_utility.convert_dict_to_yaml(
          commands_utility.convert_dict_keys_to_human_readable(
              collectors_response)))
  click.echo(f"{forwarder_utility.PRINT_SEPARATOR}")

  return collector_verbose_list
