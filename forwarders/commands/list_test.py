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
  mock_client.return_value.request.side_effect = [list_empty_forwarders_data]
  result = runner.invoke(list_command)
  assert result.output == "No forwarders found.\n"


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
  mock_client.return_value.request.side_effect = [list_error_forwarders_data]
  result = runner.invoke(list_command)
  assert "Failed to list forwarders." in result.output


@mock.patch(
    "forwarders.commands.list.chronicle_auth.initialize_http_session"
)
def test_list_200(mock_client: mock.MagicMock,
                  list_forwarder_data: Dict[str, Any]) -> None:
  """Test case to check response for 200 response code.

  Args:
    mock_client (mock.MagicMock): Mock object
    list_forwarder_data (Tuple): Test data to fetch forwarder.
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [list_forwarder_data]
  result = runner.invoke(list_command)
  assert """================================================================================
(Forwarder [asdf1234-1234-abcd-efgh-12345678abcd])

Name: forwarders/asdf1234-1234-abcd-efgh-12345678abcd
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
        Unready status code: 43""" in result.output


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
