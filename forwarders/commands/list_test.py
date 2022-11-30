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
"""Unit tests for list.py."""
from typing import Any, Dict
from unittest import mock

from click.testing import CliRunner

from forwarders.commands.list import list_command
from forwarders.tests.fixtures import *  # pylint: disable=wildcard-import
from mock_test_utility import MockResponse

runner = CliRunner()


@mock.patch(
    "forwarders.commands.list.chronicle_auth.initialize_http_session"
)
def test_list_no_forwarders_found(
    mock_client: mock.MagicMock, list_empty_forwarders_data: Dict[str,
                                                                  Any]) -> None:
  """Test case to check if no forwarders found for customer.

  Args:
    mock_client (mock.MagicMock): Mock object
    list_empty_forwarders_data (Tuple): Test data to fetch list of forwarders
      with empty response.
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      list_empty_forwarders_data,
      MockResponse(status_code=200, text="""{}""")
  ]
  result = runner.invoke(list_command)
  assert result.output == ("Fetching list of forwarders...\nNo forwarders "
                           "found.\n")


@mock.patch(
    "forwarders.commands.list.chronicle_auth.initialize_http_session"
)
def test_list_error_code(mock_client: mock.MagicMock,
                         list_error_forwarders_data: Dict[str, str]) -> None:
  """Test case to check for empty list of forwarders.

  Args:
    mock_client (mock.MagicMock): Mock object
    list_error_forwarders_data (Tuple): Test data to fetch list of forwarders
      with error response.
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      list_error_forwarders_data,
      MockResponse(status_code=200, text="""{"collectors": []}""")
  ]
  result = runner.invoke(list_command)
  assert "Failed to list forwarders." in result.output


@mock.patch(
    "forwarders.commands.list.chronicle_auth.initialize_http_session"
)
def test_list_fetch_collectors_error(
    mock_client: mock.MagicMock, list_forwarders_data: Dict[str, Any],
    list_error_collectors_data: Dict[str, Any],
    list_collectors_data: Dict[str, Any]) -> None:
  """Test to check if list collectors API calls returns bad request in between.

  Args:
    mock_client (mock.MagicMock): Mock object.
    list_forwarders_data (Tuple): Test data to fetch list of forwarders.
    list_error_collectors_data (Tuple): Test data to fetch list of forwarders
      with error response.
    list_collectors_data (Tuple): Test data to fetch list of collectors.
  """

  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      list_forwarders_data, list_error_collectors_data, list_collectors_data
  ]

  result = runner.invoke(list_command)
  assert """Collectors:
  Error:
    Response code: 400
    Message: 'generic::invalid_argument: parent (forwarders/abx-22) does not contain
      a valid UUID: invalid argument'""" in result.output


@mock.patch(
    "forwarders.commands.list.chronicle_auth.initialize_http_session"
)
def test_list_200(mock_client: mock.MagicMock, list_forwarder_data: Dict[str,
                                                                         Any],
                  list_collectors_data: Dict[str, Any]) -> None:
  """Test case to check response for 200 response code.

  Args:
    mock_client (mock.MagicMock): Mock object
    list_forwarder_data (Tuple): Test data to fetch forwarder.
    list_collectors_data (Tuple): Test data to fetch list of collectors.
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      list_forwarder_data, list_collectors_data
  ]
  result = runner.invoke(list_command)
  assert """Fetching list of forwarders...

Forwarder Details:

Name: asdf1234-1234-abcd-efgh-12345678abcd
Display name: forwarder 1
State: ACTIVE
Config:
  Upload compression: 'TRUE'
  Metadata:
    Asset namespace: test_namespace
    Labels:
    - key: my_key_1
      value: my_value_1
    - key: my_key_2
      value: my_value_2
  Regex filter:
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: ALLOW
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: BLOCK
  Server setting:
    State: ACTIVE
    Graceful timeout: 234
    Drain timeout: 567
    Http settings:
      Port: 10000
      Host: 10.0.1.3
      Read timeout: 29
      Read header timeout: 34
      Write timeout: 2
      Idle timeout: 34
      Route settings:
        Available status code: 12
        Ready status code: 33
        Unready status code: 43

