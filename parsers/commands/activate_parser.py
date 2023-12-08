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
"""Activate a parser."""

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parsers import url


@click.command(name="activate_parser", help="[New]Activate a parser")
@click.argument("project_id", required=True, default="")
@click.argument("customer_id", required=True, default="")
@click.argument("log_type", required=True, default="")
@click.argument("parser_id", required=True, default="")
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@options.v2_option
@exception_handler.catch_exception()
def activate_parser(
    v2: bool,
    credential_file: str,
    verbose: bool,
    region: str,
    env: str,
    project_id: str,
    customer_id: str,
    log_type: str,
    parser_id: int) -> None:
  """Activate a parser given the Parser ID.

  Args:
    v2 (bool): Option for enabling v2 commands.
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    env (str): Option for selection environment. Available options - prod, test.
    project_id (str): The GCP Project ID.
    customer_id (str): The Customer ID.
    log_type (str): The Log Type.
    parser_id (int): The Parser ID.

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  if not v2:
    click.echo("--v2 flag not provided. "
               "Please provide the flag to run the new commands")
    return

  if not project_id:
    click.echo("Project ID not provided. Please enter Project ID")
    return

  if not customer_id:
    click.echo("Customer ID not provided. Please enter Customer ID")
    return

  if not log_type:
    click.echo("Log Type not provided. Please enter Log Type")
    return

  if not parser_id:
    click.echo("Parser ID not provided. Please enter Parser ID")
    return

  click.echo("Activating Parser...")

  resources = {
      "project": project_id,
      "location": region.lower(),
      "instance": customer_id,
      "log_type": log_type,
      "parser": parser_id
  }

  activate_parser_url = url.get_dataplane_url(
      region,
      "activate_parser",
      env,
      resources)
  client = chronicle_auth.initialize_dataplane_http_session(credential_file)
  method = "POST"
  response = client.request(
      method, activate_parser_url, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parsed_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while activating parser.\n"
        f"Response Code: {response.status_code}\n"
        f"Error: "
        f"{parsed_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  click.echo("Parser activated successfully.")

  if verbose:
    api_utility.print_request_details(
        activate_parser_url, method, None, parsed_response
    )
