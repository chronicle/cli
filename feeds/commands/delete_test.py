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
"""Unit tests for delete.py ."""

from unittest import mock
from click.testing import CliRunner
from feeds.commands.delete import delete
from mock_test_utility import MockResponse

runner = CliRunner()


@mock.patch(
    "feeds.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.delete.click.prompt")
def test_delete_200(input_patch: mock.MagicMock,
                    mock_client: mock.MagicMock) -> None:
  """Test case to successfully delete feed.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=200, text="""{}""")
  ]

  # Method Call
  result = runner.invoke(delete)
  assert "\nFeed (ID: 123) deleted successfully." in result.output


@mock.patch(
    "feeds.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.delete.click.prompt")
def test_delete_400(input_patch: mock.MagicMock,
                    mock_client: mock.MagicMock) -> None:
  """Test case to check whether Feed ID does not exist.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=400, text="""{}""")
  ]

  # Method Call
  result = runner.invoke(delete)
  assert "Feed does not exist." in result.output


@mock.patch(
    "feeds.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.delete.click.prompt")
def test_delete_404(input_patch: mock.MagicMock,
                    mock_client: mock.MagicMock) -> None:
  """Test case to check for invalid feed ID.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=404, text="""{}""")
  ]

  # Method Call
  result = runner.invoke(delete)
  assert "Invalid Feed ID. Please enter valid Feed ID." in result.output


@mock.patch(
    "feeds.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.delete.click.prompt")
def test_delete_credential_file(input_patch: mock.MagicMock,
                                mock_client: mock.MagicMock) -> None:
  """Test case to check invalid credential path.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = OSError(
      "Credential Path not found.")
  expected_message = "Failed with exception: Credential Path not found."

  # Method Call
  result = runner.invoke(delete, ["--credential_file", "dummy.json"])
  assert expected_message in result.output


@mock.patch(
    "feeds.commands.delete.click.prompt")
def test_delete_feed_not_provided(input_patch: mock.MagicMock) -> None:
  """Test case to check if Feed ID not provided.

  Args:
    input_patch (mock.MagicMock): Mock object
  """
  input_patch.return_value = ""

  # Method Call
  result = runner.invoke(delete)
  assert "Feed ID not provided. Please enter Feed ID." in result.output
