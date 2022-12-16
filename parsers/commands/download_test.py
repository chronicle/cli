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
"""Unit tests for download parser."""

from unittest import mock

from click.testing import CliRunner

from common import uri
from mock_test_utility import MockResponse
from parsers.commands.download import download
from parsers.tests.fixtures import *  # pylint: disable=wildcard-import
from parsers.tests.fixtures import TEMP_CONF_FILE
from parsers.tests.fixtures import TEST_DATA_DIR


runner = CliRunner()
TEST_DOWNLOAD_URL = f"{uri.BASE_URL}/tools/cbnParsers/test_config_id"


@mock.patch(
    "parsers.constants.path_constants.PARSER_DATA_DIR",
    TEST_DATA_DIR)
@mock.patch("parsers.commands.download.time")
@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
@mock.patch(
    "parsers.commands.download.click.prompt")
def test_download_parser_by_config_id(input_patch: mock.MagicMock,
                                      mock_url: mock.MagicMock,
                                      mock_client: mock.MagicMock,
                                      mock_time: mock.MagicMock) -> None:
  """Test case to check response for download parser by config ID.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    mock_time (mock.MagicMock): Mock object.
  """
  mock_url.return_value = TEST_DOWNLOAD_URL
  mock_client.return_value = mock.Mock()
  mock_time.strftime.return_value = "20220824062200"
  mock_client.return_value.request.side_effect = [
      MockResponse(
          status_code=200,
          text="""{
    "configId": "test_config_id",
    "logType": "test_log_type",
    "config": "dGVzdF9jb25maWc="
  }""")
  ]
  input_patch.side_effect = ["test_config_id"]

  # Method Call
  result = runner.invoke(download)
  assert f"Writing parser to: {TEMP_CONF_FILE}" in result.output
  with open(TEMP_CONF_FILE, "r") as f:
    assert "test_config" in f.read()


@mock.patch(
    "parsers.constants.path_constants.PARSER_DATA_DIR",
    TEST_DATA_DIR)
@mock.patch("parsers.commands.download.time")
@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
@mock.patch(
    "parsers.commands.download.click.prompt")
def test_download_parser_by_log_type(input_patch: mock.MagicMock,
                                     mock_url: mock.MagicMock,
                                     mock_client: mock.MagicMock,
                                     mock_time: mock.MagicMock) -> None:
  """Test case to check response for download parser by log type.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    mock_time (mock.MagicMock): Mock object.
  """
  mock_url.return_value = TEST_DOWNLOAD_URL
  mock_client.return_value = mock.Mock()
  mock_time.strftime.return_value = "20220824062200"
  mock_client.return_value.request.side_effect = [
      MockResponse(
          status_code=200,
          text="""{"cbnParsers": [
              {"configId": "test_config_id",
                "logType": "test_log_type", 
                  "config": "dGVzdF9jb25maWc="}
                  ]}""")
  ]
  input_patch.side_effect = ["", "test_log_type"]

  # Method Call
  result = runner.invoke(download)
  assert f"Writing parser to: {TEMP_CONF_FILE}" in result.output
  with open(TEMP_CONF_FILE, "r") as f:
    assert "test_config" in f.read()


@mock.patch("parsers.commands.download.time")
@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
@mock.patch(
    "parsers.commands.download.click.prompt")
def test_parser_not_found(input_patch: mock.MagicMock, mock_url: mock.MagicMock,
                          mock_client: mock.MagicMock,
                          mock_time: mock.MagicMock) -> None:
  """Test case to check parser not found for given log type.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    mock_time (mock.MagicMock): Mock object.
  """
  mock_url.return_value = TEST_DOWNLOAD_URL
  mock_client.return_value = mock.Mock()
  mock_time.strftime.return_value = "20220824062200"
  mock_client.return_value.request.side_effect = [
      MockResponse(
          status_code=200,
          text="""{"cbnParsers": [
              {"configId": "test_config_id",
                "logType": "test_unspecified_log_type", 
                  "config": "dGVzdF9jb25maWc="}
                  ]}""")
  ]
  input_patch.side_effect = ["", "test_log_type"]

  # Check for Parser not found for given log type.
  result = runner.invoke(download)
  assert """Parser for log type test_log_type not found.""" in result.output

  # Check for No parsers configured.
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=200, text="""{}""")
  ]
  input_patch.side_effect = ["", "test_log_type"]

  result = runner.invoke(download)
  assert """No CBN parsers currently configured.""" in result.output


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("parsers.url.get_url")
@mock.patch(
    "parsers.commands.download.click.prompt")
def test_download_parser_500(
    input_patch: mock.MagicMock, mock_url: mock.MagicMock,
    mock_client: mock.MagicMock,
    test_500_resp: MockResponse) -> None:
  """Test case to check response for download parser for 500 response code.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_url (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    test_500_resp (Tuple): Test input data.
  """
  mock_url.return_value = TEST_DOWNLOAD_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      test_500_resp
  ]
  input_patch.side_effect = ["test_config_id", ""]

  result = runner.invoke(download, ["--env", "PROD"])
  assert """Note: If you want to download parser by log type then skip the config ID.
Downloading parser...
Error while downloading parser:
Response Code: 500
Error: test error""" in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""
  result = runner.invoke(download)
  assert "Enter config ID:" in result.output
