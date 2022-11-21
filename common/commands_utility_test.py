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
"""Unit tests for commands_utility.py."""

from typing import Any, Dict

from common import commands_utility
from forwarders.tests.fixtures import *  # pylint: disable=wildcard-import


def test_lower_or_none() -> None:
  """Test conversion of string to lowercase string."""
  assert commands_utility.lower_or_none('TEST') == 'test'


def test_lower_or_none_none() -> None:
  """Test return of string as None if string is None."""
  assert commands_utility.lower_or_none(None) is None


def test_camel_case_to_space() -> None:
  """Test converting of camel case sentence to space seprated first letter capital.
  """
  assert commands_utility.camel_case_to_space('dummyTest') == 'Dummy test'


def test_convert_dict_to_yaml(forwarder_response: Dict[str, Any]) -> None:
  """Test converting of dictionary to yaml user readable format.

  Args:
    forwarder_response (Dict[str, Any]): Test data.
  """
  assert commands_utility.convert_dict_to_yaml(
      forwarder_response) == """forwarder:
  name: forwarder 1
  displayName: User-specified forwarder name
  config:
    uploadCompression: 'TRUE'
    metadata:
      assetNamespace: test_namespace
      labels:
      - key: my_key_1
        value: my_value_1
      - key: my_key_2
        value: my_value_2
    regexFilter:
    - description: Describes what is being filtered and why
      regexp: The regular expression used to match against each incoming line
      behavior: ALLOW
    - description: Describes what is being filtered and why
      regexp: The regular expression used to match against each incoming line
      behavior: BLOCK
    serverSetting:
      state: ACTIVE
      gracefulTimeout: 234
      drainTimeout: 567
      httpSettings:
        port: 10000
        host: 10.0.1.3
        readTimeout: 29
        readHeaderTimeout: 34
        writeTimeout: 2
        idleTimeout: 34
        routeSettings:
          availableStatusCode: 12
          readyStatusCode: 33
          unreadyStatusCode: 43
  state: ACTIVE
"""


def test_convert_dict_keys_to_human_readable(
    forwarder_response: Dict[str, Any]) -> None:
  """Test for processing dictionary keys.

  Args:
    forwarder_response (Dict[str,Any]): Test data.
  """
  assert commands_utility.convert_dict_keys_to_human_readable(
      forwarder_response) == {
          'Forwarder': {
              'Name': 'forwarder 1',
              'Display name': 'User-specified forwarder name',
              'Config': {
                  'Upload compression': 'TRUE',
                  'Metadata': {
                      'Asset namespace':
                          'test_namespace',
                      'Labels': [{
                          'key': 'my_key_1',
                          'value': 'my_value_1'
                      }, {
                          'key': 'my_key_2',
                          'value': 'my_value_2'
                      }]
                  },
                  'Regex filter': [{
                      'description': 'Describes what is being filtered and why',
                      'regexp':
                          'The regular expression used to match against each '
                          'incoming line',
                      'behavior': 'ALLOW'
                  }, {
                      'description': 'Describes what is being filtered and why',
                      'regexp':
                          'The regular expression used to match against each '
                          'incoming line',
                      'behavior': 'BLOCK'
                  }],
                  'Server setting': {
                      'State': 'ACTIVE',
                      'Graceful timeout': 234,
                      'Drain timeout': 567,
                      'Http settings': {
                          'Port': 10000,
                          'Host': '10.0.1.3',
                          'Read timeout': 29,
                          'Read header timeout': 34,
                          'Write timeout': 2,
                          'Idle timeout': 34,
                          'Route settings': {
                              'Available status code': 12,
                              'Ready status code': 33,
                              'Unready status code': 43
                          }
                      }
                  }
              },
              'State': 'ACTIVE'
          }
      }
