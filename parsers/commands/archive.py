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
"""Archives a parser given the config ID."""

from typing import AnyStr

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parsers import parser_templates
from parsers import url
from parsers.constants import key_constants as parser_constants


@click.command(name="archive", help="Archives a parser given the config ID")
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def archive(credential_file: AnyStr, verbose: bool, region: str,
            env: str) -> None:
  """Archives a parser given the config ID.

  Args:
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    env (str): Option for selection environment. Available options - prod, test.

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  config_id = click.prompt("Enter Config ID", show_default=False, default="")

  if not config_id:
    click.echo("Config ID not provided. Please enter Config ID.")
    return

  click.echo("Archiving parser...")

  archive_parser_url = f"{url.get_url(region, 'list', env)}/{config_id}:archive"
  client = chronicle_auth.initialize_http_session(credential_file)
  method = "POST"
  response = client.request(
      method, archive_parser_url, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)

  parsed_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while archiving parser.\nResponse Code: {response.status_code}"
        f"\nError: {parsed_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  click.echo("\nParser archived successfully.")
  parser_details = parser_templates.parser_details_template.substitute(
      config_id=f"{parsed_response[parser_constants.KEY_CONFIG_ID]}",
      log_type=f"{parsed_response[common_constants.KEY_LOG_TYPE]}",
      state=f"{parsed_response[parser_constants.KEY_STATE]}",
      sha256=f"{parsed_response[parser_constants.KEY_SHA256]}",
      author=f"{parsed_response[parser_constants.KEY_AUTHOR]}",
      submit_time=f"{parsed_response[parser_constants.KEY_SUBMIT_TIME]}",
      last_live_time=f'{parsed_response.get(parser_constants.KEY_LAST_LIVE_TIME, "-")}',
      state_last_changed_time=f"{parsed_response[parser_constants.KEY_STATE_LAST_CHANGED_TIME]}"
  )
  click.echo(parser_details)

  if verbose:
    api_utility.print_request_details(archive_parser_url, method, None,
                                      parsed_response)
