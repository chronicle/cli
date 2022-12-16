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

import dataclasses
from typing import Any, AnyStr, Dict, List

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
  method = "GET"

  click.echo("\nFetching forwarder and its all associated collectors...")
  get_forwarder_response = get_forwarder(region, url, method, client,
                                         forwarder_id)

  (forwarder_url, forwarder_response,
   collector_verbose_list, collectors_response) = getattr(
       get_forwarder_response, "forwarder_url",
       ""), getattr(get_forwarder_response, "forwarder_response",
                    {}), getattr(get_forwarder_response,
                                 "collector_verbose_list",
                                 []), getattr(get_forwarder_response,
                                              "collectors_response", {})

  if key_constants.KEY_ERROR not in forwarder_response:
    forwarder_details = commands_utility.convert_dict_keys_to_human_readable(
        forwarder_utility.change_dict_keys_order(forwarder_response))

    display_output = {}
    # Capitalize keyword ID to display output on console.
    if forwarder_details.get(schema.KEY_ID.capitalize()):
      display_output[schema.KEY_ID] = forwarder_details.pop(
          schema.KEY_ID.capitalize())
    display_output.update(forwarder_details)

    click.echo("\nForwarder Details:\n")
    click.echo(commands_utility.convert_dict_to_yaml(display_output))

    if collectors_response:
      click.echo(
          commands_utility.convert_dict_to_yaml(
              commands_utility.convert_dict_keys_to_human_readable(
                  collectors_response)))
      click.echo(f"{forwarder_utility.PRINT_SEPARATOR}")

  if verbose:
    api_utility.print_request_details(forwarder_url, method, None,
                                      forwarder_response)
    for collector_response in collector_verbose_list:
      api_utility.print_request_details(
          collector_response.get("url", ""), method, None,
          collector_response.get("response", {}))


@dataclasses.dataclass
class GetForwarderResponse:
  """GetForwarderResponse dataclass."""
  forwarder_url: str
  forwarder_response: Dict[str, Any]
  collector_verbose_list: List[Dict[str, Any]]
  collectors_response: Dict[str, Any]


def get_forwarder(region: str, url: str, method: str, client: Any,
                  forwarder_id: str) -> GetForwarderResponse:
  """Gets forwarder.

  Args:
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    url (str): Base URL to be used for API calls.
    method (str): Method to be used for API calls.
    client (Any): HTTP session object to send authorized requests and receive
      responses.
    forwarder_id (str): Id of the forwarder.

  Returns:
    GetForwarderResponse: Object contains Forwarder url, Forwarder response,
    list of collectors verbose and list of collectors.
  """
  forwarder_url = f"{forwarder_utility.get_forwarder_url(region, url)}/{forwarder_id}"
  get_forwarder_response = client.request(method, forwarder_url)
  forwarder_response = api_utility.check_content_type(
      get_forwarder_response.text)
  status_code = get_forwarder_response.status_code
  list_collectors_response = None

  if status_code == status.STATUS_OK:
    list_collectors_response = list_collectors(region, url, forwarder_response,
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

  return GetForwarderResponse(
      forwarder_url, forwarder_response,
      getattr(list_collectors_response, "collector_verbose_list", []),
      getattr(list_collectors_response, "collectors_response", {}))


@dataclasses.dataclass
class ListCollectorsResponse:
  """ListCollectorResponse dataclass."""
  collector_verbose_list: List[Dict[str, Any]]
  collectors_response: Dict[str, Any]


def list_collectors(region: str, url: str, forwarder: Dict[str, Any],
                    method: str, client: Any) -> ListCollectorsResponse:
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
    ListCollectorsResponse: Object contains collector_verbose_list and
    collectors_response.
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
      collector = forwarder_utility.change_dict_keys_order(collector)

      # Remove ID from the dictionary to avoid
      # displaying it multiple times on the console.
      collector.pop(schema.KEY_ID, None)
      collectors_response[
          schema.KEY_COLLECTORS][f"Collector [{collector_id}]"] = collector

  return ListCollectorsResponse(collector_verbose_list, collectors_response)
