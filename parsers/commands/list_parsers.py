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
"""List all parsers for a given customer."""

import os
from typing import Dict

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

ALL_STATE = "ALL"
STATE_LIST = [ALL_STATE, "ACTIVE", "INACTIVE"]
TYPE = "CUSTOM"


@click.command(name="list_parsers",
               help="[New]List all parsers for a given customer")
@click.option(
    "-s",
    "--state",
    type=click.Choice(STATE_LIST, case_sensitive=False),
    default=STATE_LIST[0],
    help="Filter on Parser State",
    required=False
)
@click.option(
    "-f",
    "--file-format",
    type=click.Choice(["TXT", "JSON"], case_sensitive=False),
    default="TXT",
    help="Format of the file to be exported")
@click.argument("project_id", required=True, default="")
@click.argument("customer_id", required=True, default="")
@click.argument("log_type", required=True, default="-")
@options.export_option
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@options.v2_option
@exception_handler.catch_exception()
def list_parsers(
    v2: bool,
    credential_file: str,
    verbose: bool,
    region: str,
    env: str,
    export: str,
    project_id: str,
    customer_id: str,
    log_type: str,
    state: str,
    file_format: str) -> None:
  """List all parsers of a given customer.

  Args:
    v2 (bool): Option for enabling v2 commands.
    credential_file (str): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    env (str): Option for selecting environment. Available options - prod, test.
    export (str): Path of file to export output of list command.
    project_id (str): The GCP Project ID.
    customer_id (str): The Customer ID.
    log_type (str): The Log Type.
    state (str): Option for selecting states. Available options - ALL, ACTIVE,
      INACTIVE.
    file_format (str): Options for selecting the format of the content to be
      exported. Availabel options - TXT, JSON.

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

  click.echo("Fetching list of parsers...")

  # Set resources
  resources = {
      "project": project_id,
      "location": region.lower(),
      "instance": customer_id,
      "log_type": log_type,
  }
  # Set filter
  filter_options = {"TYPE": TYPE}
  if state != ALL_STATE:
    filter_options["STATE"] = state

  list_parser_url = url.get_dataplane_url(
      region,
      "list_parsers",
      env,
      resources,
      filter=construct_filter(filter_options),
      page_size=1000)
  client = chronicle_auth.initialize_dataplane_http_session(credential_file)
  method = "GET"
  response = client.request(
      method, list_parser_url, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parsed_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while fetching list of parsers.\n"
        f"Response Code: {response.status_code}\n"
        f"Error: "
        f"{parsed_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  if parser_constants.KEY_PARSERS not in parsed_response:
    click.echo("No Parsers currently configured.")
    return

  parser_details = ""
  parser_details_json = []
  for parser in parsed_response[parser_constants.KEY_PARSERS]:
    try:
      # Remove unwanted details
      parser.pop(parser_constants.KEY_CBN, None)
      parser.pop(parser_constants.KEY_CHANGELOGS, None)
      parser.pop(parser_constants.KEY_LOW_CODE, None)

      # Get components from the resource name
      resource_components = parser_utility.process_resource_name(
          parser[parser_constants.KEY_NAME])

      validation_report_id = "-"
      if parser_constants.KEY_VALIDATION_REPORT in parser:
        # Get components from the validation resource
        validation_components = parser_utility.process_resource_name(
            parser[parser_constants.KEY_VALIDATION_REPORT])
        validation_report_id = (
            f"{validation_components[parser_constants.KEY_VALIDATION_REPORTS]}")

      # Get Parser details
      parser_id = f"{resource_components[parser_constants.KEY_PARSERS]}"
      log_type = f"{resource_components[parser_constants.KEY_LOGTYPES]}"
      state = f"{parser[parser_constants.KEY_STATE]}"
      parser_type = f"{parser[parser_constants.KEY_TYPE]}"
      create_time = f"{parser.get(parser_constants.KEY_CREATE_TIME, '-')}"
      # Get author name
      creator = parser[parser_constants.KEY_CREATOR]
      author = "-"
      if parser_constants.KEY_AUTHOR in creator:
        author = f"{creator[parser_constants.KEY_AUTHOR]}"

      # Populate the parser details
      parser_details += parser_templates.parserv2_details_template.substitute(
          parser_id=parser_id,
          log_type=log_type,
          state=state,
          type=parser_type,
          author=author,
          validation_report_id=validation_report_id,
          create_time=create_time,
      )

      # Populate the parser details in JSON for export if needed
      parser_details_json.append({
          parser_constants.KEY_PARSER_ID: parser_id,
          parser_constants.KEY_LOGTYPE: log_type,
          parser_constants.KEY_STATE: state,
          parser_constants.KEY_TYPE: parser_type,
          parser_constants.KEY_AUTHOR: author,
          parser_constants.KEY_VALIDATION_REPORT_ID: validation_report_id,
          parser_constants.KEY_CREATE_TIME: create_time,
      })
    except KeyError as e:
      parser_details += f"\nKey {str(e)} not found in the response."
    except Exception as e:  # pylint: disable=broad-except
      parser_details += f"\nFailed with exception: {str(e)}"
    parser_details += f'\n\n{"=" * 60}\n'

  click.echo(parser_details)

  if export:
    export_path = os.path.abspath(export) + f".{file_format.lower()}"
    if file_format == file_utility.FILE_FORMAT_JSON:
      file_utility.export_json(export_path, {"parsers": parser_details_json})
    else:
      file_utility.export_txt(export_path, parser_details)
    click.echo(f"\nParser details exported successfully to: {export_path}")

  if verbose:
    api_utility.print_request_details(
        list_parser_url, method, None, parsed_response)


def construct_filter(filter_options: Dict[str, str]) -> str:
  """Construct filter for Parsers API.

  Args:
    filter_options (Dict): Filter options

  Returns:
    str: Filter query.
  """
  filters = []
  for k, v in filter_options.items():
    filters.append(f"{k} = {v}")
  return " AND ".join(filters)
