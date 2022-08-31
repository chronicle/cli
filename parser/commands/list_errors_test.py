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
"""Unit tests for list_errors."""

import os
from typing import Dict
from unittest import mock

from click.testing import CliRunner

from common import file_utility
from common import uri
from mock_test_utility import MockResponse
from parser.commands.list_errors import list_errors
from parser.tests.fixtures import *  # pylint: disable=wildcard-import
from parser.tests.fixtures import TEMP_TEST_JSON_FILE
from parser.tests.fixtures import TEMP_TEST_TXT_FILE
from parser.tests.fixtures import TEST_DATA_DIR


runner = CliRunner()
TEST_LIST_ERRORS_URL = f"{uri.BASE_URL}/tools/cbnParsers:listCbnParserErrors?log_type=test_log_type&start_time=2022-08-01T00:00:00Z&end_time=2022-08-01T11:00:00Z"


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch(
    "parser.commands.list_errors.click.prompt"
)
def test_list_errors(input_patch: mock.MagicMock, mock_url: mock.MagicMock,
                     mock_client: mock.MagicMock,
                     error_list: Dict[str, str]) -> None:
  """Test case to check response for list errors.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    error_list (Tuple): Test input data.
  """
  mock_url.return_value = TEST_LIST_ERRORS_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [error_list]
  input_patch.side_effect = [
      "test_log_type", "2022-08-01T00:00:00Z", "2022-08-01T11:00:00Z"
  ]

  # Method Call
  result = runner.invoke(list_errors)
  assert """Getting parser errors...

Error Details:
  Error ID: test_error_id
  Config ID: test_config_id
  Log type: test_log_type
  Error Time: 2022-08-18T12:28:57.443376813Z
  Error Category: test_category
  Error Message: test_error_message
  Logs:
      test_logs

============================================================""" in result.output

  mock_url.assert_called_once_with(
      "US",
      "list_errors",
      "prod",
      log_type="test_log_type",
      start_time="2022-08-01T00:00:00Z",
      end_time="2022-08-01T11:00:00Z")


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch(
    "parser.commands.list_errors.click.prompt"
)
def test_list_errors_set_default_log_type(input_patch: mock.MagicMock,
                                          mock_url: mock.MagicMock,
                                          mock_client: mock.MagicMock,
                                          error_list: Dict[str, str]) -> None:
  """Test case to check set default log type.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    error_list (Tuple): Test input data.
  """
  mock_url.return_value = "{}/tools/cbnParsers:listCbnParserErrors?log_type=UNSPECIFIED_LOG_TYPE&start_time=2022-08-01T00:00:00Z&end_time=2022-08-01T11:00:00Z".format(
      uri.BASE_URL)
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [error_list]

  # Check whether default log type is set as `UNSPECIFIED_LOG_TYPE` in case log
  # type is not provided.
  input_patch.side_effect = ["", "2022-08-01T00:00:00Z", "2022-08-01T11:00:00Z"]
  runner.invoke(list_errors)
  mock_url.assert_called_once_with(
      "US",
      "list_errors",
      "prod",
      log_type="UNSPECIFIED_LOG_TYPE",
      start_time="2022-08-01T00:00:00Z",
      end_time="2022-08-01T11:00:00Z")

  # Check for empty start date.
  input_patch.side_effect = ["test_log_type", "", "2022-08-01T11:00:00Z"]
  result = runner.invoke(list_errors)
  assert "Please enter start date and end date." in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch(
    "parser.commands.list_errors.click.prompt"
)
def test_list_errors_500(
    input_patch: mock.MagicMock, mock_url: mock.MagicMock,
    mock_client: mock.MagicMock,
    test_500_resp: MockResponse) -> None:
  """Test case to check response for list errors for 500 response code.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    test_500_resp (Tuple): Test input data.
  """
  mock_url.return_value = TEST_LIST_ERRORS_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      test_500_resp
  ]
  input_patch.side_effect = [
      "test_log_type", "2022-08-01T00:00:00Z", "2022-08-01T11:00:00Z"
  ]
  result = runner.invoke(list_errors)
  assert """Getting parser errors...
Error while fetching list of errors for the given log type:
Response Code: 500
Error: test error""" in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch(
    "parser.commands.list_errors.click.prompt"
)
def test_list_errors_export_json(input_patch: mock.MagicMock,
                                 mock_url: mock.MagicMock,
                                 mock_client: mock.MagicMock,
                                 error_list: MockResponse) -> None:
  """Test case to check export option with JSON format for list errors command.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    error_list (MockResponse): Test input data.
  """
  mock_url.return_value = TEST_LIST_ERRORS_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [error_list]
  input_patch.side_effect = [
      "test_log_type", "2022-08-01T00:00:00Z", "2022-08-01T11:00:00Z"
  ]
  result = runner.invoke(
      list_errors,
      ["--export", f"{TEST_DATA_DIR}/test", "--file-format", "JSON"])
  assert f"""Parser Errors details exported successfully to:\
 {os.path.join(os.getcwd(), TEMP_TEST_JSON_FILE)}""" in result.output
  test_file_content = file_utility.read_file(TEMP_TEST_JSON_FILE)
  assert test_file_content.decode("utf-8") == """{
  "errors": [
    {
      "errorId": "test_error_id",
      "configId": "test_config_id",
      "logType": "test_log_type",
      "errorTime": "2022-08-18T12:28:57.443376813Z",
      "category": "test_category",
      "errorMsg": "test_error_message",
      "logs": [
        "test_logs"
      ]
    }
  ]
}"""


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parser.url.get_url")
@mock.patch(
    "parser.commands.list_errors.click.prompt"
)
def test_list_errors_export_txt(input_patch: mock.MagicMock,
                                mock_url: mock.MagicMock,
                                mock_client: mock.MagicMock,
                                error_list: MockResponse) -> None:
  """Test case to check export option with TXT format for list errors command.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    error_list (MockResponse): Test input data.
  """
  mock_url.return_value = TEST_LIST_ERRORS_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [error_list]
  input_patch.side_effect = [
      "test_log_type", "2022-08-01T00:00:00Z", "2022-08-01T11:00:00Z"
  ]
  result = runner.invoke(list_errors, ["--export", f"{TEST_DATA_DIR}/test"])
  assert f"""Parser Errors details exported successfully to:\
 {os.path.join(os.getcwd(), TEMP_TEST_TXT_FILE)}""" in result.output
  test_file_content = file_utility.read_file(TEMP_TEST_TXT_FILE)
  assert test_file_content.decode("utf-8") == """
Error Details:
  Error ID: test_error_id
  Config ID: test_config_id
  Log type: test_log_type
  Error Time: 2022-08-18T12:28:57.443376813Z
  Error Category: test_category
  Error Message: test_error_message
  Logs:
      test_logs

============================================================
"""


def test_prompt_text() -> None:
  """Test case to check prompt text."""
  result = runner.invoke(list_errors)
  assert "Enter Log Type:" in result.output
  assert "Enter Start Date (Format: yyyy-mm-ddThh:mm:ssZ):" in result.output
  assert "Enter End Date (Format: yyyy-mm-ddThh:mm:ssZ):" in result.output
