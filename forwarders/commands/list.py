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
  forwarders = forwarders_response[schema.KEY_FORWARDERS]

  list_forwarders_and_associated_collectors(forwarders)

  if verbose:
    api_utility.print_request_details(forwarder_url, method, None,
                                      forwarders_response)


def list_forwarders_and_associated_collectors(
    forwarders: List[Dict[str, Any]]) -> None:
  """List all forwarders and its associated collectors for the customer.

  Args:
    forwarders (List[Dict[str, Any]]): List of forwarders.
  """

  for forwarder in forwarders:
    forwarder_id = forwarder.get(schema.KEY_NAME, "").split("/")[-1]

    click.echo(
        f"\n{forwarder_utility.PRINT_SEPARATOR}\n(Forwarder [{forwarder_id}])\n"
    )
    click.echo(
        commands_utility.convert_dict_to_yaml(
            commands_utility.convert_dict_keys_to_human_readable(
                forwarder_utility.change_dict_keys_order(forwarder))))
