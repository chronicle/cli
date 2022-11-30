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
"""Unit tests for forwarder_utility.py."""

from typing import Any, Dict
from forwarders import forwarder_utility

from forwarders.tests.fixtures import *  # pylint: disable=wildcard-import


def test_get_forwarder_url() -> None:
  """Test forwarder url."""
  assert forwarder_utility.get_forwarder_url(
      'US', '') == 'https://backstory.googleapis.com/v2/forwarders'


def test_change_dict_keys_order(forwarder_response: Dict[str, Any]) -> None:
  """Test for changing dictionary keys order.

  Args:
    forwarder_response (Dict[str,Any]): Test data.
  """
  assert forwarder_utility.change_dict_keys_order(
      forwarder_response['forwarder']
  ) == {
      'name': 'forwarder 1',
      'displayName': 'User-specified forwarder name',
      'state': 'ACTIVE',
      'config': {
          'uploadCompression': 'TRUE',
          'metadata': {
              'assetNamespace':
                  'test_namespace',
              'labels': [{
                  'key': 'my_key_1',
                  'value': 'my_value_1'
              }, {
                  'key': 'my_key_2',
                  'value': 'my_value_2'
              }]
          },
          'regexFilter': [{
              'description': 'Describes what is being filtered and why',
              'regexp':
                  'The regular expression used to match against each incoming '
                  'line',
              'behavior': 'ALLOW'
          }, {
              'description': 'Describes what is being filtered and why',
              'regexp':
                  'The regular expression used to match against each incoming '
                  'line',
              'behavior': 'BLOCK'
          }],
          'serverSetting': {
              'state': 'ACTIVE',
              'gracefulTimeout': 234,
              'drainTimeout': 567,
              'httpSettings': {
                  'port': 10000,
                  'host': '10.0.1.3',
                  'readTimeout': 29,
                  'readHeaderTimeout': 34,
                  'writeTimeout': 2,
                  'idleTimeout': 34,
                  'routeSettings': {
                      'availableStatusCode': 12,
                      'readyStatusCode': 33,
                      'unreadyStatusCode': 43
                  }
              }
          }
      }
  }


def test_get_source_id() -> None:
  """Test to extract source id."""
  forwarder = {'name': 'forwarders/asdf1234-1234-abcd-efgh-12345678abcd'}
  assert forwarder_utility.get_resource_id(
      forwarder) == 'asdf1234-1234-abcd-efgh-12345678abcd'

