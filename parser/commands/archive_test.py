# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Tests for archive.py."""

from unittest import mock

from click.testing import CliRunner

from common import uri
from mock_test_utility import MockResponse
from parser import url
from parser.commands.archive import archive
from parser.tests.fixtures import *  # pylint: disable=wildcard-import


runner = CliRunner()
TEST_ARCHIVE_URL = f"{uri.BASE_URL}/tools/cbnParsers/test_config_id:archive"


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch(
    "parser.commands.archive.click.prompt")
def test_archive_parser(mock_input: mock.MagicMock, mock_url: mock.MagicMock,
                        mock_client: mock.MagicMock,
                        test_archive_data: MockResponse) -> None:
  """Test case to check response for status of parser.

  Args:
    mock_input (mock.MagicMock): Mock prompt object
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_archive_data (Tuple): Test input data
  """
  mock_url.return_value = f"{uri.BASE_URL}/tools/cbnParsers"
  mock_input.side_effect = ["test_config_id"]
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_archive_data]
  result = runner.invoke(archive)
  assert """Archiving parser...

Parser archived successfully.

Parser Details:
  Config ID: test_config_id
  Log type: TEST_LOG_TYPE
  State: ARCHIVED
  SHA256: test_sha256
  Author: test_user
  Submit Time: 2022-04-01T08:08:44.217797Z
  State Last Changed Time: 2022-04-01T08:08:44.217797Z
  Last Live Time: 2022-04-01T08:08:44.217797Z
""" in result.output
  mock_url.assert_called_once_with("US", "list", "prod")
  mock_client.return_value.request.assert_called_once_with(
      "POST", TEST_ARCHIVE_URL, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch(
    "parser.commands.archive.click.prompt")
def test_archive_parser_500(mock_input: mock.MagicMock,
                            mock_url: mock.MagicMock,
                            mock_client: mock.MagicMock,
                            test_500_resp: MockResponse) -> None:
  """Test case to check response for archive parser 500 response code.

  Args:
    mock_input (mock.MagicMock): Mock prompt object
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_500_resp (Tuple): Test response data
  """
  mock_input.side_effect = ["test_config_id"]
  mock_url.return_value = TEST_ARCHIVE_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_500_resp]
  result = runner.invoke(archive)
  assert """Archiving parser...
Error while archiving parser.
Response Code: 500
Error: test error
""" in result.output


@mock.patch(
    "parser.commands.history.click.prompt")
def test_archive_empty_log_type(mock_input: mock.MagicMock) -> None:
  """Test case to check the console output if no input provided for log type.

  Args:
    mock_input (mock.MagicMock): Mock object
  """
  mock_input.return_value = ""
  result = runner.invoke(archive)
  assert """Config ID not provided. Please enter Config ID.""" in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""
  result = runner.invoke(archive)
  assert "Enter Config ID:" in result.output
