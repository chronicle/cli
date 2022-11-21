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
from typing import Any, AnyStr, Dict

from common import uri
from forwarders.constants import schema

API_VERSION = "v2"
PRINT_SEPARATOR = "=" * 80


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
      schema.KEY_NAME: input_dict[schema.KEY_NAME],
      schema.KEY_DISPLAY_NAME: input_dict[schema.KEY_DISPLAY_NAME],
      schema.KEY_STATE: input_dict[schema.KEY_STATE],
      schema.KEY_CONFIG: input_dict[schema.KEY_CONFIG]
  })
