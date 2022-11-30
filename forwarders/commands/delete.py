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
"""Delete a forwarder using forwarder ID."""

from typing import AnyStr

import click

from common import api_utility
from common import chronicle_auth
from common import commands_utility
from common import exception_handler
from common import options
from common.constants import key_constants
from common.constants import status
from forwarders import forwarder_utility


@click.command(help="Delete a forwarder using Forwarder ID")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def delete(credential_file: AnyStr, verbose: bool, region: str,
           url: str) -> None:
  """Delete a forwarder using Forwarder ID with all its associated collectors.

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
  forwarder_url = f"{forwarder_utility.get_forwarder_url(region, url)}/{forwarder_id}"
  method = "DELETE"

  click.echo("\nDeleting forwarder and all its associated collectors...")
  forwarder_response = client.request(method, forwarder_url)
  status_code = forwarder_response.status_code
  forwarder_response = api_utility.check_content_type(forwarder_response.text)

  if status_code == status.STATUS_OK:
    click.echo(
        f"\nForwarder (ID: {forwarder_id}) deleted successfully with all its associated collectors."
    )
  elif status_code == status.STATUS_NOT_FOUND:
    click.echo("Forwarder does not exist.")
  elif status_code == status.STATUS_BAD_REQUEST:
    click.echo("Invalid Forwarder ID. Please enter valid Forwarder ID.")
  else:
    if status_code != status.STATUS_OK:
      error_message = forwarder_response[key_constants.KEY_ERROR][
          key_constants.KEY_MESSAGE]
      click.echo(
          f"\nError while fetching forwarder.\nResponse Code: {status_code}"
          f"\nError: {error_message}")
      return

  if verbose:
    api_utility.print_request_details(forwarder_url, method, None,
                                      forwarder_response)
