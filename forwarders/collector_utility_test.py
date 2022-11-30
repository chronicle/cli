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
"""Unit tests for collector_utility.py."""

from typing import Any, Dict
from unittest import mock
from forwarders import collector_utility
from forwarders.tests.fixtures import *  # pylint: disable=wildcard-import


def test_get_collector_url() -> None:
  """Test collector url."""
  assert collector_utility.get_collector_url(
      'US', '', 'asdf1234-1234-abcd-efgh-12345678abcd'
  ) == 'https://backstory.googleapis.com/v2/forwarders/asdf1234-1234-abcd-efgh-12345678abcd/collectors'


def test_fetch_collectors_200(list_collectors_data: Dict[str, Any]) -> None:
  """Test for fetching collectors for respective forwardes.

  Args:
    list_collectors_data (Dict[str, Any]): Test data.
  """
  mock_client = mock.Mock()
  mock_client.request.return_value = list_collectors_data
  expected_output = ({
      'collectors': [{
          'name':
              'forwarders/asdf1234-1234-abcd-efgh-12345678abcd/collectors/asdf1234-1234-abcd-efgh',
          'displayName':
              'collector pqr',
          'config': {
              'logType': 'Type of logs collected.',
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
                  'regexp': 'The regular expression used to match against each '
                            'incoming line',
                  'behavior': 'ALLOW'
              }, {
                  'description': 'Describes what is being filtered and why',
                  'regexp': 'The regular expression used to match against each '
                            'incoming line',
                  'behavior': 'BLOCK'
              }],
              'diskBuffer': {
                  'state': 'ACTIVE',
                  'directoryPath': 'Directory path for files written.',
                  'maxFileBufferBytes': 3999
              },
              'maxSecondsPerBatch': 10,
              'maxBytesPerBatch': 1048576,
              'fileSettings': {
                  'filePath': 'Path of file to monitor.'
              }
          },
          'state':
              'ACTIVE'
      }]
  }, {
      'collectors': {}
  })
  assert collector_utility.fetch_collectors(
      'https://backstory.googleapis.com/v2/forwarders/asdf1234-1234-abcd-efgh-12345678abcd/collectors',
      'GET', mock_client) == expected_output


def test_fetch_collectors_empty_schema(
    list_empty_collectors_data: Dict[str, Any]) -> None:
  """Test of no collectors found for respective forwarder.

  Args:
    list_empty_collectors_data (Dict[str, Any]): Test data.
  """
  mock_client = mock.Mock()
  mock_client.request.side_effect = [list_empty_collectors_data]
  result = collector_utility.fetch_collectors(
      'https://backstory.googleapis.com/v2/forwarders/asdf1234-1234-abcd-efgh-12345678abcd/collectors',
      'GET', mock_client)
  assert result == ({}, {
      'collectors': {
          'message': 'No collectors found for this forwarder.'
      }
  })


def test_fetch_collectors_error_code(
    list_error_collectors_data: Dict[str, Any]) -> None:
  """Test to check collectors error code.

  Args:
    list_error_collectors_data (Dict[str, Any]): Test data.
  """
  mock_client = mock.Mock()
  mock_client.request.side_effect = [list_error_collectors_data]
  result = collector_utility.fetch_collectors(
      'https://backstory.googleapis.com/v2/forwarders/asdf1234-1234-abcd-efgh-12345678abcd/collectors',
      'GET', mock_client)
  assert result == ({
      'error': {
          'message':
              'generic::invalid_argument: parent (forwarders/abx-22) does not '
              'contain a valid UUID: invalid argument'
      }
  }, {
      'collectors': {
          'error': {
              'responseCode': 400,
              'message':
                  'generic::invalid_argument: parent (forwarders/abx-22) does '
                  'not contain a valid UUID: invalid argument'
          }
      }
  })
