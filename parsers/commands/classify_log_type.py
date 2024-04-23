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
"""Classify the provided logs to the corresponding log types."""

import base64
import os

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parsers import url
from parsers.constants import key_constants as parser_constants


@click.command(
    name="classify_log_type",
    help="[New]Classify the provided logs to the log types.")
@click.argument("project_id", required=True, default="")
@click.argument("customer_id", required=True, default="")
@click.argument("log_file", required=True, default="")
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@options.v2_option
@exception_handler.catch_exception()
def classify_log_type(
    v2: bool,
    credential_file: str,
    verbose: bool,
    region: str,
    env: str,
    project_id: str,
    customer_id: str,
    log_file: str) -> None:
  """Classify the provided logs to the corresponding log types.

  Args:
    v2 (bool): Option for enabling v2 commands.
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    env (str): Option for selection environment. Available options - prod, test.
    project_id (str): The GCP Project ID.
    customer_id (str): The Customer ID.
    log_file (str): Path of log file containing a single log line.

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
    click.echo("Project ID not provided. Please enter Project ID")
    return

  if not customer_id:
    click.echo("Customer ID not provided. Please enter Customer ID")
    return

  if not os.path.exists(log_file):
    click.echo(f"{log_file} does not exist. "
               "Please enter valid log file path")
    return

  click.echo("Classifying the provided log to the corresponding log types...\n")

  resources = {
      "project": project_id,
      "location": region.lower(),
      "instance": customer_id
  }

  with open(log_file, "r") as f:
    log_lines = f.readlines()

  log_data = []
  for log_line in log_lines:
    log_line = log_line.strip(" \n")
    log_data.append(base64.b64encode(log_line.encode()).decode())

  data = {
      parser_constants.KEY_LOG_DATA: log_data,
  }

  classify_log_type_url = url.get_dataplane_url(
      region,
      "classify_log_type",
      env,
      resources)
  client = chronicle_auth.initialize_dataplane_http_session(credential_file)
  method = "POST"
  response = client.request(
      method, classify_log_type_url,
      json=data, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parsed_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while classifying the logs.\n"
        f"Response Code: {response.status_code}\n"
        f"Error: "
        f"{parsed_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  if parser_constants.KEY_PREDICTIONS not in parsed_response:
    click.echo("No predictions found in the response.")
    return

  results = parsed_response.get(parser_constants.KEY_PREDICTIONS, [])
  for result in results:
    # Handle log type and score
    log_type = result[parser_constants.KEY_LOGTYPE]
    score = result[parser_constants.KEY_SCORE]
    click.echo(f"Log Type: {log_type} , Score: {score}")

  if verbose:
    api_utility.print_request_details(
        classify_log_type_url, method, None, parsed_response)
