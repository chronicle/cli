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
"""Tests for history.py."""

from unittest import mock

from click.testing import CliRunner

from common import uri
from mock_test_utility import MockResponse
from parser import url
from parser.commands.history import history
from parser.tests.fixtures import *  # pylint: disable=wildcard-import


runner = CliRunner()

TEST_HISTORY_URL = f"{uri.BASE_URL}/tools/cbnParsers:listCbnParserHistory?log_type=TEST_LOG_TYPE"


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch(
    "parser.commands.history.click.prompt")
def test_history_command(mock_input: mock.MagicMock, mock_url: mock.MagicMock,
                         mock_client: mock.MagicMock,
                         test_history_data: MockResponse,
                         test_data_list_command: MockResponse) -> None:
  """Test case to check response for list parsers history.

  Args:
    mock_input (mock.MagicMock): Mock object
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_history_data (MockResponse): Test input data
    test_data_list_command (MockResponse): Test input data
  """
  mock_input.return_value = "TEST_LOG_TYPE"
  mock_url.return_value = TEST_HISTORY_URL

  # Check for non-empty response.
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_history_data]
  result = runner.invoke(history)
  assert """Fetching history for parser...

Parser History:
  Config ID: test_config_id
  Log type: TEST_LOG_TYPE
  State: LIVE
  SHA256: test_sha256
  Author: test_user
  Submit Time: 2022-04-01T08:08:44.217797Z
  State Last Changed Time: 2022-04-01T08:08:44.217797Z
  Validation Errors:
    Error:
      test error 1
    Log:
      test log 1
    --------------------------------------------------------
    Error:
      test error 2

============================================================

""" in result.output
  mock_url.assert_called_once_with(
      "US", "history", "prod", log_type="TEST_LOG_TYPE")
  mock_client.return_value.request.assert_called_once_with(
      "GET",
      TEST_HISTORY_URL,
      headers=url.HTTP_REQUEST_HEADERS,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)

  # Check for successful submitted parser's history.
  mock_client.return_value.request.side_effect = [test_data_list_command]
  result = runner.invoke(history)
  assert """Fetching history for parser...

Parser History:
  Config ID: test_config_id
  Log type: TEST_LOG_TYPE
  State: LIVE
  SHA256: test_sha256
  Author: test_user
  Submit Time: 2022-04-01T08:08:44.217797Z
  State Last Changed Time: 2022-04-01T08:08:44.217797Z
  Last Live Time: 2022-04-01T08:08:44.217797Z

============================================================

""" in result.output

  # Check for empty response.
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=200, text="""{}""")
  ]
  result = runner.invoke(history)
  assert """No CBN parser currently configured.""" in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch(
    "parser.commands.history.click.prompt")
def test_history_500_error(mock_input: mock.MagicMock, mock_url: mock.MagicMock,
                           mock_client: mock.MagicMock,
                           test_500_resp: MockResponse) -> None:
  """Test case to check history command for 500 response code.

  Args:
    mock_input (mock.MagicMock): Mock object
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_500_resp (MockResponse): Test input data
  """
  mock_input.return_value = "TEST_LOG_TYPE"
  mock_url.return_value = TEST_HISTORY_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_500_resp]
  result = runner.invoke(history)
  assert """Fetching history for parser...
Error while fetching history for parser.
Response Code: 500
Error: test error
""" in result.output
  mock_url.assert_called_once_with(
      "US", "history", "prod", log_type="TEST_LOG_TYPE")
  mock_client.return_value.request.assert_called_once_with(
      "GET",
      TEST_HISTORY_URL,
      headers=url.HTTP_REQUEST_HEADERS,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)


@mock.patch(
    "parser.commands.history.click.prompt")
def test_history_empty_log_type(mock_input: mock.MagicMock) -> None:
  """Test case to check the console output if no input provided for log type.

  Args:
    mock_input (mock.MagicMock): Mock object
  """
  mock_input.return_value = ""
  result = runner.invoke(history)
  assert """Log type not provided. Please enter log type.""" in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""
  result = runner.invoke(history)
  assert "Enter Log Type:" in result.output
