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
"""List errors of a log type between specific timestamps."""

import os
from typing import Any, AnyStr, Dict

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import file_utility
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parser import parser_templates
from parser import parser_utility
from parser import url
from parser.constants import key_constants as parser_constants


def get_formatted_error_logs(error_logs: Dict[str, Any]) -> str:
  """Get formatted error logs string to print on console.

  Args:
    error_logs: Dictionary containing multiple error logs

  Returns:
    str: Formatted error logs string to print on console
  """
  formatted_error_logs = []
  for index, log in enumerate(error_logs.get(parser_constants.KEY_LOGS, [])):
    formatted_error_logs.append(f"\n      {parser_utility.decode_log(log)}")
    if index != len(error_logs.get(parser_constants.KEY_LOGS)) - 1:
      formatted_error_logs.append(f'\n    {"-" * 56}')

  if formatted_error_logs:
    return f'Logs:{"".join(formatted_error_logs)}'
  return ""


@click.command(
    name="list_errors",
    help="List errors of a log type between specific timestamps")
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
def list_errors(credential_file: AnyStr, verbose: bool, region: str, env: str,
                export: AnyStr, file_format: AnyStr) -> None:
  """List errors of a log type between specific timestamps.

  Args:
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    env (str): Option for selecting environment. Available options - prod, test.
    export (AnyStr): Path of file to export output of list_errors command.
    file_format (AnyStr): Format of the content to be exported.

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  log_type = click.prompt("Enter Log Type", show_default=False, default="")
  start_date = click.prompt(
      "Enter Start Date (Format: yyyy-mm-ddThh:mm:ssZ)",
      show_default=False,
      default="")
  end_date = click.prompt(
      "Enter End Date (Format: yyyy-mm-ddThh:mm:ssZ)",
      show_default=False,
      default="")

  if not log_type:
    log_type = "UNSPECIFIED_LOG_TYPE"

  if (not start_date) or (not end_date):
    click.echo("Please enter start date and end date.")
    return

  click.echo("Getting parser errors...")

  list_errors_url = url.get_url(
      region,
      "list_errors",
      env,
      log_type=log_type,
      start_time=start_date,
      end_time=end_date)
  client = chronicle_auth.initialize_http_session(credential_file)
  method = "GET"
  response = client.request(
      method, list_errors_url, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  list_errors_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while fetching list of errors for the given log type:\nResponse Code: {response.status_code}"
        f"\nError: {list_errors_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  if common_constants.KEY_ERRORS not in list_errors_response:
    click.echo("No errors found for the log type and time range provided.")
    return

  errors_details = ""
  for errors in list_errors_response.get(common_constants.KEY_ERRORS, []):
    try:
      errors_details += parser_templates.errors_details_template.substitute(
          error_id=f"{errors[parser_constants.KEY_ERROR_ID]}",
          config_id=f"{errors.get(parser_constants.KEY_CONFIG_ID, 'N/A')}",
          log_type=f"{errors[common_constants.KEY_LOG_TYPE]}",
          error_time=f"{errors[parser_constants.KEY_ERROR_TIME]}",
          category=f"{errors[parser_constants.KEY_CATEGORY]}",
          error_msg=f"{errors[parser_constants.KEY_ERROR_MESSAGE]}",
          logs=get_formatted_error_logs(errors))
    except KeyError as e:
      errors_details += f"\nKey {str(e)} not found in the response."
    except Exception as e:  # pylint: disable=broad-except
      errors_details += f"\nFailed with exception: str({e})"
    errors_details += f'\n\n{"=" * 60}\n'

  click.echo(errors_details)

  if export:
    export_path = os.path.abspath(export) + f".{file_format.lower()}"
    if file_format == file_utility.FILE_FORMAT_JSON:
      for index, error in enumerate(
          list_errors_response[common_constants.KEY_ERRORS]):
        decode_logs = []
        for log in error.get(parser_constants.KEY_LOGS, []):
          decode_logs.append(parser_utility.decode_log(log))
        list_errors_response[common_constants.KEY_ERRORS][index][
            parser_constants.KEY_LOGS] = decode_logs
      file_utility.export_json(export_path, list_errors_response)
    else:
      file_utility.export_txt(export_path, errors_details)
    click.echo(
        f"\nParser Errors details exported successfully to: {export_path}")

  if verbose:
    api_utility.print_request_details(list_errors_url, method, None,
                                      list_errors_response)
