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
"""Download parser code given log type."""

import base64
import os
import pathlib
import time
from typing import AnyStr

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parser import url
from parser.constants import key_constants
from parser.constants import path_constants


@click.command(
    name="download", help="Download parser code given config ID or log type")
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def download(credential_file: AnyStr, verbose: bool, region: str,
             env: str) -> None:
  """Download parser code given log type or config ID.

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
  click.echo(
      "Note: If you want to download parser by log type then skip the config ID."
  )
  config_id = click.prompt("Enter config ID", show_default=False, default="")

  http_client = chronicle_auth.initialize_http_session(credential_file)
  method = "GET"

  if config_id:
    # Get the parser from config id
    download_parser_url = f'{url.get_url(region, "list", env)}/{config_id}'
    response = http_client.request(
        method, download_parser_url, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
    download_parser_response = api_utility.check_content_type(response.text)
  else:
    # Get the parser of `log_type` from list of parsers
    log_type = click.prompt("Enter Log Type", show_default=False, default="")
    if not log_type:
      click.echo("Please enter log type or config ID.")
      return
    download_parser_url = url.get_url(region, "list", env)
    response = http_client.request(
        method, download_parser_url, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
    download_parser_response = api_utility.check_content_type(response.text)
    if key_constants.KEY_CBN_PARSER not in download_parser_response:
      click.echo("No CBN parsers currently configured.")
      return
    found = False
    for p in download_parser_response[key_constants.KEY_CBN_PARSER]:
      if p[common_constants.KEY_LOG_TYPE] == log_type:
        found = True
        download_parser_response = p
        break
    if not found:
      click.echo(f"Parser for log type {log_type} not found.")
      return

  click.echo("Downloading parser...")

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while downloading parser:\nResponse Code: {response.status_code}"
        f"\nError: {download_parser_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  decoded_config = base64.b64decode(
      download_parser_response[key_constants.KEY_CONFIG])
  decoded_config = decoded_config.decode("utf-8")
  timestr = time.strftime("%Y%m%d%H%M%S")
  filename = download_parser_response[
      common_constants.KEY_LOG_TYPE] + "_" + timestr + ".conf"
  sample_dir = pathlib.Path(path_constants.PARSER_DATA_DIR)
  sample_dir.mkdir(parents=True, exist_ok=True)
  filepath = os.path.join(sample_dir, filename)
  click.echo(f"Writing parser to: {filepath}")
  with open(filepath, "w") as f:
    f.write(decoded_config)

  if verbose:
    api_utility.print_request_details(download_parser_url, method, None,
                                      download_parser_response)
