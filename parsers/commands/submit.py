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
"""Submit a new parser."""

import base64
import os
from typing import AnyStr
import urllib

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


@click.command(name='submit', help='Submit a new parser')
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def submit(credential_file: AnyStr, verbose: bool, region: str,
           env: str) -> None:
  """Submit a new parser.

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
  log_type = click.prompt('Enter Log type', show_default=False, default='')
  conf_file = click.prompt(
      'Enter Config file path', show_default=False, default='')
  author = click.prompt('Enter author', show_default=False, default='')

  if (not log_type) or (not conf_file) or (not author):
    click.echo('Log Type, Config file path and Author fields are required. '
               'Please enter value for the missing field(s).')
    return

  if not os.path.exists(conf_file):
    click.echo(
        f'{conf_file} does not exist. Please enter valid config file path.')
    return

  with open(conf_file, 'rb') as config_file:
    config_data = config_file.read()

  data = {
      parser_constants.KEY_LOG_TYPE: log_type,
      parser_constants.KEY_CONFIG: base64.urlsafe_b64encode(config_data),
      parser_constants.KEY_AUTHOR: author
  }

  click.echo('Submitting parser...')

  request_body = urllib.parse.urlencode(data)
  submit_parser_url = url.get_url(region, 'list', env)
  client = chronicle_auth.initialize_http_session(credential_file)
  method = 'POST'
  response = client.request(
      method,
      submit_parser_url,
      request_body,
      headers=url.HTTP_REQUEST_HEADERS,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parser = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f'Error while submitting parser:\nResponse Code: {response.status_code}'
        f'\nError: {parser[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}'
    )
    return

  del parser[parser_constants.KEY_CONFIG]

  parser_details = parser_templates.submitted_parser_details_template.substitute(
      config_id=f'{parser[parser_constants.KEY_CONFIG_ID]}',
      log_type=f'{parser[common_constants.KEY_LOG_TYPE]}',
      submit_time=f'{parser[parser_constants.KEY_SUBMIT_TIME]}',
      state_last_changed_time=f'{parser[parser_constants.KEY_STATE_LAST_CHANGED_TIME]}',
      state=f'{parser[parser_constants.KEY_STATE]}',
      sha256=f'{parser[parser_constants.KEY_SHA256]}',
      author=f'{parser[parser_constants.KEY_AUTHOR]}')
  click.echo(parser_details)

  click.echo(
      '\nParser submitted successfully. To get status of the parser, run this '
      f'command using following Config ID - {parser[parser_constants.KEY_CONFIG_ID]}:'
  )
  click.echo('`chronicle_cli parsers status`')

  if verbose:
    api_utility.print_request_details(submit_parser_url, method, None, parser)
