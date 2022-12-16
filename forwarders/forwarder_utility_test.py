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
import os
from typing import Any, Dict, List
from unittest import mock

from click._compat import WIN

from forwarders import forwarder_utility
from forwarders.tests.fixtures import *  # pylint: disable=wildcard-import
from forwarders.tests.fixtures import TEMP_CREATE_BACKUP_FILE


def test_get_forwarder_url() -> None:
  """Test forwarder url."""
  assert forwarder_utility.get_forwarder_url(
      'US', '') == 'https://backstory.googleapis.com/v2/forwarders'


def test_get_labels_str() -> None:
  """Test printing of key-value pair of labels field."""
  expected_output = ('k: v\n')
  assert forwarder_utility.get_labels_str(
      {'labels': [{
          'key': 'k',
          'value': 'v'
      }]}) == expected_output


def test_get_regex_filters_str(regex_filters: List[Dict[str, Any]]) -> None:
  """Test converting of regex filter from list of dict to str format.

  Args:
    regex_filters (List[Dict[str, Any]]): Test data.
  """
  assert forwarder_utility.get_regex_filters_str(
      regex_filters) in """Description: Describes what is being filtered and why
Regexp: The regular expression used to match against each incoming line
Behavior: ALLOW

Description: Describes what is being filtered and why
Regexp: The regular expression used to match against each incoming line
Behavior: BLOCK

"""


def test_change_dict_keys_order(forwarder_response: Dict[str, Any]) -> None:
  """Test for changing dictionary keys order.

  Args:
    forwarder_response (Dict[str,Any]): Test data.
  """
  assert forwarder_utility.change_dict_keys_order(
      forwarder_response['forwarder']
  ) == {
      'ID': 'forwarder 1',
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


def test_preview_changes(capfd) -> None:
  """Test preview changes."""
  forwarder_utility.preview_changes({'displayName': 'test'})
  output, _ = capfd.readouterr()
  expected_output = """Preview changes:

  - Press Up/b or Down/z keys to paginate.
  - To switch case-sensitivity, press '-i' and press enter. By default, search
    is case-sensitive.
  - To search for specific field, press '/' key, enter text and press enter.
  - Press 'q' to quit and confirm preview changes.
  - Press `h` for all the available options to navigate the list.
=============================================================================

Display name: test"""
  if WIN:
    expected_output = """Preview changes:

  - Press ENTER key (scrolls one line at a time) or SPACEBAR key (display next screen).
  - Press 'q' to quit and confirm preview changes.
============================================================================="""
  assert expected_output in output


def test_write_backup():
  """Test to check write data to backup file."""
  flattend_data = {'display_name': 'tst'}
  forwarder_utility.write_backup(TEMP_CREATE_BACKUP_FILE, flattend_data,
                                 '123-abcd-efg-345')
  assert os.path.exists(TEMP_CREATE_BACKUP_FILE)


@mock.patch(
    'google3.third_party.chronicle.cli.forwarders.forwarder_utility.click.confirm'
)
def test_read_backup_retry_true(mock_choice):
  """Test to read data from backup file if retry.

  Args:
    mock_choice (mock.MagicMock): Mock object.
  """
  flattend_data = {'display_name': 'tst', 'config.log_type': 'WINDOWS_DNS'}
  expected_output = {
      'display_name': 'tst',
      'config.log_type': 'WINDOWS_DNS',
      'name': '123-abcd-efg-345'
  }
  forwarder_utility.write_backup(TEMP_CREATE_BACKUP_FILE, flattend_data,
                                 '123-abcd-efg-345')
  mock_choice.return_value = True
  result = forwarder_utility.read_backup(TEMP_CREATE_BACKUP_FILE,
                                         '123-abcd-efg-345')
  assert result == expected_output


@mock.patch(
    'google3.third_party.chronicle.cli.forwarders.forwarder_utility.click.confirm'
)
def test_read_backup_retry_false(mock_choice):
  """Test to read data from backup file if not retry.

  Args:
    mock_choice (mock.MagicMock): Mock object.
  """
  flattend_data = {'display_name': 'tst', 'config.log_type': 'WINDOWS_DNS'}
  expected_output = {}
  forwarder_utility.write_backup(TEMP_CREATE_BACKUP_FILE, flattend_data,
                                 '123-abcd-efg-345')
  mock_choice.return_value = False
  result = forwarder_utility.read_backup(TEMP_CREATE_BACKUP_FILE,
                                         '123-abcd-efg-345')
  assert result == expected_output


def test_prepare_update_mask():
  """Test to prepare update mask send it with the update API call."""
  request_body_fields = [
      'field1', 'field2.field3', 'field2.field4.field5', 'field6.field7'
  ]
  repeated_message_fields = ['field2.field4', 'field6']
  assert forwarder_utility.prepare_update_mask(request_body_fields,
                                               repeated_message_fields) == [
                                                   'field1', 'field2.field3',
                                                   'field2.field4', 'field6'
                                               ]
