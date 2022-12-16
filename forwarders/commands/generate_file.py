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
"""Generate Forwarders File."""

import os
from typing import AnyStr

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

CONF_FILE_EXTENSION = "conf"


@click.command(
    name="generate_file",
    help="Generate forwarder configuration using Forwarder ID")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@click.option(
    "--file-path",
    default="",
    help="Download generated forwarder file to the specified path.")
@exception_handler.catch_exception()
def generate_file(credential_file: AnyStr, verbose: bool, region: str, url: str,
                  file_path: AnyStr) -> None:
  """Generate forwarder file using Forwarder ID.

  Args:
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing listverbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    url (str): Base URL to be used for API calls.
    file_path (AnyStr): Path where the generated forwarder file would be stored.
  """
  forwarder_id = click.prompt(
      "Enter Forwarder ID", default="", show_default=False)
  if not forwarder_id:
    click.echo("Forwarder ID not provided. Please enter Forwarder ID.")
    return

  url = commands_utility.lower_or_none(url)
  client = chronicle_auth.initialize_http_session(credential_file)
  forwarder_url = f"{forwarder_utility.get_forwarder_url(region, url)}/{forwarder_id}:generateForwarderFiles"
  method = "GET"

  generate_forwarders_response = client.request(method, forwarder_url)
  forwarder_response = api_utility.check_content_type(
      generate_forwarders_response.text)
  status_code = generate_forwarders_response.status_code

  download_path = os.path.abspath(file_path) if file_path else os.path.abspath(
      forwarder_id)

  click.echo("Generating forwarder file ...")

  if status_code == status.STATUS_OK:
    file_utility.export_txt(f"{download_path}.{CONF_FILE_EXTENSION}",
                            forwarder_response["config"])
    click.echo(
        f"Forwarder configuration generated successfully at the following path: {download_path}.{CONF_FILE_EXTENSION}"
    )
  else:
    error_message = forwarder_response[key_constants.KEY_ERROR][
        key_constants.KEY_MESSAGE]
    click.echo(
        f"\nError while generating forwarder file.\nResponse Code: {status_code}"
        f"\nError: {error_message}")

  if verbose:
    api_utility.print_request_details(forwarder_url, method, None,
                                      forwarder_response)
