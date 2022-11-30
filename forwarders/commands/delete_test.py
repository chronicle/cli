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

from typing import Any, Dict
from unittest import mock

from click.testing import CliRunner

from forwarders.commands.delete import delete
from forwarders.tests.fixtures import *  # pylint: disable=wildcard-import
from mock_test_utility import MockResponse

runner = CliRunner()


@mock.patch(
    "forwarders.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.delete.click.prompt")
def test_delete_200(input_patch: mock.MagicMock,
                    mock_client: mock.MagicMock) -> None:
  """Test case to successfully delete forwarder.

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
  assert (
      "Deleting forwarder and all its associated collectors...\n\nForwarder "
      "(ID: 123) deleted successfully with all its associated collectors."
  ) in result.output


@mock.patch(
    "forwarders.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.delete.click.prompt")
def test_delete_400(input_patch: mock.MagicMock,
                    mock_client: mock.MagicMock) -> None:
  """Test case to check whether Forwarder ID does not exist.

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
  assert "Invalid Forwarder ID. Please enter valid Forwarder ID." in result.output


@mock.patch(
    "forwarders.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.delete.click.prompt")
def test_delete_404(input_patch: mock.MagicMock,
                    mock_client: mock.MagicMock) -> None:
  """Test case to check for invalid Forwarder ID.

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
  assert "Forwarder does not exist." in result.output


@mock.patch(
    "forwarders.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.get.click.prompt")
def test_delete_server_error_code(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    get_forwarder_server_error_code: Dict[str, Any]) -> None:
  input_patch.return_value = "123"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_forwarder_server_error_code
  ]

  # Method call
  result = runner.invoke(delete)
  assert ("\nError while fetching forwarder.\nResponse Code: 500\nError: "
          "Internal Server Error") in result.output


@mock.patch(
    "forwarders.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.delete.click.prompt")
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
    "forwarders.commands.delete.click.prompt")
def test_delete_forwarder_not_provided(input_patch: mock.MagicMock) -> None:
  """Test case to check if Forwarder ID not provided.

  Args:
    input_patch (mock.MagicMock): Mock object
  """
  input_patch.return_value = ""

  # Method Call
  result = runner.invoke(delete)
  assert "Forwarder ID not provided. Please enter Forwarder ID." in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""

  # Method call
  result = runner.invoke(delete)
  assert "Enter Forwarder ID:" in result.output
