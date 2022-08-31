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
"""Tests for run.py."""

from unittest import mock

from click.testing import CliRunner

from mock_test_utility import MockResponse
from parser.commands.run import run
from parser.tests.fixtures import *  # pylint: disable=wildcard-import


runner = CliRunner()


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch("common.file_utility.read_file")
@mock.patch("parser.commands.run.click.prompt"
           )
def test_run_command(mock_input: mock.MagicMock, mock_read_file: mock.MagicMock,
                     mock_url: mock.MagicMock, mock_client: mock.MagicMock,
                     test_run_validation_data: MockResponse) -> None:
  """Test case to check response for run parsers.

  Args:
    mock_input: Mock object
    mock_read_file: Mock object
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_run_validation_data (Tuple): Test input data
  """
  mock_input.side_effect = ["path1", "path2"]
  mock_read_file.side_effect = [b"conf", b"log"]
  mock_url.return_value = "test_url"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_run_validation_data]
  result = runner.invoke(run)
  assert """Running Validation...
result 1
result 2
""" in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch("common.file_utility.read_file")
@mock.patch("parser.commands.run.time.time")
@mock.patch("parser.commands.run.click.prompt"
           )
def test_run_command_error(
    mock_input: mock.MagicMock, mock_time: mock.MagicMock,
    mock_read_file: mock.MagicMock, mock_url: mock.MagicMock,
    mock_client: mock.MagicMock,
    test_run_validation_error_data: MockResponse) -> None:
  """Test case to check response for run parsers in case of error.

  Args:
    mock_input: Mock object
    mock_time: Mock object
    mock_read_file: Mock object
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_run_validation_error_data (Tuple): Test input data
  """
  mock_input.side_effect = ["path1", "path2"]
  mock_time.side_effect = [2.1, 5.2]
  mock_read_file.side_effect = [b"conf", b"log"]
  mock_url.return_value = "test_url"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      test_run_validation_error_data
  ]
  result = runner.invoke(run)
  assert """Running Validation...
test error
sample log
Runtime: 3.1s
""" in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch("common.file_utility.read_file")
@mock.patch("parser.commands.run.click.prompt"
           )
def test_run_command_500(mock_input: mock.MagicMock,
                         mock_read_file: mock.MagicMock,
                         mock_url: mock.MagicMock, mock_client: mock.MagicMock,
                         test_500_resp: MockResponse) -> None:
  """Test case to check response for run parsers in case of 500 response code.

  Args:
    mock_input: Mock object
    mock_read_file: Mock object
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_500_resp (Tuple): Test input data
  """
  mock_input.side_effect = ["path1", "path2"]
  mock_read_file.side_effect = [b"conf", b"log"]
  mock_url.return_value = "test_url"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_500_resp]
  result = runner.invoke(run)
  assert """Running Validation...
Error while running validation.
Response Code: 500
Error: test error
""" in result.output
