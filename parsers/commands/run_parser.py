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
"""Run a parser(with extension) against given logs."""

import base64
import os
import time

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import file_utility
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parsers import url
from parsers.constants import key_constants as parser_constants


@click.command(name="run_parser",
               help="[New]Run a parser(with extension) against given logs")
@click.option(
    "--parserextension_config_file",
    help="Path of parser extension config file",
)
@click.argument("project_id", required=True, default="")
@click.argument("customer_id", required=True, default="")
@click.argument("log_type", required=True, default="")
@click.argument("parser_config_file", required=True, default="")
@click.argument("log_file", required=True, default="")
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@options.v2_option
@exception_handler.catch_exception()
def run_parser(
    v2: bool,
    credential_file: str,
    verbose: bool,
    region: str,
    env: str,
    project_id: str,
    customer_id: str,
    log_type: str,
    parser_config_file: str,
    log_file: str,
    parserextension_config_file: str) -> None:
  """Run a parser(with extension) against given logs.

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
    parser_config_file (str): Path of parser config file.
    log_file (str): Path of log file containing a single log line.
    parserextension_config_file (str): Path of parser extension config file.

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
    click.echo("Project ID not provided. Please enter Porject ID")
    return

  if not customer_id:
    click.echo("Customer ID not provided. Please enter Customer ID")
    return

  if not log_type:
    click.echo("Log Type not provided. Please enter Log Type")
    return

  if not os.path.exists(parser_config_file):
    click.echo(f"{parser_config_file} does not exist. "
               "Please enter valid parser config file path")
    return

  if not os.path.exists(log_file):
    click.echo(f"{log_file} does not exist. "
               "Please enter valid log file path")
    return

  if (parserextension_config_file and
      not os.path.exists(parserextension_config_file)):
    click.echo(f"{parserextension_config_file} does not exist. "
               "Please enter valid parser extension config file path")
    return

  click.echo("Running parser(with extension) against given logs...\n")
  start_time = time.time()

  resources = {
      "project": project_id,
      "location": region.lower(),
      "instance": customer_id,
      "log_type": log_type
  }

  parser_config_data = file_utility.read_file(parser_config_file)
  parser_config_data = base64.urlsafe_b64encode(parser_config_data).decode()

  with open(log_file, "r") as f:
    log_lines = f.readlines()

  log_data = []
  for log_line in log_lines:
    log_line = log_line.strip(" \n")
    log_data.append(base64.urlsafe_b64encode(log_line.encode()).decode())

  parser_extension_config_data = b""
  if parserextension_config_file:
    with open(parserextension_config_file, "rb") as f:
      parser_extension_config_data = f.read()
  parser_extension_config_data = base64.urlsafe_b64encode(
      parser_extension_config_data).decode()

  data = {
      parser_constants.KEY_PARSER: {
          parser_constants.KEY_CBN: parser_config_data
      },
      parser_constants.KEY_LOG: log_data
  }
  if parser_extension_config_data:
    data[parser_constants.KEY_PARSER_EXTENSION] = {
        parser_constants.KEY_CBN_SNIPPET: parser_extension_config_data
    }

  run_parser_url = url.get_dataplane_url(region, "run_parser", env, resources)
  method = "POST"
  client = chronicle_auth.initialize_dataplane_http_session(credential_file)
  response = client.request(method, run_parser_url, json=data,
                            timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parsed_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while running parser(with extension).\n"
        f"Response Code: {response.status_code}\n"
        f"Error: "
        f"{parsed_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  if parser_constants.KEY_RUN_PARSER_RESULTS not in parsed_response:
    click.echo("Parser yielded no results.")
    return

  results = parsed_response.get(parser_constants.KEY_RUN_PARSER_RESULTS, [])
  for result in results:
    # Handle error if present
    if parser_constants.KEY_ERROR in result:
      error = result[parser_constants.KEY_ERROR]
      click.echo(error[parser_constants.KEY_MESSAGE])
      continue
    # Handle parsed events
    log = result[parser_constants.KEY_LOG]
    log = base64.urlsafe_b64decode(log).decode()
    click.echo(f"Log: {log}")
    click.echo(f"Events: {result[parser_constants.KEY_PARSED_EVENTS]}")

  time_elapsed = time.time() - start_time
  click.echo(f"\nRuntime: {time_elapsed:.5}s")

  if verbose:
    api_utility.print_request_details(
        run_parser_url, method, None, parsed_response)

