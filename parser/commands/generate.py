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
"""Generate sample logs for a given log type."""

import pathlib
from typing import AnyStr

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parser import parser_utility
from parser import url
from parser.constants import key_constants
from parser.constants import path_constants


@click.command(
    name='generate', help='Generate sample logs for a given log type')
@options.env_option
@options.region_option
@options.credential_file_option
@exception_handler.catch_exception()
def generate(credential_file: AnyStr, region: str, env: str) -> None:
  """Generates sample data for writing parsers.

  Args:
    credential_file (AnyStr): Path of Service Account JSON.
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
  sample_sizes = ['1', '10', '1000']
  sample_names = ['1', '10', '1k']

  start_date = click.prompt(
      'Enter Start Date (Format: yyyy-mm-ddThh:mm:ssZ)',
      default='',
      show_default=False)
  end_date = click.prompt(
      'Enter End Date (Format: yyyy-mm-ddThh:mm:ssZ)',
      default='',
      show_default=False)
  log_type = click.prompt('Enter Log Type', default='', show_default=False)

  if (not start_date) or (not end_date) or (not log_type):
    click.echo(
        'Start Date, End Date and Log Type are required. Please enter value for the missing field(s).'
    )
    return

  # Verify directory structure exists or create it.
  sample_dir = pathlib.Path(
      f'{path_constants.PARSER_DATA_DIR}/{log_type.lower()}')
  sample_dir.mkdir(parents=True, exist_ok=True)

  # Generate sample data of given sizes.
  for i, size in enumerate(sample_sizes):
    outfile = f'{sample_dir}/{log_type.lower()}_{sample_names[i]}.log'
    click.echo('\nGenerating sample size: {}... '.format(sample_names[i]),)
    call_get_sample_logs(credential_file, region, env, log_type.upper(),
                         start_date, end_date, int(size), outfile)

  click.echo(
      f'\nGenerated sample data ({log_type.upper()}); run this to go there:')
  click.echo(f'cd {sample_dir}')


def call_get_sample_logs(credential_file: str, region: str, env: str,
                         log_type: str, start_time: str, end_time: str,
                         number_of_entries: int, file_path: str) -> None:
  """Calls get sample logs endpoint and writes response to file."""
  data = {
      key_constants.KEY_LOG_TYPE: log_type,
      key_constants.KEY_START_TIME: start_time,
      key_constants.KEY_END_TIME: end_time,
      key_constants.KEY_MAX_ENTRIES: number_of_entries,
  }
  get_sample_log_url = f"{url.get_url(region, 'generate', env)}"

  # Make the request.
  client = chronicle_auth.initialize_http_session(credential_file)
  response = client.request(
      'POST', get_sample_log_url, data, headers=url.HTTP_REQUEST_HEADERS)
  sample_logs = api_utility.check_content_type(response.text)
  if response.status_code != status.STATUS_OK:
    click.echo(
        f'Error while fetching status for parser.\nResponse Code: {response.status_code}'
        f'\nError: {sample_logs[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}'
    )
    return

  # Parse the response.
  sample_logs_data = sample_logs.get(key_constants.KEY_DATA, [])
  with open(file_path, 'w') as f:
    for sample_log in sample_logs_data:
      f.write(parser_utility.decode_log(sample_log))
      f.write('\n')
