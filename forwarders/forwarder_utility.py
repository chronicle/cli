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
"""Utility functions."""

import collections
import json
import os.path
from typing import Any, AnyStr, Dict, List, Optional

import click
from click._compat import WIN

from common import commands_utility
from common import file_utility
from common import uri
from forwarders import forwarder_templates
from forwarders.constants import schema

API_VERSION = "v2"
PRINT_SEPARATOR = "=" * 80


def export_txt(export_path: AnyStr, final_json_response: Dict[str,
                                                              Any]) -> None:
  """Exports forwarder or collectors data to a txt file.

  Args:
    export_path (AnyStr): Path of file to export output of list command.
    final_json_response (Dict[str, Any]): Json with all required details.
  """
  with open(export_path, "w") as f:
    if schema.KEY_COLLECTORS in final_json_response:
      for each_collector in final_json_response[schema.KEY_COLLECTORS]:
        f.write("\n\nCollector Details:\n\n")
        f.write(
            commands_utility.convert_dict_to_yaml(
                commands_utility.convert_dict_keys_to_human_readable(
                    each_collector)))
        f.write(f"\n{PRINT_SEPARATOR}")
    else:
      for forwarder in final_json_response.get(schema.KEY_FORWARDERS, []):
        f.write("\n\nForwarder Details:\n\n")
        f.write(
            commands_utility.convert_dict_to_yaml(
                commands_utility.convert_dict_keys_to_human_readable(
                    change_dict_keys_order(forwarder))))
        f.write(
            commands_utility.convert_dict_to_yaml(
                commands_utility.convert_dict_keys_to_human_readable(
                    {schema.KEY_COLLECTORS: forwarder[schema.KEY_COLLECTORS]})))
        f.write(f"{PRINT_SEPARATOR}")


def get_labels_str(forwarder_response: Dict[str, Any]) -> str:
  """Converts kv dict to string for showing the data in CSV file.

  Args:
    forwarder_response (Dict[str, Any]): Forwarder response. Example -
      {'labels':{'key':'k1', 'value':'v1'}}

  Returns:
    str: Labels to be displayed on console. Example - "k1: v1"
  """
  labels = []
  for label in forwarder_response.get("labels", []):
    labels.append(f"{label['key']}: {label['value']}\n")
  return "\n".join(labels)


def get_regex_filters_str(regex_filters: List[Dict[str, Any]]) -> str:
  """Converts regex filter dict from response to string for showing it in CSV cell.

  Args:
    regex_filters (List[Dict[str, Any]]): List of regex filters configuration.
      Example - {'description': 'test', 'regexp': '.*','behavior': 'ALLOW'}

  Returns:
    str: String to represent in cell. Example - Description: test
  Regexp: .*
  Behavior: ALLOW
  """
  regex_filter_inline = []
  for regex_filter in regex_filters:
    regex_filter_inline.append(
        f"Description: {regex_filter.get(schema.KEY_DESCRIPTION, '')}\nRegexp: {regex_filter.get(schema.KEY_REGEXP, '')}\nBehavior: {regex_filter.get(schema.KEY_BEHAVIOR, '')}\n"
    )
  return "\n".join(regex_filter_inline)


def get_brokers(brokers: List[str]) -> str:
  """Converts list of brkers into string format.

  Args:
    brokers (List[str]): List of brokers. Example - ['b1','b2']

  Returns:
    str: String representation of broker. Example - "b1
    b2"
  """
  return "\n".join(brokers)


def get_forwarder_url(region: str, custom_url: str) -> str:
  """Gets forwarder URL according to selected region.

  Args:
    region (str): Region (US, EUROPE, ASIA_SOUTHEAST1).
    custom_url (str): Base URL to be used for API calls.

  Returns:
    str: Forwarder URL.
  """
  return uri.get_base_url(region, custom_url) + f"/{API_VERSION}/forwarders"


