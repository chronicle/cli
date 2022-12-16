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
"""Tests for status."""

from unittest import mock

from click.testing import CliRunner

from common import uri
from mock_test_utility import MockResponse
from parsers import url
from parsers.commands.status import status_command
from parsers.tests.fixtures import *  # pylint: disable=wildcard-import


runner = CliRunner()


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "parsers.commands.status.click.prompt")
def test_status_parser(mock_input: mock.MagicMock, mock_client: mock.MagicMock,
                       status_parser: MockResponse) -> None:
  """Test case to check response for status of parser.

  Args:
    mock_input (mock.MagicMock): Mock prompt object.
    mock_client (mock.MagicMock): Mock object.
    status_parser (Tuple): Test input data.
  """
  mock_input.side_effect = ["test_config_id"]
  # Check for non-empty response.
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [status_parser]
  result = runner.invoke(status_command)
  assert """Getting parser...

Parser Details:
  Config ID: test_config_id
  Log type: TEST_LOG_TYPE
  State: LIVE
  SHA256: test_sha256
  Author: test_user
  Submit Time: 2022-04-01T08:08:44.217797Z
  State Last Changed Time: 2022-04-01T08:08:44.217797Z
  Last Live Time: 2022-04-01T08:08:44.217797Z
""" in result.output
  mock_client.return_value.request.assert_called_once_with(
      "GET",
      f"{uri.BASE_URL}/v1/tools/cbnParsers/test_config_id",
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)


@mock.patch(
    "parsers.commands.status.click.prompt")
def test_prompt_required(mock_input: mock.MagicMock) -> None:
  """Test case to check prompt text.

  Args:
    mock_input (mock.MagicMock): Mock prompt object.
  """
  mock_input.side_effect = [""]
  result = runner.invoke(status_command)
  assert "Please enter config id." in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
@mock.patch(
    "parsers.commands.status.click.prompt")
def test_status_parser_400(mock_input: mock.MagicMock, mock_url: mock.MagicMock,
                           mock_client: mock.MagicMock,
                           test_400_resp_status_command: MockResponse) -> None:
  """Test case to check response for status of parser for 500 response code.

  Args:
    mock_input (mock.MagicMock): Mock prompt object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    test_400_resp_status_command (Tuple): Test response data.
  """
  mock_input.side_effect = ["test_config_id"]
  mock_url.return_value = f"{uri.BASE_URL}/tools/cbnParsers"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_400_resp_status_command]
  result = runner.invoke(status_command)
  assert """Getting parser...
Error while fetching status for parser.
Response Code: 400
Error: Invalid ID.
""" in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
@mock.patch(
    "parsers.commands.status.click.prompt")
def test_status_parser_500(mock_input: mock.MagicMock, mock_url: mock.MagicMock,
                           mock_client: mock.MagicMock,
                           test_500_resp_status_command: MockResponse) -> None:
  """Test case to check response for status of parser for 500 response code.

  Args:
    mock_input (mock.MagicMock): Mock prompt object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    test_500_resp_status_command (Tuple): Test response data.
  """
  mock_input.side_effect = ["test_config_id"]
  mock_url.return_value = f"{uri.BASE_URL}/tools/cbnParsers"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_500_resp_status_command]
  result = runner.invoke(status_command)
  assert """Getting parser...
Error while fetching status for parser.
Response Code: 500
Error: could not get CBN parser.
""" in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""
  result = runner.invoke(status_command)
  assert "Enter Config ID:" in result.output
