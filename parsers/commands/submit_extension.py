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
"""Submit a new parser extension."""

import base64
import os

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import file_utility
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parsers import parser_templates
from parsers import parser_utility
from parsers import url
from parsers.constants import key_constants as parser_constants


@click.command(name="submit_extension", help="[New]Submit a new extension")
@click.argument("project_id", required=True, default="")
@click.argument("customer_id", required=True, default="")
@click.argument("log_type", required=True, default="")
@click.argument("config_file", required=True, default="")
@click.argument("log_file", required=True, default="")
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@options.v2_option
@exception_handler.catch_exception()
def submit_extension(
    v2: bool,
    credential_file: str,
    verbose: bool,
    region: str,
    env: str,
    project_id: str,
    customer_id: str,
    log_type: str,
    config_file: str,
    log_file: str) -> None:
  """Submit a new parser extension.

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
    config_file (str): Path of parser extension config file.
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

  if not log_type:
    click.echo("Log Type not provided. Please enter Log Type")
    return

  if not os.path.exists(config_file):
    click.echo(f"{config_file} does not exist. "
               "Please enter valid config file path")
    return

  if not os.path.exists(log_file):
    click.echo(f"{log_file} does not exist. "
               "Please enter valid log file path")
    return

  click.echo("Submitting Parser Extension...")

  resources = {
      "project": project_id,
      "location": region.lower(),
      "instance": customer_id,
      "log_type": log_type
  }

  cbn_data = file_utility.read_file(config_file)
  log_data = file_utility.read_file(log_file)

  cbn_data = base64.urlsafe_b64encode(cbn_data).decode()
  log_data = base64.urlsafe_b64encode(log_data).decode()

  # Set Parser Extension details
  parser_extension = {
      parser_constants.KEY_INPUT_CBN_SNIPPET: cbn_data,
      parser_constants.KEY_LOG: log_data,
  }

  submit_extension_url = url.get_dataplane_url(
      region,
      "submit_extension",
      env,
      resources)
  method = "POST"
  client = chronicle_auth.initialize_dataplane_http_session(credential_file)
  response = client.request(method, submit_extension_url, json=parser_extension,
                            timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parsed_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while submitting parser extension.\n"
        f"Response Code: {response.status_code}\n"
        f"Error: "
        f"{parsed_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  if parser_constants.KEY_NAME not in parsed_response:
    click.echo("No ParserExtension currently configured.")
    return

  parserextension_details = ""
  try:
    # TODO(sathishbabu): Create a library to encompass the common
    # code for parser/extension.
    # Remove unwanted details
    parsed_response.pop(parser_constants.KEY_CBN_SNIPPET, None)
    parsed_response.pop(parser_constants.KEY_FIELD_EXTRACTORS, None)
    parsed_response.pop(parser_constants.KEY_LOG, None)
    parsed_response.pop(parser_constants.KEY_EXTENSION_VALIDATION_REPORT, None)

    # Get components from the resource name
    resource_components = parser_utility.process_resource_name(
        parsed_response[parser_constants.KEY_NAME])

    # Get Parser Extension details
    parserextension_id = (
        f"{resource_components[parser_constants.KEY_PARSER_EXTENSIONS]}")
    log_type = f"{resource_components[parser_constants.KEY_LOGTYPES]}"
    validation_report_id = "-"
    state = f"{parsed_response[parser_constants.KEY_STATE]}"
    author = f"{parsed_response.get(parser_constants.KEY_AUTHOR, '-')}"
    create_time = (
        f"{parsed_response.get(parser_constants.KEY_CREATE_TIME, '-')}")
    state_last_changed_time = f"{parsed_response.get(parser_constants.KEY_STATE_LAST_CHANGED_TIME, '-')}"  # pylint: disable=line-too-long
    last_live_time = (
        f"{parsed_response.get(parser_constants.KEY_LAST_LIVE_TIME, '-')}")

    # Populate the Parser Extension details
    parserextension_template = parser_templates.parserextension_details_template
    parserextension_details += parserextension_template.substitute(
        parserextension_id=parserextension_id,
        log_type=log_type,
        state=state,
        author=author,
        validation_report_id=validation_report_id,
        create_time=create_time,
        state_last_changed_time=state_last_changed_time,
        last_live_time=last_live_time
    )

  except KeyError as e:
    parserextension_details += f"\nKey {str(e)} not found in the response."
  except Exception as e:  # pylint: disable=broad-except
    parserextension_details += f"\nFailed with exception: {str(e)}"
  parserextension_details += f'\n\n{"=" * 60}\n'

  click.echo(parserextension_details)

  if verbose:
    api_utility.print_request_details(
        submit_extension_url, method, None, parsed_response)
