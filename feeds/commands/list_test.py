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
"""Unit test cases for list.py."""

from typing import Dict, Tuple
from unittest import mock

from click.testing import CliRunner

from feeds.commands.list import list_command
from feeds.tests.fixtures import *  # pylint: disable=wildcard-import
from feeds.tests.fixtures import TEMP_EXPORT_CSV_FILE
from feeds.tests.fixtures import TEMP_EXPORT_JSON_FILE
from feeds.tests.fixtures import TEMP_EXPORT_TXT_FILE
from mock_test_utility import MockResponse

runner = CliRunner()


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_list_no_feeds_found(mock_client: mock.MagicMock,
                             list_empty_feeds_data: Dict[str, str]) -> None:
  """Check for empty list of feeds.

  Args:
    mock_client (mock.MagicMock): Mock object
    list_empty_feeds_data (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=200, text="""{"feedSourceTypeSchemas": []}"""),
      list_empty_feeds_data
  ]
  # Method Call
  result = runner.invoke(list_command)
  assert result.output == "No feeds found.\n"


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_list_200(mock_client: mock.MagicMock, get_feed_schema: Dict[str, str],
                  list_feeds_data: Dict[str, str]) -> None:
  """Test case to check response for 200 response code.

  Args:
    mock_client (mock.MagicMock): Mock object
    get_feed_schema (Tuple): Test input data
    list_feeds_data (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema, list_feeds_data
  ]

  # Method Call
  result = runner.invoke(list_command)
  assert """
Feed Details:
  ID: 123
  Display Name: Dummy feed display name
  Source type: Dummy Source Type
  Log type: Dummy LogType
  State: INACTIVE
  Feed Settings:
    Field 1: abc.dummy.com
    Field 2: ID
  Namespace: sample_namespace
  Labels:
    k: v

============================================================
""" in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_list_empty_schema(mock_client: mock.MagicMock,
                           list_feeds_data: Dict[str, str]) -> None:
  """Test case to check response for empty schema.

  Args:
    mock_client (mock.MagicMock): Mock object
    list_feeds_data (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=200, text="""{"feedSourceTypeSchemas": []}"""),
      list_feeds_data
  ]

  # Method Call
  result = runner.invoke(list_command)
  assert "Schema Not Found." in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
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


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_list_export_csv(mock_client: mock.MagicMock,
                         get_feed_schema: Dict[str, str],
                         list_feeds_data: Dict[str, str]) -> None:
  """Test case to check feed list details exported in csv format.

  Args:
    mock_client (mock.MagicMock): Mock object
    get_feed_schema (Tuple): Test input data
    list_feeds_data (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema, list_feeds_data
  ]

  # Method Call
  result = runner.invoke(
      list_command,
      ["--export", TEMP_EXPORT_CSV_FILE[:-4], "--file-format", "csv"])
  assert "Feed list details exported successfully" in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_list_export_txt(mock_client: mock.MagicMock,
                         get_feed_schema: Dict[str, str],
                         list_feeds_data: Dict[str, str]) -> None:
  """Test case to check feed list details exported in txt format.

  Args:
    mock_client (mock.MagicMock): Mock object
    get_feed_schema (Tuple): Test input data
    list_feeds_data (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema, list_feeds_data
  ]

  # Method Call
  result = runner.invoke(
      list_command,
      ["--export", TEMP_EXPORT_TXT_FILE[:-4], "--file-format", "txt"])
  assert "Feed list details exported successfully" in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_list_error_code(
    mock_client: mock.MagicMock, list_error_feeds_data: Tuple[Dict[str, str],
                                                              str]) -> None:
  """Check for empty list of feeds.

  Args:
    mock_client (mock.MagicMock): Mock object
    list_error_feeds_data (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=200, text="""{"feedSourceTypeSchemas": []}"""),
      list_error_feeds_data
  ]
  # Method Call
  result = runner.invoke(list_command)
  assert "Failed to find feeds." in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_list_key_missing(mock_client: mock.MagicMock,
                          get_feed_schema: Dict[str, str],
                          list_missing_key_feeds_data: Dict[str, str]) -> None:
  """Test case to check response for 200 response code.

  Args:
    mock_client (mock.MagicMock): Mock object
    get_feed_schema (Tuple): Test input data
    list_missing_key_feeds_data (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema, list_missing_key_feeds_data
  ]

  # Method Call
  result = runner.invoke(list_command)
  assert "Field 1: abc.dummy.com" in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_list_export_json(mock_client: mock.MagicMock,
                          get_feed_schema: Dict[str, str],
                          list_feeds_data: Dict[str, str]) -> None:
  """Test case to check feed list details exported in JSON format.

  Args:
    mock_client (mock.MagicMock): Mock object
    get_feed_schema (Tuple): Test input data
    list_feeds_data (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema, list_feeds_data
  ]

  # Method Call
  result = runner.invoke(
      list_command,
      ["--export", TEMP_EXPORT_JSON_FILE[:-5], "--file-format", "json"])
  assert "Feed list details exported successfully" in result.output
