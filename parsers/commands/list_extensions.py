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
"""List all parser extensions for a given customer."""

import os

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import file_utility
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from parsers import parser_templates as templates
from parsers import parser_utility
from parsers import url
from parsers.constants import key_constants as parser_constants


@click.command(name="list_extensions",
               help="[New]List all extensions for a given customer")
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
def list_extensions(
    v2: bool,
    credential_file: str,
    verbose: bool,
    region: str,
    env: str,
    export: str,
    project_id: str,
    customer_id: str,
    log_type: str,
    file_format: str) -> None:
  """List all parser extensions for a given customer.

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
    file_format (str): Format of the content to be exported.

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

  click.echo("Fetching list of Parser Extensions...")

  resources = {
      "project": project_id,
      "location": region.lower(),
      "instance": customer_id,
      "log_type": log_type,
  }

  list_extensions_url = url.get_dataplane_url(
      region,
      "list_extensions",
      env,
      resources)
  client = chronicle_auth.initialize_dataplane_http_session(credential_file)
  method = "GET"
  response = client.request(
      method, list_extensions_url, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parsed_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while fetching list of Parser Extensions.\n"
        f"Response Code: {response.status_code}\n"
        f"Error: "
        f"{parsed_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  if parser_constants.KEY_PARSER_EXTENSIONS not in parsed_response:
    click.echo("No Parser Extensions currently configured.")
    return

  parserextension_details = ""
  parserextension_details_json = []
  for extension in parsed_response[parser_constants.KEY_PARSER_EXTENSIONS]:
    try:
      # Remove unwanted details
      extension.pop(parser_constants.KEY_CBN_SNIPPET, None)
      extension.pop(parser_constants.KEY_FIELD_EXTRACTORS, None)
      extension.pop(parser_constants.KEY_LOG, None)
      extension.pop(parser_constants.KEY_EXTENSION_VALIDATION_REPORT, None)

      # Get components from the resource name
      resource_components = parser_utility.process_resource_name(
          extension[parser_constants.KEY_NAME])

      validation_report_id = "-"
      if parser_constants.KEY_VALIDATION_REPORT in extension:
        # Get components from the validation resource
        validation_components = parser_utility.process_resource_name(
            extension[parser_constants.KEY_VALIDATION_REPORT])
        validation_report_id = (
            f"{validation_components[parser_constants.KEY_VALIDATION_REPORTS]}")

      # Get Parser Extension details
      parserextension_id = (
          f"{resource_components[parser_constants.KEY_PARSER_EXTENSIONS]}")
      log_type = f"{resource_components[parser_constants.KEY_LOGTYPES]}"
      state = f"{extension[parser_constants.KEY_STATE]}"
      author = f"{extension.get(parser_constants.KEY_AUTHOR, '-')}"
      create_time = f"{extension.get(parser_constants.KEY_CREATE_TIME, '-')}"
      state_last_changed_time = (
          f"{extension.get(parser_constants.KEY_STATE_LAST_CHANGED_TIME, '-')}")
      last_live_time = (
          f"{extension.get(parser_constants.KEY_LAST_LIVE_TIME, '-')}")

      # Populate the extension details
      parserextension_template = templates.parserextension_details_template
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

      # Popluate the extension details in JSON for export if needed
      parserextension_details_json.append({
          parser_constants.KEY_PARSER_EXTENSION_ID: parserextension_id,
          parser_constants.KEY_LOGTYPE: log_type,
          parser_constants.KEY_STATE: state,
          parser_constants.KEY_AUTHOR: author,
          parser_constants.KEY_VALIDATION_REPORT_ID: validation_report_id,
          parser_constants.KEY_CREATE_TIME: create_time,
          parser_constants.KEY_STATE_LAST_CHANGED_TIME: state_last_changed_time,
          parser_constants.KEY_LAST_LIVE_TIME: last_live_time
      })
    except KeyError as e:
      parserextension_details += f"\nKey {str(e)} not found in the response."
    except Exception as e:  # pylint: disable=broad-except
      parserextension_details += f"\nFailed with exception: {str(e)}"
    parserextension_details += f'\n\n{"=" * 60}\n'

  click.echo(parserextension_details)

  if export:
    export_path = os.path.abspath(export) + f".{file_format.lower()}"
    if file_format == file_utility.FILE_FORMAT_JSON:
      file_utility.export_json(
          export_path, {"parserExtensions": parserextension_details_json})
    else:
      file_utility.export_txt(export_path, parserextension_details)
    click.echo(f"\nParser Extensions' details exported successfully to: "
               f"{export_path}")

  if verbose:
    api_utility.print_request_details(
        list_extensions_url, method, None, parsed_response)
