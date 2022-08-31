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
"""List all parsers of a given customer."""

import os
from typing import AnyStr

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import file_utility
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parser import parser_templates
from parser import url
from parser.constants import key_constants as parser_constants


@click.command(name="list", help="List all parsers of a given customer")
@click.option(
    "-f",
    "--file-format",
    type=click.Choice(["TXT", "JSON"], case_sensitive=False),
    default="TXT",
    help="Format of the file to be exported")
@options.export_option
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def list_command(credential_file: AnyStr, verbose: bool, region: str, env: str,
                 export: AnyStr, file_format: AnyStr) -> None:
  """List all parsers of a given customer.

  Args:
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    env (str): Option for selecting environment. Available options - prod, test.
    export (AnyStr): Path of file to export output of list command.
    file_format (AnyStr): Format of the content to be exported.

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  click.echo("Fetching list of parsers...")
  list_parser_url = url.get_url(region, "list", env)
  client = chronicle_auth.initialize_http_session(credential_file)
  method = "GET"
  response = client.request(
      method, list_parser_url, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parser_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while fetching list of parsers.\nResponse Code: {response.status_code}"
        f"\nError: {parser_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  if parser_constants.KEY_CBN_PARSER not in parser_response:
    click.echo("No CBN parsers currently configured.")
    return

  parser_details = ""
  for parser in parser_response[parser_constants.KEY_CBN_PARSER]:
    try:
      del parser[parser_constants.KEY_CONFIG]
      parser_details += parser_templates.parser_details_template.substitute(
          config_id=f"{parser[parser_constants.KEY_CONFIG_ID]}",
          log_type=f"{parser[common_constants.KEY_LOG_TYPE]}",
          state=f"{parser[parser_constants.KEY_STATE]}",
          sha256=f"{parser[parser_constants.KEY_SHA256]}",
          author=f'{parser.get(parser_constants.KEY_AUTHOR, "-")}',
          submit_time=f"{parser[parser_constants.KEY_SUBMIT_TIME]}",
          last_live_time=f"{parser[parser_constants.KEY_LAST_LIVE_TIME]}",
          state_last_changed_time=f"{parser[parser_constants.KEY_STATE_LAST_CHANGED_TIME]}"
      )
    except KeyError as e:
      parser_details += f"\nKey {str(e)} not found in the response."
    except Exception as e:  # pylint: disable=broad-except
      parser_details += f"\nFailed with exception: str({e})"
    parser_details += f'\n\n{"=" * 60}\n'

  click.echo(parser_details)

  if export:
    export_path = os.path.abspath(export) + f".{file_format.lower()}"
    if file_format == file_utility.FILE_FORMAT_JSON:
      file_utility.export_json(export_path, parser_response)
    else:
      file_utility.export_txt(export_path, parser_details)
    click.echo(f"\nParser details exported successfully to: {export_path}")

  if verbose:
    api_utility.print_request_details(list_parser_url, method, None,
                                      parser_response)
