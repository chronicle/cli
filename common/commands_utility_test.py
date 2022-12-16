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


def test_space_separated_str() -> None:
  """Test converting of camel case sentence to space seprated first letter capital.
  """
  assert commands_utility.space_separated_str('dummyTest') == 'Dummy test'


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


def test_convert_to_snakecase() -> None:
  """Test converting of camelcase key name to snakecase key name."""
  assert commands_utility.convert_to_snakecase(
      'workdaySettings') == 'workday_settings'


def test_flatten_dict() -> None:
  """Test flattening of dict."""
  input_dict = {'a': {'b': 'c'}, 1: {'a': [1]}, 'p': {'q': {'r': 's'}}}
  expected_output = {'a.b': 'c', '1.a': [1], 'p.q.r': 's'}
  assert commands_utility.flatten_dict(input_dict) == expected_output


def test_flatten_dict_with_custom_parent_and_separator() -> None:
  """Test flattening of dict with custom key and separator."""
  input_dict = {'a': {'b': 'c'}, 1: {'a': [1]}, 'p': {'q': {'r': 's'}}}
  expected_output = {
      'custom_key_a_b': 'c',
      'custom_key_1_a': [1],
      'custom_key_p_q_r': 's'
  }
  assert commands_utility.flatten_dict(input_dict, 'custom_key',
                                       '_') == expected_output


def test_unpack() -> None:
  """Test unpacking of dictionary."""
  data = {'key': 'value'}
  assert len(commands_utility.unpack(data)) == 1


def test_unpack_row_data() -> None:
  """Test unpacking of row data."""
  data = 'dummy_data'
  assert commands_utility.unpack(data) == 'dummy_data'


def test_convert_dict_keys_to_snake_case() -> None:
  """Test converting of dictionary keys to snake case."""
  data = {'sampleKey1': 'sample', 'sampleKey2': 'sample'}
  expected_output = {'sample_key1': 'sample', 'sample_key2': 'sample'}
  assert commands_utility.convert_dict_keys_to_snake_case(
      data) == expected_output


def test_convert_nested_dict_keys_to_snake_case() -> None:
  """Test converting of nested dictionary keys to snake case."""
  data = {
      'sampleKey1': 'sample',
      'sampleKey2': [{
          'sampleKey3': 'sample'
      }],
      'sampleKey3': ['value1', 'value2']
  }
  expected_output = {
      'sample_key1': 'sample',
      'sample_key2': [{
          'sample_key3': 'sample'
      }],
      'sample_key3': ['value1', 'value2']
  }
  assert commands_utility.convert_nested_dict_keys_to_snake_case(
      data) == expected_output


def test_remove_sensitive_fields():
  """Test removing sensitive fields."""
  backup_data = {
      'key1': 'value1',
      'key2': {
          'key3': 'value3',
          'password': 'dummy_password'
      }
  }
  commands_utility.remove_sensitive_fields(backup_data)
  assert backup_data == {'key1': 'value1', 'key2': {'key3': 'value3'}}
