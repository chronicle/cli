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

import json
from typing import Any, AnyStr, Dict, List

from common import uri
from common.constants import key_constants
from feeds import feed_templates
from feeds.constants import schema

API_VERSION = "v1"


def get_namespace(feed_response: Dict[str, Any]) -> str:
  """Return namespace.

  Args:
    feed_response (Dict): Feed response.

  Returns:
    str: Namespace to be displayed on console.
  """
  if feed_response.get("namespace", ""):
    return f"  Namespace: {feed_response.get('namespace', '')}\n"
  return ""


def get_labels(feed_response: Dict[str, Any]) -> str:
  """Return key-value pair after correlation with labels.

  Args:
    feed_response (Dict): Feed response.

  Returns:
    str: Labels to be displayed on console.
  """
  labels = []
  for label in feed_response.get("labels", []):
    labels.append(f"    {label['key']}: {label['value']}\n")
  if labels:
    return "  Labels:\n" + "".join(labels)
  return ""


def get_feed_details(flattened_response: Dict[str, Any],
                     detailed_schema: Dict[str, Any]) -> str:
  """Return key-value pair after correlation with schema.

  Args:
    flattened_response (Dict): Flattened feed response.
    detailed_schema (Dict): Feed schema for specific log type and source type.

  Returns:
    str: Feed details to be displayed on console.
  """
  field_response = []
  for field in detailed_schema.get(schema.KEY_DETAILED_FEED_SCHEMAS, []):
    if field[schema.KEY_FIELD_PATH] in flattened_response:
      field_response.append(
          f"    {field[schema.KEY_DISPLAY_NAME]}: "
          f"{flattened_response[field[schema.KEY_FIELD_PATH]]}\n")

  if field_response:
    return "  Feed Settings:\n" + "".join(field_response)
  return ""


def deflatten_dict(input_dict: Dict[AnyStr, Any]) -> Dict[AnyStr, Any]:
  """Convert flattened dictionary in format required by request body.

  Args:
    input_dict (dict): Dictionary with flattened keys.

  Returns:
    output_dict (dict): Dictionary in format required by request body.
  """
  output_dict = {}
  for key, value in input_dict.items():
    temp_dict = output_dict
    parts = key.split(".")
    for part in parts[:-1]:
      temp_dict = temp_dict.setdefault(snake_to_camel(part), {})
    temp_dict[snake_to_camel(parts[-1])] = value
  return output_dict


def snake_to_camel(word: AnyStr) -> AnyStr:
  """Convert snakecase word to camelcase word.

  Args:
    word (str): Snakecase word.

  Returns:
    str: Camelcase word.
  """
  components = word.split("_")
  # We capitalize the first letter of each component except the first one
  # with the 'title' method and join them together.
  return components[0] + "".join(each.title() for each in components[1:])


def get_feed_url(region: str, custom_url: str) -> str:
  """Get feed URL according to selected region.

  Args:
    region (str): Region (US, EUROPE, ASIA_SOUTHEAST1).
    custom_url (str): Base URL to be used for API calls.

  Returns:
    str: Feed URL.
  """
  return uri.get_base_url(region, custom_url) + f"/{API_VERSION}/feeds"


def export_txt(export_path: AnyStr, feed_rows: List[List[str]]) -> None:
  """Write feed list data into txt file.

  Args:
    export_path (AnyStr): Path of file to export output of list command.
    feed_rows (List[List[str]]): Array of all listed feed details.
  """
  with open(export_path, "w") as file_out:
    for feed_id, feed_display_name, source_type, log_type, feed_state, feed_details, namespace, labels in feed_rows:
      feed_template_str = feed_templates.feed_template.substitute(
          feed_id=f"{feed_id}",
          feed_display_name=get_feed_display_name(
              {"displayName": feed_display_name}),
          source_type=f"{source_type}",
          log_type=f"{log_type}",
          feed_state=f"{feed_state}",
          feed_details=f"{feed_details}",
          namespace=f"{namespace}",
          labels=f"{labels}")
      file_out.write(feed_template_str)
      file_out.write(f"\n{'=' * 60}\n")


def write_backup(filename: str, flattened_response: Dict[str, Any],
                 display_source_type: str, source_type: str,
                 display_log_type: str, log_type: str,
                 feed_display_name: str) -> None:
  """Write the data to the backup file.

  Args:
    filename (str): The path of the file to write the data.
    flattened_response (Dict): Flattened response of existing feed.
    display_source_type (str): Display name of the Source Type.
    source_type (str): Source Type value in string.
    display_log_type (str): Display name of the Log Type.
    log_type (str): Log Type value in string.
    feed_display_name (str): Feed display name
  """
  with open(filename, "w") as file:
    flattened_response[schema.KEY_FEED_SOURCE_TYPE] = source_type
    flattened_response[schema.KEY_DISPLAY_SOURCE_TYPE] = display_source_type
    flattened_response[key_constants.KEY_LOG_TYPE] = log_type
    flattened_response[schema.KEY_DISPLAY_LOG_TYPE] = display_log_type
    flattened_response[schema.KEY_DISPLAY_NAME] = feed_display_name
    file.write(json.dumps(flattened_response))


def get_feed_display_name(feed: Dict[str, str]) -> str:
  """Provide feed display name if exist in feed dictionary.

  Args:
    feed: input dictionary

  Returns:
    str: return display name if exist in dictionary.
  """
  return f"\n  Display Name: {feed.get(schema.KEY_DISPLAY_NAME)}" if feed.get(
      schema.KEY_DISPLAY_NAME) else ""
