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
"""Run the parser against given logs."""

import base64
import time
from typing import AnyStr
import urllib

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import file_utility
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parser import url
from parser.constants import key_constants as parser_constants


@click.command(name='run', help='Run the parser against given logs')
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def run(credential_file: AnyStr, verbose: bool, region: str, env: str) -> None:
  """Run the parser against given logs.

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
  conf_file_path = click.prompt('Enter path for conf file')
  log_file_path = click.prompt('Enter path for log file')
  click.echo('Running Validation...')
  start_time = time.time()

  config_data = file_utility.read_file(conf_file_path)
  log_data = file_utility.read_file(log_file_path)

  data = urllib.parse.urlencode({
      parser_constants.KEY_CONFIG: base64.urlsafe_b64encode(config_data),
      parser_constants.KEY_LOGS: base64.urlsafe_b64encode(log_data)
  })

  run_parser_url = url.get_url(region, 'run', env)
  method = 'POST'
  client = chronicle_auth.initialize_http_session(credential_file)

  response = client.request(
      method,
      run_parser_url,
      data=data,
      headers=url.HTTP_REQUEST_HEADERS,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parser_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f'Error while running validation.\nResponse Code: {response.status_code}'
        f'\nError: {parser_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}'
    )
    return

  for result in parser_response.get(parser_constants.KEY_RESULT, []):
    click.echo(result)

  for err in parser_response.get(common_constants.KEY_ERRORS, []):
    click.echo(err[parser_constants.KEY_ERROR_MSG])
    click.echo(err[parser_constants.KEY_LOG_ENTRY])

  time_elapsed = time.time() - start_time
  click.echo('Runtime: {:.5}s'.format(time_elapsed))

  if verbose:
    api_utility.print_request_details(run_parser_url, method, None,
                                      parser_response)
