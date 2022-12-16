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
"""List all collectors for the customer."""
import os
from typing import Any, AnyStr, Dict, List

import click

from common import api_utility
from common import chronicle_auth
from common import commands_utility
from common import exception_handler
from common import file_utility
from common import options
from forwarders import forwarder_utility
from forwarders.collectors import collector_utility
from forwarders.commands.list import get_collector_csv_rows
from forwarders.constants import schema


@click.command(name="list", help="List all collectors.")
@options.url_option
@options.region_option
@options.verbose_option
@options.export_option
@click.option(
    "--file-format",
    type=click.Choice(["TXT", "CSV", "JSON"], case_sensitive=False),
    default="CSV",
    help="Format of the file to be exported")
@options.credential_file_option
@exception_handler.catch_exception()
def list_command(credential_file: AnyStr, verbose: bool, file_format: AnyStr,
                 export: AnyStr, region: str, url: str) -> None:
  """List all associated collectors for the customer.

  Args:
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    file_format (AnyStr): Format of the content to be exported.
    export (AnyStr): Path of file to export output of list command.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    url (str): Base URL to be used for API calls.

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  forwarder_id = click.prompt(
      "Enter Forwarder ID", default="", show_default=False)
  if not forwarder_id:
    click.echo("Forwarder ID not provided. Please enter Forwarder ID.")
    return

  url = commands_utility.lower_or_none(url)
  client = chronicle_auth.initialize_http_session(credential_file)
  collector_url = collector_utility.get_collector_url(region, url, forwarder_id)
  method = "GET"

  # Fetch collectors for respective forwarder_id.
  collectors_api_response, collectors = collector_utility.fetch_collectors(
      collector_url, method, client)

  if "error" not in collectors[
      schema.KEY_COLLECTORS] and collectors_api_response.get(
          schema.KEY_COLLECTORS):

    collectors = collectors_api_response[schema.KEY_COLLECTORS]
    final_json_response, collector_rows = list_collectors(export, collectors)

    if export:
      export_data(export, file_format, final_json_response, collector_rows)

    if verbose:
      api_utility.print_request_details(collector_url, method, None,
                                        collectors_api_response)
      for collector_response in collectors:
        api_utility.print_request_details(collector_url, method, None,
                                          collector_response)
  else:
    click.echo(
        commands_utility.convert_dict_to_yaml(
            commands_utility.convert_dict_keys_to_human_readable(collectors)))


def list_collectors(
    export: AnyStr,
    collectors: List[Dict[str, Any]],
) -> Any:
  """List all Collectors of this Forwarder Id.

  Args:
    export (AnyStr): Path of file to export output of list command.
    collectors (List[Dict[str, Any]]): List of collectors.

  Returns:
    Any:
      final_json_response - Contains collectors and collectors response.
      collector_rows - List of collector rows for CSV export.
  """
  collector_rows = []
  final_json_response = {}
  final_json_response[schema.KEY_COLLECTORS] = []

  for collector in collectors:

    collector.update(
        {schema.KEY_NAME: forwarder_utility.get_resource_id(collector)})
    collector_details = commands_utility.convert_dict_keys_to_human_readable(
        forwarder_utility.change_dict_keys_order(collector))

    display_output = {}
    # Capitalize keyword ID to display output on console.
    if collector_details.get(schema.KEY_ID.capitalize()):
      display_output[schema.KEY_ID] = collector_details.pop(
          schema.KEY_ID.capitalize())
    display_output.update(collector_details)

    click.echo("\nCollector Details:\n")
    click.echo(commands_utility.convert_dict_to_yaml(display_output))
    click.echo(f"{forwarder_utility.PRINT_SEPARATOR}")

    if export:
      # Export collector rows without forwarder ID
      # since forwarder ID is same for all its associated collectors.
      collector_rows.append((get_collector_csv_rows({}, collector))[1:])

    final_json_response[schema.KEY_COLLECTORS].append(collector)

  return final_json_response, collector_rows


def export_data(export: str, file_format: str, json_response: Dict[str, Any],
                collector_rows: List[List[str]]) -> None:
  """Exports data into csv, json, text format.

  Args:
    export (str): Path of file to export output of list command.
    file_format (str): Format of the content to be exported. Supported formats:
      CSV, JSON, TXT
    json_response (Dict[str, Any]): JSON response including all collectors.
    collector_rows (List[List[str]]): List of rows export into csv.
  """
  export_path = os.path.abspath(export) + f".{file_format.lower()}"
  if (file_format == file_utility.FILE_FORMAT_JSON) and (json_response.get(
      schema.KEY_COLLECTORS)):
    file_utility.export_json(export_path, json_response)

  elif file_format == file_utility.FILE_FORMAT_CSV:
    file_utility.export_csv(export_path, schema.COLLECTOR_COLUMN_HEADER[1:],
                            collector_rows)

  elif file_format == file_utility.FILE_FORMAT_TXT:
    forwarder_utility.export_txt(export_path, json_response)
  click.echo(
      f"\nCollectors list details exported successfully to: {export_path}")