Collectors:
  Collector [asdf1234-1234-abcd-efgh]:
    Name: asdf1234-1234-abcd-efgh
    Display name: collector pqr
    State: ACTIVE
    Config:
      Log type: Type of logs collected.
      Metadata:
        Asset namespace: test_namespace
        Labels:
        - key: my_key_1
          value: my_value_1
        - key: my_key_2
          value: my_value_2
      Regex filter:
      - description: Describes what is being filtered and why
        regexp: The regular expression used to match against each incoming line
        behavior: ALLOW
      - description: Describes what is being filtered and why
        regexp: The regular expression used to match against each incoming line
        behavior: BLOCK
      Disk buffer:
        State: ACTIVE
        Directory path: Directory path for files written.
        Max file buffer bytes: 3999
      Max seconds per batch: 10
      Max bytes per batch: 1048576
      File settings:
        File path: Path of file to monitor.""" in result.output


@mock.patch(
    "forwarders.commands.list.chronicle_auth.initialize_http_session"
)
def test_credential_file_invalid(mock_client: mock.MagicMock) -> None:
  """Test case for checking invalid credential path.

  Args:
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = OSError(
      "Credential Path not found.")
  # Method Call
  expected_message = "Failed with exception: Credential Path not found."

  result = runner.invoke(list_command,
                         ["--credential_file", "dummy.json", "--region", "us"])
  assert expected_message in result.output


@mock.patch(
    "forwarders.commands.list.chronicle_auth.initialize_http_session"
)
def test_list_no_collectors_found(mock_client: mock.MagicMock,
                                  list_forwarders_data: Dict[str, str],
                                  list_empty_collectors_data: Dict[str, Any],
                                  list_collectors_data: Dict[str, Any]) -> None:
  """Test to check no collectors found for respective forwarder.

  Args:
    mock_client (mock.MagicMock): Mock object.
    list_forwarders_data (Tuple): Test data to fetch list of forwarders.
    list_empty_collectors_data (Tuple): Test data to fetch list of collectors
      with empty response body.
    list_collectors_data (Tuple): Test data to fetch list of collectors.
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      list_forwarders_data, list_empty_collectors_data, list_collectors_data
  ]
  result = runner.invoke(list_command)
  assert """Fetching list of forwarders...

Forwarder Details:

Name: asdf1234-1234-abcd-efgh-12345678abcd
Display name: forwarder 1
State: ACTIVE
Config:
  Upload compression: 'TRUE'
  Metadata:
    Asset namespace: test_namespace
    Labels:
    - key: my_key_1
      value: my_value_1
    - key: my_key_2
      value: my_value_2
  Regex filter:
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: ALLOW
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: BLOCK
  Server setting:
    State: ACTIVE
    Graceful timeout: 234
    Drain timeout: 567
    Http settings:
      Port: 10000
      Host: 10.0.1.3
      Read timeout: 29
      Read header timeout: 34
      Write timeout: 2
      Idle timeout: 34
      Route settings:
        Available status code: 12
        Ready status code: 33
        Unready status code: 43

Collectors:
  Message: No collectors found for this forwarder.

================================================================================

Forwarder Details:

Name: asdf1234-1234-abcd-efgh-12345678abcd
Display name: forwarder 1
State: ACTIVE
Config:
  Upload compression: 'TRUE'
  Metadata:
    Asset namespace: test_namespace
    Labels:
    - key: my_key_1
      value: my_value_1
    - key: my_key_2
      value: my_value_2
  Regex filter:
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: ALLOW
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: BLOCK
  Server setting:
    State: ACTIVE
    Graceful timeout: 234
    Drain timeout: 567
    Http settings:
      Port: 10000
      Host: 10.0.1.3
      Read timeout: 29
      Read header timeout: 34
      Write timeout: 2
      Idle timeout: 34
      Route settings:
        Available status code: 12
        Ready status code: 33
        Unready status code: 43

Collectors:
  Collector [asdf1234-1234-abcd-efgh]:
    Name: asdf1234-1234-abcd-efgh
    Display name: collector pqr
    State: ACTIVE
    Config:
      Log type: Type of logs collected.
      Metadata:
        Asset namespace: test_namespace
        Labels:
        - key: my_key_1
          value: my_value_1
        - key: my_key_2
          value: my_value_2
      Regex filter:
      - description: Describes what is being filtered and why
        regexp: The regular expression used to match against each incoming line
        behavior: ALLOW
      - description: Describes what is being filtered and why
        regexp: The regular expression used to match against each incoming line
        behavior: BLOCK
      Disk buffer:
        State: ACTIVE
        Directory path: Directory path for files written.
        Max file buffer bytes: 3999
      Max seconds per batch: 10
      Max bytes per batch: 1048576
      File settings:
        File path: Path of file to monitor.""" in result.output


@mock.patch(
    "forwarders.commands.list.chronicle_auth.initialize_http_session"
)
def test_verbose_output(mock_client: mock.MagicMock, list_forwarder_data,
                        list_collectors_data) -> None:
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      list_forwarder_data, list_collectors_data
  ]
  result = runner.invoke(list_command, ["--verbose"])
  assert """Fetching list of forwarders...

