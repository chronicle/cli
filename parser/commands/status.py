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
"""Get status of a submitted parser."""

from typing import AnyStr

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parser import parser_templates
from parser import url
from parser.constants import key_constants as parser_constants


@click.command(name="status", help="Get status of a submitted parser")
@options.env_option
@options.verbose_option
@options.region_option
@options.credential_file_option
@exception_handler.catch_exception()
def status_command(credential_file: AnyStr, verbose: bool, region: str,
                   env: str) -> None:
  """Get status of a submitted parser.

  Args:
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    env (str): Option for selecting environment. Available options - prod, test.

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  config_id = click.prompt("Enter Config ID", default="", show_default=False)

  if not config_id:
    click.echo("\nPlease enter config id.")
    return

  click.echo("\nGetting parser...")

  # Make the request.
  get_parser_status_url = f"{url.get_url(region, 'status', env)}/{config_id}"
  method = "GET"
  client = chronicle_auth.initialize_http_session(credential_file)
  response = client.request(
      method, get_parser_status_url, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parser = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while fetching status for parser.\nResponse Code: {response.status_code}"
        f"\nError: {parser[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  parser_details = parser_templates.parser_details_template.substitute(
      config_id=f"{parser[parser_constants.KEY_CONFIG_ID]}",
      log_type=f"{parser[common_constants.KEY_LOG_TYPE]}",
      state=f"{parser[parser_constants.KEY_STATE]}",
      sha256=f"{parser[parser_constants.KEY_SHA256]}",
      author=f"{parser[parser_constants.KEY_AUTHOR]}",
      submit_time=f"{parser[parser_constants.KEY_SUBMIT_TIME]}",
      last_live_time=f"{parser[parser_constants.KEY_LAST_LIVE_TIME]}",
      state_last_changed_time=f"{parser[parser_constants.KEY_STATE_LAST_CHANGED_TIME]}"
  )
  click.echo(parser_details)

  if verbose:
    api_utility.print_request_details(get_parser_status_url, method, None,
                                      parser)
