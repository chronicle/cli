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
"""Unit tests for submit a new parser."""

import base64
from unittest import mock
import urllib


from click.testing import CliRunner

from common import uri
from mock_test_utility import MockResponse
from parsers import url
from parsers.commands.submit import submit
from parsers.tests.fixtures import *  # pylint: disable=wildcard-import
from parsers.tests.fixtures import create_temp_config_file
from parsers.tests.fixtures import TEMP_SUBMIT_CONF_FILE

runner = CliRunner()
TEST_SUBMIT_URL = f"{uri.BASE_URL}/tools/cbnParsers"


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
@mock.patch(
    "parsers.commands.submit.click.prompt")
def test_submit_parser(input_patch: mock.MagicMock, mock_url: mock.MagicMock,
                       mock_client: mock.MagicMock,
                       submit_parser: MockResponse) -> None:
  """Test case to check response for submit a new parser.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    submit_parser (Tuple): Test input data.
  """
  create_temp_config_file(TEMP_SUBMIT_CONF_FILE, "test_config")
  mock_url.return_value = TEST_SUBMIT_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [submit_parser]
  input_patch.side_effect = [
      "test_log_type", TEMP_SUBMIT_CONF_FILE, "test_author", False
  ]

  # Method Call
  result = runner.invoke(submit)
  assert """Submitting parser...

Submitted Parser Details:
  Config ID: test_config_id
  Log type: TEST_LOG_TYPE
  State: LIVE
  SHA256: test_sha256
  Author: test_user
  Submit Time: 2022-04-01T08:08:44.217797Z
  State Last Changed Time: 2022-04-01T08:08:44.217797Z
  

Parser submitted successfully. To get status of the parser, run this command using following Config ID - test_config_id:
`chronicle_cli parsers status`""" in result.output
  data = {
      "log_type": "test_log_type",
      "config": base64.urlsafe_b64encode("test_config".encode()),
      "author": "test_author",
      "skipValidationOnNoLogs": False,
  }
  request_body = urllib.parse.urlencode(data)
  mock_client.return_value.request.assert_called_once_with(
      "POST",
      TEST_SUBMIT_URL,
      request_body,
      headers=url.HTTP_REQUEST_HEADERS,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS
  )


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
@mock.patch(
    "parsers.commands.submit.click.prompt")
def test_submit_parser_skip_valiadtion(
    input_patch: mock.MagicMock, mock_url: mock.MagicMock,
    mock_client: mock.MagicMock,
    submit_parser: MockResponse) -> None:
  """Test case to check response for submit a new parser.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    submit_parser (Tuple): Test input data.
  """
  create_temp_config_file(TEMP_SUBMIT_CONF_FILE, "test_config")
  mock_url.return_value = TEST_SUBMIT_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [submit_parser]
  input_patch.side_effect = [
      "test_log_type", TEMP_SUBMIT_CONF_FILE, "test_author", True
  ]

  # Method Call
  result = runner.invoke(submit)
  assert """Submitting parser...

Submitted Parser Details:
  Config ID: test_config_id
  Log type: TEST_LOG_TYPE
  State: LIVE
  SHA256: test_sha256
  Author: test_user
  Submit Time: 2022-04-01T08:08:44.217797Z
  State Last Changed Time: 2022-04-01T08:08:44.217797Z
  

Parser submitted successfully. To get status of the parser, run this command using following Config ID - test_config_id:
`chronicle_cli parsers status`""" in result.output
  data = {
      "log_type": "test_log_type",
      "config": base64.urlsafe_b64encode("test_config".encode()),
      "author": "test_author",
      "skipValidationOnNoLogs": True,
  }
  request_body = urllib.parse.urlencode(data)
  mock_client.return_value.request.assert_called_once_with(
      "POST",
      TEST_SUBMIT_URL,
      request_body,
      headers=url.HTTP_REQUEST_HEADERS,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS
  )


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
@mock.patch(
    "parsers.commands.submit.click.prompt")
def test_config_file_not_exist(input_patch: mock.MagicMock,
                               mock_url: mock.MagicMock,
                               mock_client: mock.MagicMock) -> None:
  """Test case to check response for config file does not exist.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
  """
  mock_url.return_value = TEST_SUBMIT_URL
  mock_client.return_value = mock.Mock()

  # Check for config file does not exist.
  input_patch.side_effect = [
      "test_log_type", "test_config_file.conf", "test_author", False
  ]
  result = runner.invoke(submit)
  assert ("test_config_file.conf does not exist. "
          "Please enter valid config file path.") in result.output

  # Check for log type, config file and author all three parameters are
  # required.
  input_patch.side_effect = ["", "", "test_author", False]
  result = runner.invoke(submit)
  assert ("Log Type, Config file path and Author fields are required. "
          "Please enter value for the missing field(s).") in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
@mock.patch(
    "parsers.commands.submit.click.prompt")
def test_submit_parser_500(input_patch: mock.MagicMock,
                           mock_url: mock.MagicMock,
                           mock_client: mock.MagicMock,
                           test_500_resp: MockResponse) -> None:
  """Test case to check response for submit parser for 500 response code.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    test_500_resp (Tuple): Test input data.
  """
  create_temp_config_file(TEMP_SUBMIT_CONF_FILE, "test_config")
  mock_url.return_value = TEST_SUBMIT_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_500_resp]
  input_patch.side_effect = [
      "test_log_type", TEMP_SUBMIT_CONF_FILE, "test_author", False
  ]
  result = runner.invoke(submit, ["--env", "PROD"])
  assert """Submitting parser...
Error while submitting parser:
Response Code: 500
Error: test error""" in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""
  result = runner.invoke(submit)
  assert "Enter Log type:" in result.output
  assert "Enter Config file path:" in result.output
  assert "Enter author:" in result.output
