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
"""List all forwarders for the customer."""
import copy
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
from forwarders import collector_utility
from forwarders import forwarder_utility
from forwarders.constants import schema


@click.command(name="list", help="List all forwarders")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def list_command(credential_file: AnyStr, verbose: bool, region: str,
                 url: str) -> None:
  """List all forwarders and its associated collectors for the customer.

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
  click.echo("Fetching list of forwarders...")
  url = commands_utility.lower_or_none(url)
  client = chronicle_auth.initialize_http_session(credential_file)
  forwarder_url = forwarder_utility.get_forwarder_url(region, url)
  method = "GET"
  list_forwarders_response = client.request(method, forwarder_url)

  forwarders_response = api_utility.check_content_type(
      list_forwarders_response.text)
  status_code = list_forwarders_response.status_code

  if status_code != status.STATUS_OK:
    error_message = forwarders_response[key_constants.KEY_ERROR][
        key_constants.KEY_MESSAGE]
    click.echo(
        f"\nError while fetching list of forwarders.\nResponse Code: {status_code}"
        f"\nError: {error_message}")
    return

  if not forwarders_response:
    click.echo("No forwarders found.")
    return

  # List of forwarders.
  forwarders = copy.deepcopy(forwarders_response[schema.KEY_FORWARDERS])

  collector_verbose_list = list_forwarders_and_associated_collectors(
      region, url, client, forwarders, method)

  if verbose:
    api_utility.print_request_details(forwarder_url, method, None,
                                      forwarders_response)
    for verbose_data in collector_verbose_list:
      api_utility.print_request_details(
          getattr(verbose_data, "url"), method, None,
          getattr(verbose_data, "response"))


@dataclasses.dataclass
class Verbose:
  """Verbose dataclass."""
  url: str
  response: Any


def list_forwarders_and_associated_collectors(region: str, url: str,
                                              client: Any,
                                              forwarders: List[Dict[str, Any]],
                                              method: str) -> Any:
  """List all forwarders and its associated collectors for the customer.

  Args:
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    url (str): Base URL to be used for API calls.
    client (Any): HTTP session object to send authorized requests and receive
      responses.
    forwarders (List[Dict[str, Any]]): List of forwarders.
    method (str): Method to be used for API calls.

  Returns:
    Any:
      collector_verbose_list - Contains list of Verbose object with
      collector request url and method for verbose output
  """
  collector_verbose_list = []

  for forwarder in forwarders:

    forwarder_id = forwarder_utility.get_resource_id(forwarder)
    forwarder.update({schema.KEY_NAME: forwarder_id})
    collector_url = collector_utility.get_collector_url(region, url,
                                                        forwarder_id)

    # Fetch collectors for respective forwarders.
    collectors_api_response, collectors = collector_utility.fetch_collectors(
        collector_url, method, client)

    # Store URL and API response for each collector to
    # print verbose on console later.
    collector_verbose_list.append(
        Verbose(collector_url, collectors_api_response))

    for collector in collectors_api_response.get(schema.KEY_COLLECTORS, []):

      if "error" not in collector:

        # Converts list of collectors to nested dictionary object with key name
        # "Collector [<collector_uuid>]" for easy readability in yaml output.
        # Example-{"collectors":{"Collector [<collector_uuid>]":{"name":""}}}
        collector_id = forwarder_utility.get_resource_id(collector)
        collector.update({schema.KEY_NAME: collector_id})

        collectors[schema.KEY_COLLECTORS][
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
                collectors)))
    click.echo(f"{forwarder_utility.PRINT_SEPARATOR}")

  return collector_verbose_list
