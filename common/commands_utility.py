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

import re
from typing import Any, AnyStr, Dict
import yaml


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


def camel_case_to_space(input_str: AnyStr) -> AnyStr:
  """Converts a string to camelcase separated by spaces.

  Args:
    input_str (AnyStr): Input string in camel case. Example - displayName

  Returns:
    AnyStr: Space separated camelcase string. Example - Display name
  """
  return re.sub("([a-z])([A-Z])", r"\g<1> \g<2>", input_str).capitalize()


def convert_dict_keys_to_human_readable(
    input_dict: Dict[AnyStr, Any]) -> Dict[AnyStr, Any]:
  """Converts dictionary keys to a readable format which will be printed on the console.

  Args:
    input_dict (Dict[AnyStr, Any]): Input dictionary. Example:
      {"regexFilters":{"decription": "any description"}}

  Returns:
    Any: Dictionary with modified keys. Example :
    {"Regex filters":{"Description":"any description"}}
  """
  res = dict()
  for k, v in input_dict.items():
    if isinstance(v, dict):
      res[camel_case_to_space(k)] = convert_dict_keys_to_human_readable(v)
    else:
      res[camel_case_to_space(k)] = v
  return res
