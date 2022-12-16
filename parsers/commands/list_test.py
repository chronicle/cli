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
"""Tests for list.py."""

import os
from unittest import mock

from click._compat import WIN
from click.testing import CliRunner

from common import file_utility
from mock_test_utility import MockResponse
from parsers import url
from parsers.commands.list import list_command
from parsers.tests.fixtures import *  # pylint: disable=wildcard-import
from parsers.tests.fixtures import TEMP_TEST_JSON_FILE
from parsers.tests.fixtures import TEMP_TEST_TXT_FILE
from parsers.tests.fixtures import TEST_DATA_DIR


runner = CliRunner()
LIST_URL = url.get_url("", "list", "prod")


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
def test_list_command(mock_url: mock.MagicMock, mock_client: mock.MagicMock,
                      test_data_list_command: MockResponse) -> None:
  """Test case to check response for list parsers.

  Args:
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_data_list_command (MockResponse): Test input data
  """
  mock_url.return_value = LIST_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_data_list_command]
  result = runner.invoke(list_command, ["--env", "PROD"])
  assert """Fetching list of parsers...

Parser Details:
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
  mock_url.assert_called_once_with("US", "list", "prod")
  mock_client.return_value.request.assert_called_once_with(
      "GET", LIST_URL, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
def test_list_command_empty_response(mock_url: mock.MagicMock,
                                     mock_client: mock.MagicMock) -> None:
  """Test case to check empty response for list parsers.

  Args:
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_url.return_value = LIST_URL
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=200, text="""{}""")
  ]
  result = runner.invoke(list_command)
  assert """No CBN parsers currently configured.""" in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
def test_list_command_500(mock_url: mock.MagicMock, mock_client: mock.MagicMock,
                          test_500_resp: MockResponse) -> None:
  """Test case to check response for list parsers for 500 response code.

  Args:
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_500_resp (MockResponse): Test input data
  """
  mock_url.return_value = LIST_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_500_resp]
  result = runner.invoke(list_command, ["--env", "PROD"])
  assert """Fetching list of parsers...
Error while fetching list of parsers.
Response Code: 500
Error: test error
""" in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
def test_list_command_missing_key(
    mock_url: mock.MagicMock, mock_client: mock.MagicMock,
    test_data_list_cmd_missing_key: MockResponse) -> None:
  """Test case to verify if key is missing from one of the parser details dict.

  Args:
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_data_list_cmd_missing_key (MockResponse): Test input data
  """
  mock_url.return_value = LIST_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      test_data_list_cmd_missing_key
  ]
  result = runner.invoke(list_command)
  assert """Fetching list of parsers...

Parser Details:
  Config ID: config 1
  Log type: TEST_LOG_TYPE
  State: LIVE
  SHA256: test_sha256
  Author: test_user
  Submit Time: 2022-04-01T08:08:44.217797Z
  State Last Changed Time: 2022-04-01T08:08:44.217797Z
  Last Live Time: 2022-04-01T08:08:44.217797Z

============================================================

Key 'configId' not found in the response.

============================================================

Parser Details:
  Config ID: config 2
  Log type: TEST_LOG_TYPE
  State: LIVE
  SHA256: test_sha256
  Author: test_user
  Submit Time: 2022-04-01T08:08:44.217797Z
  State Last Changed Time: 2022-04-01T08:08:44.217797Z
  Last Live Time: 2022-04-01T08:08:44.217797Z

============================================================

""" in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
def test_list_command_exception(mock_url: mock.MagicMock,
                                mock_client: mock.MagicMock) -> None:
  """Test case to verify console output in case of exception.

  Args:
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_url.return_value = LIST_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = Exception("test error message")
  result = runner.invoke(list_command)
  assert """Fetching list of parsers...
Failed with exception: test error message
""" in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
def test_list_command_export(mock_url: mock.MagicMock,
                             mock_client: mock.MagicMock,
                             test_data_list_command: MockResponse) -> None:
  """Test case to check export option with TXT file format for list command.

  Args:
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_data_list_command (MockResponse): Test input data
  """
  mock_url.return_value = LIST_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_data_list_command]
  result = runner.invoke(list_command, ["--export", f"{TEST_DATA_DIR}/test"])
  assert f"""Parser details exported successfully to:\
 {os.path.join(os.getcwd(), TEMP_TEST_TXT_FILE)}""" in result.output
  output = file_utility.read_file(TEMP_TEST_TXT_FILE)
  output = output.decode("utf-8")

  # "\n" is the Unix/linux for new line whereas "\r\n" is the default Windows
  # style for line separator. Hence, below condition is to handle the tests for
  # Windows OS platform.
  if WIN:
    output = "\n".join(output.splitlines()) + "\n"

  assert output == """\

Parser Details:
  Config ID: test_config_id
  Log type: TEST_LOG_TYPE
  State: LIVE
  SHA256: test_sha256
  Author: test_user
  Submit Time: 2022-04-01T08:08:44.217797Z
  State Last Changed Time: 2022-04-01T08:08:44.217797Z
  Last Live Time: 2022-04-01T08:08:44.217797Z

============================================================
"""


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
def test_list_command_export_json(mock_url: mock.MagicMock,
                                  mock_client: mock.MagicMock,
                                  test_data_list_command: MockResponse) -> None:
  """Test case to check export option with JSON format for list command.

  Args:
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_data_list_command (MockResponse): Test input data
  """
  mock_url.return_value = LIST_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_data_list_command]
  result = runner.invoke(
      list_command,
      ["--export", f"{TEST_DATA_DIR}/test", "--file-format", "JSON"])
  assert f"""Parser details exported successfully to:\
 {os.path.join(os.getcwd(), TEMP_TEST_JSON_FILE)}""" in result.output
  test_file_content = file_utility.read_file(TEMP_TEST_JSON_FILE)
  test_file_content = test_file_content.decode("utf-8")

  # "\n" is the Unix/linux for new line whereas "\r\n" is the default Windows
  # style for line separator. Hence, below condition is to handle the tests for
  # Windows OS platform.
  if WIN:
    test_file_content = "\n".join(test_file_content.splitlines())

  assert test_file_content == """{
  "cbnParsers": [
    {
      "configId": "test_config_id",
      "author": "test_user",
      "state": "LIVE",
      "sha256": "test_sha256",
      "logType": "TEST_LOG_TYPE",
      "submitTime": "2022-04-01T08:08:44.217797Z",
      "lastLiveTime": "2022-04-01T08:08:44.217797Z",
      "stateLastChangedTime": "2022-04-01T08:08:44.217797Z"
    }
  ]
}"""
