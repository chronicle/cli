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
"""Delete a collector using forwarder ID and collector ID."""

from typing import AnyStr

import click

from common import api_utility
from common import chronicle_auth
from common import commands_utility
from common import exception_handler
from common import options
from common.constants import key_constants
from common.constants import status
from forwarders.collectors import collector_utility


@click.command(
    name="delete", help="Delete a collector using forwarder and collector ID.")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def delete(credential_file: AnyStr, verbose: bool, region: str,
           url: str) -> None:
  """Delete a collector using Forwarder and Collector ID with all its associated collectors.

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
  collector_url = f"{collector_utility.get_collector_url(region, url, forwarder_id)}/{collector_id}"
  method = "DELETE"

  collector_response = client.request(method, collector_url)
  status_code = collector_response.status_code
  collector_response = api_utility.check_content_type(collector_response.text)

  if status_code == status.STATUS_OK:
    click.echo(f"\nCollector (ID: {collector_id}) deleted successfully.")
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
    return

  if verbose:
    api_utility.print_request_details(collector_url, method, None,
                                      collector_response)
