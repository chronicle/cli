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
"""List all forwarders for the customer."""
import copy
import dataclasses
import os
from typing import Any, AnyStr, Dict, List

import click

from common import api_utility
from common import chronicle_auth
from common import commands_utility
from common import exception_handler
from common import file_utility
from common import options
from common.constants import key_constants
from common.constants import status
from forwarders import collector_utility
from forwarders import forwarder_utility
from forwarders.constants import schema


@click.command(name="list", help="List all forwarders")
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
  """List all forwarders and its associated collectors for the customer.

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
  click.echo("Fetching list of forwarders...")
  url = commands_utility.lower_or_none(url)
  client = chronicle_auth.initialize_http_session(credential_file)
  forwarder_url = forwarder_utility.get_forwarder_url(region, url)
  method = "GET"
  list_forwarders_response = client.request(method, forwarder_url)

  forwarders_response = api_utility.check_content_type(
      list_forwarders_response.text)
  status_code = list_forwarders_response.status_code

  if status_code != status.STATUS_OK:
    error_message = forwarders_response[key_constants.KEY_ERROR][
        key_constants.KEY_MESSAGE]
    click.echo(
        f"\nError while fetching list of forwarders.\nResponse Code: {status_code}"
        f"\nError: {error_message}")
    return

  if not forwarders_response:
    click.echo("No forwarders found.")
    return

  # List of forwarders.
  forwarders = copy.deepcopy(forwarders_response[schema.KEY_FORWARDERS])

  collector_verbose_list, final_json_response, collector_rows, forwarder_rows = list_forwarders_and_associated_collectors(
      export, region, url, client, forwarders, method)

  if export:
    export_data(export, file_format, final_json_response, forwarder_rows,
                collector_rows)
  if verbose:
    api_utility.print_request_details(forwarder_url, method, None,
                                      forwarders_response)
    for verbose_data in collector_verbose_list:
      api_utility.print_request_details(
          getattr(verbose_data, "url"), method, None,
          getattr(verbose_data, "response"))


@dataclasses.dataclass
class Verbose:
  """Verbose dataclass."""
  url: str
  response: Any


def list_forwarders_and_associated_collectors(export: AnyStr, region: str,
                                              url: str, client: Any,
                                              forwarders: List[Dict[str, Any]],
                                              method: str) -> Any:
  """List all forwarders and its associated collectors for the customer.

  Args:
    export (AnyStr): Path of file to export output of list command.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    url (str): Base URL to be used for API calls.
    client (Any): HTTP session object to send authorized requests and receive
      responses.
    forwarders (List[Dict[str, Any]]): List of forwarders.
    method (str): Method to be used for API calls.

  Returns:
    Any:
      collector_verbose_list - Contains list of Verbose object with
      collector request url and method for verbose output
  """
  collector_verbose_list = []
  forwarder_rows = []
  collector_rows = []

  # Contains forwarder and collector response.
  final_json_response = {}
  final_json_response[schema.KEY_FORWARDERS] = []
  for forwarder in forwarders:

    forwarder_id = forwarder_utility.get_resource_id(forwarder)
    forwarder.update({schema.KEY_NAME: forwarder_id})
    collector_url = collector_utility.get_collector_url(region, url,
                                                        forwarder_id)

    # Fetch collectors for respective forwarders.
    collectors_api_response, collectors = collector_utility.fetch_collectors(
        collector_url, method, client)

    # Store URL and API response for each collector to
    # print verbose on console later.
    collector_verbose_list.append(
        Verbose(collector_url, collectors_api_response))

    for collector in collectors_api_response.get(schema.KEY_COLLECTORS, []):

      if "error" not in collector:

        # Converts list of collectors to nested dictionary object with key name
        # "Collector [<collector_uuid>]" for easy readability in yaml output.
        # Example-{"collectors":{"Collector [<collector_uuid>]":{"name":""}}}
        collector_id = forwarder_utility.get_resource_id(collector)
        collector.update({schema.KEY_NAME: collector_id})

        collectors[schema.KEY_COLLECTORS][
            f"Collector [{collector_id}]"] = forwarder_utility.change_dict_keys_order(
                collector)
        if export:
          collector_rows.append(get_collector_csv_rows(forwarder, collector))

    click.echo("\nForwarder Details:\n")
    click.echo(
        commands_utility.convert_dict_to_yaml(
            commands_utility.convert_dict_keys_to_human_readable(
                forwarder_utility.change_dict_keys_order(forwarder))))
    click.echo(
        commands_utility.convert_dict_to_yaml(
            commands_utility.convert_dict_keys_to_human_readable(collectors)))
    click.echo(f"{forwarder_utility.PRINT_SEPARATOR}")

    forwarder[schema.KEY_COLLECTORS] = collectors[schema.KEY_COLLECTORS]
    final_json_response[schema.KEY_FORWARDERS].append(forwarder)

    if export:
      forwarder_rows.append(get_forwarder_csv_rows(forwarder))

  return collector_verbose_list, final_json_response, collector_rows, forwarder_rows


def export_data(export_path: str, file_format: str,
                json_response: Dict[str, Any], forwarder_rows: List[List[str]],
                collector_rows: List[List[str]]) -> None:
  """Exports data into csv, json, text format.

  Args:
    export_path (str): Path of file to export output of list command.
    file_format (str): Format of the content to be exported. Supported formats:
      CSV, JSON, TXT
    json_response (Dict[str, Any]): Json response including all forwarders and
      collectors.
    forwarder_rows (List[List[str]]): List of rows export into csv.
    collector_rows (List[List[str]]): List of rows export into csv.
  """
  export_path = os.path.abspath(export_path) + f".{file_format.lower()}"

  if (file_format == file_utility.FILE_FORMAT_JSON) and (json_response.get(
      schema.KEY_FORWARDERS)):
    file_utility.export_json(export_path, json_response)
  elif file_format == file_utility.FILE_FORMAT_CSV:
    # Since we need two distinct files for forwarders and collectors and
    # the export path already contains the file format extension,
    # we must slice the export path in order to change the filename.
    export_path_forwarder = f"{export_path[:-4]}_{schema.KEY_FORWARDERS}.{file_format.lower()}"
    export_path_collectors = f"{export_path[:-4]}_{schema.KEY_COLLECTORS}.{file_format.lower()}"

    if forwarder_rows:
      file_utility.export_csv(export_path_forwarder,
                              schema.FORWARDER_COLUMN_HEADER, forwarder_rows)
    if collector_rows:
      file_utility.export_csv(export_path_collectors,
                              schema.COLLECTOR_COLUMN_HEADER, collector_rows)

    export_path = f"{export_path_forwarder} and {export_path_collectors}"
  elif file_format == file_utility.FILE_FORMAT_TXT:
    forwarder_utility.export_txt(export_path, json_response)
  click.echo(
      f"\nForwarders list details exported successfully to: {export_path}")


def get_forwarder_csv_rows(forwarder: Dict[str, Any]) -> List[Any]:
  """Gets list of rows for forwarder.

  Args:
    forwarder: Forwarder dictionary with all required keys.

  Returns:
    List of rows for forwarders.
  """

  config = forwarder.get(schema.KEY_CONFIG, {})
  server_settings = config.get(schema.KEY_SERVER_SETTINGS, {})
  http_settings = server_settings.get(schema.KEY_HTTP_SETTINGS, {})

  return [
      forwarder.get(schema.KEY_NAME, ""),
      forwarder.get(schema.KEY_DISPLAY_NAME, ""),
      forwarder.get(schema.KEY_STATE, ""),
      config.get(schema.KEY_UPLOAD_COMPRESSION, ""),
      (config.get(schema.KEY_METADATA, {})).get(schema.KEY_ASSET_NAMESPACE),
      forwarder_utility.get_labels_str(config.get(schema.KEY_METADATA, {})),
      forwarder_utility.get_regex_filters_str(
          config.get(schema.KEY_REGEX_FILTER, "")),
      server_settings.get(schema.KEY_STATE, ""),
      server_settings.get(schema.KEY_GRACEFUL_TIMEOUT, ""),
      server_settings.get(schema.KEY_DRAIN_TIMEOUT, ""),
      http_settings.get(schema.KEY_PORT),
      http_settings.get(schema.KEY_HOST),
      http_settings.get(schema.KEY_READ_TIMEOUT),
      http_settings.get(schema.KEY_READ_HEADER_TIMEOUT),
      http_settings.get(schema.KEY_WRITE_TIMEOUT),
      http_settings.get(schema.KEY_IDLE_TIMEOUT),
      (http_settings.get(schema.KEY_ROUTE_SETTINGS,
                         {})).get(schema.KEY_AVAILABLE_STATUS_CODE, 0),
      (http_settings.get(schema.KEY_ROUTE_SETTINGS,
                         {})).get(schema.KEY_READY_STATUS_CODE, 0),
      (http_settings.get(schema.KEY_ROUTE_SETTINGS,
                         {})).get(schema.KEY_UNREADY_STATUS_CODE, 0)
  ]


def get_collector_csv_rows(forwarder: Dict[str, Any],
                           collector: Dict[str, Any]) -> List[Any]:
  """Gets list of rows for collector.

  Args:
    forwarder: Forwarder dictionary with all required keys.
    collector: Collector dictionary with all required keys.

  Returns:
    List of rows for collector.
  """
  config = collector.get(schema.KEY_CONFIG, {})
  kafka_settings = config.get(schema.KEY_KAFKA_SETTINGS, {})
  pcap_settings = config.get(schema.KEY_PCAP_SETTINGS, {})
  splunk_settings = config.get(schema.KEY_SPLUNK_SETTINGS, {})
  syslog_settings = config.get(schema.KEY_SYSLOG_SETTINGS, {})

  return [
      forwarder.get(schema.KEY_NAME, ""),
      collector.get(schema.KEY_NAME, ""),
      collector.get(schema.KEY_DISPLAY_NAME, ""),
      collector.get(schema.KEY_STATE, ""),
      config.get(schema.KEY_LOG_TYPE, ""),
      config.get(schema.KEY_MAX_SECONDS_PER_BATCH, 0),
      config.get(schema.KEY_MAX_BYTES_PER_BATCH, 0),
      (config.get(schema.KEY_METADATA, {})).get(schema.KEY_ASSET_NAMESPACE, ""),
      forwarder_utility.get_labels_str(config.get(schema.KEY_METADATA, {})),
      forwarder_utility.get_regex_filters_str(
          config.get(schema.KEY_REGEX_FILTER, [])),
      (config.get(schema.KEY_DISK_BUFFER, {})).get(schema.KEY_STATE, ""),
      (config.get(schema.KEY_DISK_BUFFER, {})).get(schema.KEY_DIRECTORY_PATH,
                                                   ""),
      (config.get(schema.KEY_DISK_BUFFER,
                  {})).get(schema.KEY_MAX_FILE_BUFFER_BYTES, ""),
      (config.get(schema.KEY_FILE_SETTINGS, {})).get(schema.KEY_FILE_PATH, ""),
      (kafka_settings.get(schema.KEY_AUTHENTICATION,
                          {})).get(schema.KEY_USERNAME, ""),
      (kafka_settings.get(schema.KEY_AUTHENTICATION,
                          {})).get(schema.KEY_PASSWORD, ""),
      kafka_settings.get(schema.KEY_TOPIC, ""),
      kafka_settings.get(schema.KEY_GROUP_ID, ""),
      kafka_settings.get(schema.KEY_TIMEOUT, ""),
      forwarder_utility.get_brokers(kafka_settings.get(schema.KEY_BROKERS, [])),
      (kafka_settings.get(schema.KEY_TLS_SETTINGS,
                          {})).get(schema.KEY_CERTIFICATE, ""),
      (kafka_settings.get(schema.KEY_TLS_SETTINGS,
                          {})).get(schema.KEY_CERTIFICATE_KEY, ""),
      (kafka_settings.get(schema.KEY_TLS_SETTINGS,
                          {})).get(schema.KEY_MINIMUM_TLS_VERSION, ""),
      (kafka_settings.get(schema.KEY_TLS_SETTINGS,
                          {})).get(schema.KEY_INSECURE_SKIP_VERIFY, ""),
      pcap_settings.get(schema.KEY_NETWORK_INTERFACE, ""),
      pcap_settings.get(schema.KEY_BPF, ""),
      (splunk_settings.get(schema.KEY_AUTHENTICATION,
                           {})).get(schema.KEY_USERNAME, ""),
      (splunk_settings.get(schema.KEY_AUTHENTICATION,
                           {})).get(schema.KEY_PASSWORD, ""),
      splunk_settings.get(schema.KEY_HOST, ""),
      splunk_settings.get(schema.KEY_PORT, ""),
      splunk_settings.get(schema.KEY_MINIMUM_WINDOW_SIZE, ""),
      splunk_settings.get(schema.KEY_MAXIMUM_WINDOW_SIZE, ""),
      splunk_settings.get(schema.KEY_QUERY_STRING, ""),
      splunk_settings.get(schema.KEY_QUERY_MODE, ""),
      splunk_settings.get(schema.KEY_CERT_IGNORED, ""),
      syslog_settings.get(schema.KEY_PROTOCOL, ""),
      syslog_settings.get(schema.KEY_ADDRESS, ""),
      syslog_settings.get(schema.KEY_PORT, ""),
      syslog_settings.get(schema.KEY_BUFFER_SIZE, ""),
      syslog_settings.get(schema.KEY_CONNECTION_TIMEOUT),
      (syslog_settings.get(schema.KEY_TLS_SETTINGS,
                           {})).get(schema.KEY_CERTIFICATE, ""),
      (syslog_settings.get(schema.KEY_TLS_SETTINGS,
                           {})).get(schema.KEY_CERTIFICATE_KEY, ""),
      (syslog_settings.get(schema.KEY_TLS_SETTINGS,
                           {})).get(schema.KEY_MINIMUM_TLS_VERSION, ""),
      (syslog_settings.get(schema.KEY_TLS_SETTINGS,
                           {})).get(schema.KEY_INSECURE_SKIP_VERIFY, "")
  ]
