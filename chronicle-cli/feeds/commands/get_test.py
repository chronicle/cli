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
"""Unit tests for get.py."""

from typing import Dict, Tuple
from unittest import mock

from click.testing import CliRunner

from feeds.commands.get import get
from feeds.tests.fixtures import *  # pylint: disable=wildcard-import
from feeds.tests.fixtures import MockResponse

runner = CliRunner()


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch("feeds.commands.get.click.prompt")
def test_feed_not_exist(
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
  result = runner.invoke(get)
  assert result.output == "Feed does not exist.\n"


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch("feeds.commands.get.click.prompt")
def test_feed_id_invalid(
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
  result = runner.invoke(get)
  assert result.output == ("Invalid Feed ID. Please enter valid Feed ID.\n")


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch("feeds.commands.get.click.prompt")
def test_get_200(input_patch: mock.MagicMock, mock_client: mock.MagicMock,
                 get_feed_data: Tuple[Dict[str, str], str],
                 get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check response for 200 response code.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_feed_data (Tuple): Test input data
    get_feed_schema (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_feed_data
  ]

  # Method Call
  result = runner.invoke(get)
  expected_output = ("\nFeed Details:\n  ID: 123\n  Source type: Dummy Source"
                     " Type\n  Log type: Dummy LogType\n  "
                     "State: INACTIVE\n  Feed Settings:\n    "
                     "Field 1: abc.dummy.com\n    Field 2: ID")
  assert expected_output in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch("feeds.commands.get.click.prompt")
def test_schema_not_found(input_patch: mock.MagicMock,
                          mock_client: mock.MagicMock,
                          get_fail_feed_data: Tuple[Dict[str, str], str],
                          get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check response for 200 response code.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_fail_feed_data (Tuple): Test input data
    get_feed_schema (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_fail_feed_data
  ]

  # Method Call
  result = runner.invoke(get)
  assert "Schema Not Found." in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch("feeds.commands.get.click.prompt")
def test_feed_id_absent(input_patch: mock.MagicMock,
                        mock_client: mock.MagicMock,
                        get_feed_data: Tuple[Dict[str, str], str],
                        get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check for input absent.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_feed_data (Tuple): Test input data
    get_feed_schema (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = ""
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_feed_data
  ]

  # Method Call
  result = runner.invoke(get)
  assert "Feed ID not provided. Please enter Feed ID." in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_get_credential_file_invalid(mock_client: mock.MagicMock) -> None:
  """Test case for checking invalid credential path.

  Args:
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = OSError(
      "Credential Path not found.")
  expected_message = "Failed with exception: Credential Path not found."

  result = runner.invoke(get, ["--credential_file", "dummy.json"])

  assert expected_message in result.output


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch("feeds.commands.get.click.prompt")
def test_get_verbose_option(input_patch: mock.MagicMock,
                            mock_client: mock.MagicMock,
                            get_feed_data: Tuple[Dict[str, str], str],
                            get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check response for 200 response code with verbose option.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_feed_data (Tuple): Test input data
    get_feed_schema (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_feed_data
  ]

  # Method Call
  result = runner.invoke(get, ["--verbose"])
  expected_output = ("\nFeed Details:\n  ID: 123\n  Source type: Dummy Source"
                     " Type\n  Log type: Dummy LogType\n  "
                     "State: INACTIVE\n  Feed Settings:\n    "
                     "Field 1: abc.dummy.com\n    Field 2: ID")
  assert expected_output in result.output
  assert "HTTP Request Details" in result.output
