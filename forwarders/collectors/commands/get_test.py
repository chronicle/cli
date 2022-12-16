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
"""Unit tests for get.py."""

from typing import Any, Dict, Tuple
from unittest import mock

from click.testing import CliRunner

from forwarders.collectors.commands.get import get
from forwarders.collectors.tests.fixtures import *  # pylint: disable=wildcard-import

runner = CliRunner()


@mock.patch(
    "forwarders.collectors.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.get.click.prompt"
)
def test_collector_not_exist(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    collector_does_not_exist_response: Tuple[Dict[str, str], str]) -> None:
  """Test case to check whether collector exists or not.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    collector_does_not_exist_response (Tuple): Test data to fetch forwarder with
      no status code found.
  """

  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      collector_does_not_exist_response
  ]

  # Method Call.
  result = runner.invoke(get)
  assert "Collector does not exist.\n" in result.output


@mock.patch(
    "forwarders.collectors.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.get.click.prompt"
)
def test_collector_id_invalid(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    get_collector_id_invalid_response: Tuple[Dict[str, str], str]) -> None:
  """Test case to check whether collector exists or not.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    get_collector_id_invalid_response (Tuple): Test data to fetch forwarder with
      bad request status code.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      get_collector_id_invalid_response
  ]

  # Method Call.
  result = runner.invoke(get)
  assert ("Invalid Collector ID. Please enter valid Collector ID.\n"
         ) in result.output


@mock.patch(
    "forwarders.collectors.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.get.click.prompt"
)
def test_get_200(input_patch: mock.MagicMock, mock_client: mock.MagicMock,
                 get_collectors_response: Dict[str, Any]) -> None:
  """Test case to check response for 200 response code.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    get_collectors_response (Dict[str, Any]): Test data to fetch collectors.
  """
  mock_client.return_value = mock.Mock()
  input_patch.side_effect = ["123", "123"]
  mock_client.return_value.request.side_effect = [get_collectors_response]

  # Method Call.
  result = runner.invoke(get)
  assert """Collector Details:

ID: '123'
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
    "forwarders.collectors.commands.get.click.prompt"
)
def test_collector_id_absent(input_patch: mock.MagicMock) -> None:
  """Test case to check for input absent.

  Args:
    input_patch (mock.MagicMock): Mock object.
  """
  input_patch.side_effect = ["123", ""]

  # Method Call.
  result = runner.invoke(get)
  assert "Collector ID not provided. Please enter collector ID." in result.output


@mock.patch(
    "forwarders.collectors.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.get.click.prompt"
)
def test_get_server_error_code(input_patch: mock.MagicMock,
                               mock_client: mock.MagicMock,
                               collector_500_response: Dict[str, Any]) -> None:
  """Test case to check server error code.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    collector_500_response (Dict): Test data to fetch collector with server
      error status code.
  """
  input_patch.side_effect = ["123", "123"]
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [collector_500_response]

  # Method Call.
  result = runner.invoke(get)
  assert ("\nError while fetching collector.\nResponse Code: 500\nError: "
          "Internal Server Error") in result.output


@mock.patch(
    "forwarders.collectors.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.get.click.prompt"
)
def test_get_credential_file_invalid(input_patch: mock.MagicMock,
                                     mock_client: mock.MagicMock) -> None:
  """Test case for checking invalid credential path.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
  """
  mock_client.return_value = mock.Mock()
  input_patch.side_effect = ["123", "123"]
  mock_client.side_effect = OSError("Credential Path not found.")
  expected_message = "Failed with exception: Credential Path not found."

  result = runner.invoke(get, ["--credential_file", "my_dummy.json"])
  assert expected_message in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""

  # Method Call.
  result = runner.invoke(get)
  assert "Enter Forwarder ID:" in result.output


@mock.patch(
    "forwarders.collectors.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.get.click.prompt"
)
def test_get_verbose_option(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    get_collectors_response: Tuple[Dict[str, str], str]) -> None:
  """Test case to check response for 200 response code with verbose option.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    get_collectors_response (Tuple): Test data to fetch collectors.
  """
  mock_client.return_value = mock.Mock()
  input_patch.side_effect = ["123", "456"]
  mock_client.return_value.request.side_effect = [get_collectors_response]

  # Method Call.
  result = runner.invoke(get, ["--verbose"])
  assert """==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: https://backstory.googleapis.com/v2/forwarders/123/collectors/456
  Method: GET
  Body: None
Response:
  Body: {'name': '456', 'displayName': 'collector pqr', 'config': {'logType': 'Type of logs collected.', 'metadata': {'assetNamespace': 'test_namespace', 'labels': [{'key': 'my_key_1', 'value': 'my_value_1'}, {'key': 'my_key_2', 'value': 'my_value_2'}]}, 'regexFilter': [{'description': 'Describes what is being filtered and why', 'regexp': 'The regular expression used to match against each incoming line', 'behavior': 'ALLOW'}, {'description': 'Describes what is being filtered and why', 'regexp': 'The regular expression used to match against each incoming line', 'behavior': 'BLOCK'}], 'diskBuffer': {'state': 'ACTIVE', 'directoryPath': 'Directory path for files written.', 'maxFileBufferBytes': 3999}, 'maxSecondsPerBatch': 10, 'maxBytesPerBatch': 1048576, 'fileSettings': {'filePath': 'Path of file to monitor.'}}, 'state': 'ACTIVE'}""" in result.output


@mock.patch(
    "forwarders.collectors.commands.get.click.prompt"
)
def test_forwarder_id_absent(input_patch: mock.MagicMock) -> None:
  """Test case to check for input absent.

  Args:
    input_patch (mock.MagicMock): Mock object.
  """
  input_patch.return_value = ""

  # Method Call.
  result = runner.invoke(get)
  assert "Forwarder ID not provided. Please enter forwarder ID." in result.output
