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
import re
from typing import Any, AnyStr, Dict

import yaml

from forwarders.constants.schema import SENSITIVE_FIELDS


def lower_or_none(input_str: AnyStr) -> Any:
  """Converts input string to lowercase if not None.

  Args:
    input_str (AnyStr): Input string.

  Returns:
    str: String in lower case if not None.
  """
  return input_str.lower() if input_str else None


def convert_dict_to_yaml(input_dict: Dict[AnyStr, Any]) -> Any:
  """Converts JSON dictionary to YAML format.

  Args:
    input_dict (Dict[AnyStr, Any]): JSON dictionary

  Returns:
    Any: YAML output to be printed on console.
  """
  return yaml.dump(input_dict, Dumper=yaml.Dumper, sort_keys=False)


def space_separated_str(input_str: AnyStr) -> AnyStr:
  """Converts a string separated by spaces.

  Args:
    input_str (AnyStr): Input string in camel case or snake case. Example -
      displayName, commands_utility

  Returns:
    AnyStr: Space separated string. Example - Display name, Commands
    utility
  """
  # Handle input string in snake case.
  components = input_str.split("_")
  # Capitalize the first letter of each component except the first one
  # with the 'title' method and join them together.
  camel_case_str = components[0] + "".join(
      each.title() for each in components[1:])

  return re.sub("([a-z])([A-Z])", r"\g<1> \g<2>", camel_case_str).capitalize()


def convert_dict_keys_to_human_readable(
    input_dict: Dict[AnyStr, Any]) -> Dict[AnyStr, Any]:
  """Converts dictionary keys to a readable format which will be printed on the console.

  Args:
    input_dict (Dict[AnyStr, Any]): Input dictionary. Example:
      {"regexFilters":{"decription": "any description"}}

  Returns:
    Any: Dictionary with modified keys. Example:
    {"Regex filters":{"Description":"any description"}}
  """
  res = dict()
  for k, v in input_dict.items():
    if isinstance(v, dict):
      res[space_separated_str(k)] = convert_dict_keys_to_human_readable(v)
    else:
      res[space_separated_str(k)] = v
  return res


def convert_to_snakecase(key: AnyStr) -> AnyStr:
  """Converts camelcase key name to snakecase key name.

  Args:
    key (AnyStr): Camelcase key name.

  Returns:
    AnyStr: Snakecase key name.
  """
  s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", key)
  return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def unpack(data: Any) -> Any:
  """Unpack value from dictionary.

  Args:
    data (Any): Input dictionary or list.

  Returns:
    Any: List containing tuple of key and value.
  """
  if isinstance(data, dict):
    return data.items()
  return data


def convert_dict_keys_to_snake_case(content: Any) -> Dict[AnyStr, Any]:
  """Convert all keys for given dict to snake case.

  Args:
    content (Any): Input dictionary.

  Returns:
    Dict[AnyStr, Any]: Dictionary with snake case keys.
  """
  return {convert_to_snakecase(key): value for key, value in content.items()}


def convert_nested_dict_keys_to_snake_case(data: Any) -> Dict[str, Any]:
  """Convert all keys for given dict/list to snake case recursively.

  Args:
    data (Any): Input dictionary or list.

  Returns:
    Dict[str, Any]: Dictionary or list with snake case keys.
  """
  converted_dict = {}
  for key, value in unpack(convert_dict_keys_to_snake_case(data)):
    if isinstance(value, dict):
      converted_dict[key] = convert_nested_dict_keys_to_snake_case(value)
    elif isinstance(value, list) and len(value) >= 1:
      converted_dict[key] = []
      for _, val in enumerate(value):
        if isinstance(val, dict):
          converted_dict[key].append(
              convert_nested_dict_keys_to_snake_case(val))
        else:
          converted_dict[key].append(val)
    else:
      converted_dict[key] = value
  return converted_dict


def flatten_dict(input_dict: Dict[str, Any],
                 parent_key: AnyStr = "",
                 sep: AnyStr = ".") -> Dict[str, Any]:
  """Flatten dictionary.

  Args:
    input_dict (Dict[str, Any]): Input dictionary from API response.
    parent_key (AnyStr): The parent key name for which the data is being
      flattened.
    sep (AnyStr): The separator indicates by which the name will be formed for
      the flattened data. Example - input_dict - {'name': 'feeds/123',
      'details': {'logType': 'WORKDAY'}} Output - {'name': 'feeds/123',
      'details.log_type': 'WORKDAY'}.

  Returns:
    Dict[str]: Flattened dictionary.
  """
  items = []
  for k, v in input_dict.items():
    new_key = parent_key + sep + str(k) if parent_key else str(k)
    if isinstance(v, collections.abc.MutableMapping):
      items.extend(
          flatten_dict(v, convert_to_snakecase(new_key), sep=sep).items())  # pytype: disable=wrong-arg-types
    else:
      items.append((convert_to_snakecase(new_key), v))

  return dict(items)


def remove_sensitive_fields(data: Dict[str, Any]):
  """Remove sensitive fields from data dictionary while writing a backup.

  Args:
    data (Dict): Backup data dictionary.
  """
  for field_name, field_value in list(data.items()):
    if isinstance(field_value, dict):
      remove_sensitive_fields(field_value)
    else:
      if field_name in SENSITIVE_FIELDS:
        data.pop(field_name, None)