def change_dict_keys_order(input_dict: Dict[AnyStr, Any]) -> Dict[AnyStr, Any]:
  """Takes dictionary and modifies order of keys.

  Args:
    input_dict (Dict[AnyStr, Any]): Input dictionary to modified keys order

  Returns:
    Dict: Modified dict.
  """
  return collections.OrderedDict({
      schema.KEY_ID: input_dict[schema.KEY_NAME],
      schema.KEY_DISPLAY_NAME: input_dict[schema.KEY_DISPLAY_NAME],
      schema.KEY_STATE: input_dict[schema.KEY_STATE],
      schema.KEY_CONFIG: input_dict[schema.KEY_CONFIG]
  })


def get_resource_id(resource: Dict[str, Any]) -> str:
  """Extracts resource id from name field.

  Args:
    resource (Dict[str, Any]): Resource could be forwarder or collector.

  Returns:
    str: Resource id.
  """
  return resource.get(schema.KEY_NAME, "").split("/")[-1]


def preview_changes(request_body: Dict[str, Any]):
  """Preview changes to user for approval.

  Args:
    request_body (Dict[str, Any]): Request body.
  """
  preview_template_str = f"{forwarder_templates.preview_template.template}\n"
  if WIN:
    preview_template_str = f"{forwarder_templates.preview_template_win.template}\n"
  preview_template_str = preview_template_str + commands_utility.convert_dict_to_yaml(
      commands_utility.convert_dict_keys_to_human_readable(request_body))
  click.echo_via_pager(preview_template_str)


def write_backup(file_path: str,
                 backup_data: Dict[str, Any],
                 backup_id: Optional[str] = None) -> None:
  """Write the data to the backup file.

  Args:
    file_path (str): The path of the file to write the data.
    backup_data (Dict): Backup data of existing forwarder or collector.
    backup_id (str): ID of forwarder or collector for backup.
  """
  # Check backup data exists or not.
  if backup_data:
    if backup_id:
      backup_data[schema.KEY_NAME] = backup_id
    commands_utility.remove_sensitive_fields(backup_data)
    with open(file_path, "w") as file:
      file.write(json.dumps(backup_data))


def read_backup(file_path: str,
                backup_id: Optional[str] = None) -> Dict[str, Any]:
  """Read the data from backup file.

  Args:
    file_path (str): Name of the backup file to read.
    backup_id (str): ID of forwarder or collector for backup.

  Returns:
    Dict: Backup data of existing forwarder.
  """
  backup_response = {}

  # Check whether file exists and its contents are not empty.
  if os.path.exists(file_path) and (os.path.getsize(file_path)) != 0:

    # Read backup data.
    with open(file_path, "r") as file:
      backup_data = json.load(file)

    retry_template_str = forwarder_templates.retry_template.substitute(
        display_name=backup_data["display_name"])

    # Checks the backup data against the appropriate forwarder/collector id.
    if backup_id == backup_data.get(schema.KEY_NAME):

      # Ask user to confirm use of backup data.
      retry = click.confirm(f"{retry_template_str}", default=False)

      if retry:
        backup_response = backup_data
      else:
        file_utility.remove_file(file_path)

  return backup_response


def prepare_update_mask(request_body_fields: List[str],
                        repeated_message_fields: List[str]) -> List[str]:
  """Prepare update_mask used for update forwarder API request.

  Args:
    request_body_fields (List[str]): List of key names of request body. Example:
      ['field1', 'field2.field3', 'field2.field4.field5', 'field6.field7']
    repeated_message_fields (List[str]): List of fields with type repeated in
      schema. Example: ['field2.field4', 'field6']

  Returns:
    List[str]: Update mask.
  """
  update_mask_fields = []
  for updated_field in request_body_fields:
    if not updated_field.startswith(tuple(repeated_message_fields)):
      update_mask_fields.append(updated_field)
  update_mask_fields.extend(repeated_message_fields)
  return update_mask_fields