Forwarder Details:

Name: asdf1234-1234-abcd-efgh-12345678abcd
Display name: forwarder 1
State: ACTIVE
Config:
  Upload compression: 'TRUE'
  Metadata:
    Asset namespace: test_namespace
    Labels:
    - key: my_key_1
      value: my_value_1
    - key: my_key_2
      value: my_value_2
  Regex filter:
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: ALLOW
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: BLOCK
  Server setting:
    State: ACTIVE
    Graceful timeout: 234
    Drain timeout: 567
    Http settings:
      Port: 10000
      Host: 10.0.1.3
      Read timeout: 29
      Read header timeout: 34
      Write timeout: 2
      Idle timeout: 34
      Route settings:
        Available status code: 12
        Ready status code: 33
        Unready status code: 43

Collectors:
  Collector [asdf1234-1234-abcd-efgh]:
    Name: asdf1234-1234-abcd-efgh
    Display name: collector pqr
    State: ACTIVE
    Config:
      Log type: Type of logs collected.
      Metadata:
        Asset namespace: test_namespace
        Labels:
        - key: my_key_1
          value: my_value_1
        - key: my_key_2
          value: my_value_2
      Regex filter:
      - description: Describes what is being filtered and why
        regexp: The regular expression used to match against each incoming line
        behavior: ALLOW
      - description: Describes what is being filtered and why
        regexp: The regular expression used to match against each incoming line
        behavior: BLOCK
      Disk buffer:
        State: ACTIVE
        Directory path: Directory path for files written.
        Max file buffer bytes: 3999
      Max seconds per batch: 10
      Max bytes per batch: 1048576
      File settings:
        File path: Path of file to monitor.

================================================================================
==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: https://backstory.googleapis.com/v2/forwarders
  Method: GET
  Body: None
Response:
  Body: {'forwarders': [{'name': 'forwarders/asdf1234-1234-abcd-efgh-12345678abcd', 'displayName': 'forwarder 1', 'config': {'uploadCompression': 'TRUE', 'metadata': {'assetNamespace': 'test_namespace', 'labels': [{'key': 'my_key_1', 'value': 'my_value_1'}, {'key': 'my_key_2', 'value': 'my_value_2'}]}, 'regexFilter': [{'description': 'Describes what is being filtered and why', 'regexp': 'The regular expression used to match against each incoming line', 'behavior': 'ALLOW'}, {'description': 'Describes what is being filtered and why', 'regexp': 'The regular expression used to match against each incoming line', 'behavior': 'BLOCK'}], 'serverSetting': {'state': 'ACTIVE', 'gracefulTimeout': 234, 'drainTimeout': 567, 'httpSettings': {'port': 10000, 'host': '10.0.1.3', 'readTimeout': 29, 'readHeaderTimeout': 34, 'writeTimeout': 2, 'idleTimeout': 34, 'routeSettings': {'availableStatusCode': 12, 'readyStatusCode': 33, 'unreadyStatusCode': 43}}}}, 'state': 'ACTIVE'}]}

==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: https://backstory.googleapis.com/v2/forwarders/asdf1234-1234-abcd-efgh-12345678abcd/collectors
  Method: GET
  Body: None
Response:
  Body: {'collectors': [{'name': 'asdf1234-1234-abcd-efgh', 'displayName': 'collector pqr', 'config': {'logType': 'Type of logs collected.', 'metadata': {'assetNamespace': 'test_namespace', 'labels': [{'key': 'my_key_1', 'value': 'my_value_1'}, {'key': 'my_key_2', 'value': 'my_value_2'}]}, 'regexFilter': [{'description': 'Describes what is being filtered and why', 'regexp': 'The regular expression used to match against each incoming line', 'behavior': 'ALLOW'}, {'description': 'Describes what is being filtered and why', 'regexp': 'The regular expression used to match against each incoming line', 'behavior': 'BLOCK'}], 'diskBuffer': {'state': 'ACTIVE', 'directoryPath': 'Directory path for files written.', 'maxFileBufferBytes': 3999}, 'maxSecondsPerBatch': 10, 'maxBytesPerBatch': 1048576, 'fileSettings': {'filePath': 'Path of file to monitor.'}}, 'state': 'ACTIVE'}]}""" in result.output
