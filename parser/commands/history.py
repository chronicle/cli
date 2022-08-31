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
"""History retrieves all parser submissions given a log type."""

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


@click.command(
    name='history',
    help='History retrieves all parser submissions given a log type')
@click.option(
    '-f',
    '--file-format',
    type=click.Choice(['TXT', 'JSON'], case_sensitive=False),
    default='TXT',
    help='Format of the file to be exported')
@options.export_option
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def history(credential_file: AnyStr, verbose: bool, region: str, env: str,
            export: AnyStr, file_format: AnyStr) -> None:
  """History retrieves all parser submissions given a log type.

  Args:
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    env (str): Option for selection environment. Available options - prod, test.
    export (AnyStr): Path of file to export output of list command.
    file_format (AnyStr): Format of the content to be exported.

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  log_type = click.prompt('Enter Log Type', show_default=False, default='')

  if not log_type:
    click.echo('Log type not provided. Please enter log type.')
    return

  click.echo('Fetching history for parser...')

  history_url = url.get_url(region, 'history', env, log_type=log_type)
  method = 'GET'
  client = chronicle_auth.initialize_http_session(credential_file)
  response = client.request(
      method,
      history_url,
      headers=url.HTTP_REQUEST_HEADERS,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parsed_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f'Error while fetching history for parser.\nResponse Code: {response.status_code}'
        f'\nError: {parsed_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}'
    )
    return

  if parser_constants.KEY_CBN_PARSER not in parsed_response:
    click.echo('No CBN parser currently configured.')
    return

  parser_history_details = ''
  for parser_history in parsed_response[parser_constants.KEY_CBN_PARSER]:
    try:
      del parser_history[parser_constants.KEY_CONFIG]
      parser_history_details += parser_templates.parser_history_template.substitute(
          config_id=f'{parser_history[parser_constants.KEY_CONFIG_ID]}',
          log_type=f'{parser_history[common_constants.KEY_LOG_TYPE]}',
          state=f'{parser_history[parser_constants.KEY_STATE]}',
          sha256=f'{parser_history[parser_constants.KEY_SHA256]}',
          author=f'{parser_history.get(parser_constants.KEY_AUTHOR, "-")}',
          submit_time=f'{parser_history[parser_constants.KEY_SUBMIT_TIME]}',
          last_live_time=get_last_live_time(parser_history),
          state_last_changed_time=f'{parser_history[parser_constants.KEY_STATE_LAST_CHANGED_TIME]}',
          validationErrors=get_validation_errors(parser_history))
    except KeyError as e:
      parser_history_details += f'\nKey {str(e)} not found in the response.'
    except Exception as e:  # pylint: disable=broad-except
      parser_history_details += f'\nFailed with exception: str({e})'
    parser_history_details += f'\n\n{"=" * 60}\n'

  click.echo(parser_history_details)

  if export:
    export_path = os.path.abspath(export) + f'.{file_format.lower()}'
    if file_format == file_utility.FILE_FORMAT_JSON:
      file_utility.export_json(export_path, parsed_response)
    else:
      file_utility.export_txt(export_path, parser_history_details)
    click.echo(f'\nParser history exported successfully to: {export_path}')

  if verbose:
    api_utility.print_request_details(history_url, method, None,
                                      parsed_response)


def get_last_live_time(parser_history: Dict[str, Any]) -> str:
  """Get last live time from API response.

  Args:
    parser_history: API response

  Returns:
    String if API response contains lastLiveTime key
  """
  last_live_time = parser_history.get(parser_constants.KEY_LAST_LIVE_TIME, '')
  if last_live_time:
    return f'\n  Last Live Time: {last_live_time}' + '{0}'.format(
        '\n' if parser_history.get(parser_constants.KEY_VALIDATION_ERRORS
                                  ) else '')
  return ''


def get_validation_errors(parser_history: Dict[str, Any]) -> str:
  """Get validation errors.

  Args:
    parser_history: API response containing validation error

  Returns:
    Formatted response to be displayed on console
  """
  error_response = []
  validation_errors = parser_history.get(parser_constants.KEY_VALIDATION_ERRORS,
                                         {})

  for index, error in enumerate(
      validation_errors.get(common_constants.KEY_ERRORS, [])):
    if error.get(common_constants.KEY_ERROR, ''):
      error_response.append(f'\n    Error:\n'
                            f'      {error.get(common_constants.KEY_ERROR)}')

    if error.get(parser_constants.KEY_LOG, ''):
      error_response.append(
          f'\n    Log:\n'
          f'      {parser_utility.decode_log(error.get(parser_constants.KEY_LOG))}'
      )

    if index != len(validation_errors.get(common_constants.KEY_ERRORS)) - 1:
      error_response.append(f"\n    {'-' * 56}")

  if error_response:
    return f'\n  Validation Errors:{"".join(error_response)}'
  return ''
