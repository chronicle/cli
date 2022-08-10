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
"""Unit tests for disable.py."""

from typing import Dict, Tuple
from unittest import mock

from click.testing import CliRunner

from feeds.commands.disable import disable
from feeds.tests.fixtures import *  # pylint: disable=wildcard-import
from feeds.tests.fixtures import MockResponse

runner = CliRunner()


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.disable.click.prompt")
def test_disable_feed_not_exist(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    get_feed_not_exist_data: Tuple[Dict[str, str], str]) -> None:
  """Test case to check if feed does not exist.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_feed_not_exist_data (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=200, text="""{"feedSourceTypeSchemas": []}"""),
      get_feed_not_exist_data
  ]

  # Method Call
  result = runner.invoke(disable)
  assert result.output == "Feed does not exist.\n"


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.disable.click.prompt")
def test_disable_feed_id_invalid(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    get_feed_id_invalid_data: Tuple[Dict[str, str], str]) -> None:
  """Test case for handling invalid feed ID.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_feed_id_invalid_data (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=200, text="""{"feedSourceTypeSchemas": []}"""),
      get_feed_id_invalid_data
  ]

  # Method Call
  result = runner.invoke(disable)
  assert result.output == ("Invalid Feed ID. Please enter valid Feed ID.\n")


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.disable.click.prompt")
def test_disable_feed_200(input_patch: mock.MagicMock,
                          mock_client: mock.MagicMock,
                          get_active_feed_data: Tuple[Dict[str, str], str],
                          get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check response for 200 response code.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_active_feed_data (Tuple): Test input data
    get_feed_schema (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_active_feed_data
  ]

  # Method Call
  result = runner.invoke(disable)
  expected_output = ("Feed with ID: 123 disabled successfully.")
  assert expected_output in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.disable.click.prompt")
def test_disable_feed_id_absent(input_patch: mock.MagicMock,
                                mock_client: mock.MagicMock,
                                get_active_feed_data: Tuple[Dict[str, str],
                                                            str],
                                get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check for input absent.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_active_feed_data (Tuple): Test input data
    get_feed_schema (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = ""
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_active_feed_data
  ]

  # Method Call
  result = runner.invoke(disable)
  assert "Feed ID not provided. Please enter Feed ID." in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_disable_feed_credential_file_invalid(
    mock_client: mock.MagicMock) -> None:
  """Test case for checking invalid credential path.

  Args:
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = OSError(
      "Credential Path not found.")
  expected_message = "Failed with exception: Credential Path not found."

  result = runner.invoke(disable, ["--credential_file", "dummy.json"])

  assert expected_message in result.output
