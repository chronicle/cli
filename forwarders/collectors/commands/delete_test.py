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

from forwarders.collectors.commands.delete import delete
from forwarders.collectors.tests.fixtures import *  # pylint: disable=wildcard-import
from mock_test_utility import MockResponse

runner = CliRunner()


def test_prompt_text() -> None:
  """Test case to check prompt text."""
  result = runner.invoke(delete)
  assert "Enter Forwarder ID:" in result.output


@mock.patch(
    "forwarders.collectors.commands.delete.click.prompt"
)
def test_delete_forwarder_not_provided(input_patch: mock.MagicMock) -> None:
  """Test case to check if Forwarder ID not provided.

  Args:
    input_patch (mock.MagicMock): Mock object
  """
  input_patch.return_value = ""

  # Method Call
  result = runner.invoke(delete)
  assert "Forwarder ID not provided. Please enter Forwarder ID." in result.output


@mock.patch(
    "forwarders.collectors.commands.delete.click.prompt"
)
def test_delete_collector_not_provided(input_patch: mock.MagicMock) -> None:
  """Test case to check if Collector ID not provided.

  Args:
    input_patch (mock.MagicMock): Mock object
  """

  input_patch.side_effect = ["123", ""]
  # Method Call
  result = runner.invoke(delete)
  assert "Collector ID not provided. Please enter Collector ID.\n" in result.output


@mock.patch(
    "forwarders.collectors.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.delete.click.prompt"
)
def test_delete_collector_200(input_patch: mock.MagicMock,
                              mock_client: mock.MagicMock) -> None:
  """Test case to successfully delete collector.

  Args:
   input_patch (mock.MagicMock): Mock object
   mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  input_patch.side_effect = ["123", "456"]
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=200, text="""{}""")
  ]

  # Method Call
  result = runner.invoke(delete)
  assert "\nCollector (ID: 456) deleted successfully." in result.output


@mock.patch(
    "forwarders.collectors.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.delete.click.prompt"
)
def test_delete_collector_404(input_patch: mock.MagicMock,
                              mock_client: mock.MagicMock) -> None:
  """Test case to check for invalid Collector ID.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  input_patch.side_effect = ["123", "456"]
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=404, text="""{}""")
  ]

  # Method Call
  result = runner.invoke(delete)
  assert "Collector does not exist." in result.output


@mock.patch(
    "forwarders.collectors.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.delete.click.prompt"
)
def test_delete_collector_400(input_patch: mock.MagicMock,
                              mock_client: mock.MagicMock) -> None:
  """Test case to check whether Collector ID does not exist.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  input_patch.side_effect = ["123", "456"]
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=400, text="""{}""")
  ]

  # Method Call
  result = runner.invoke(delete)
  assert "Invalid Collector ID. Please enter valid Collector ID." in result.output


@mock.patch(
    "forwarders.collectors.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.delete.click.prompt"
)
def test_delete_credential_file_missing(input_patch: mock.MagicMock,
                                        mock_client: mock.MagicMock) -> None:
  """Test case to check invalid credential path.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  input_patch.side_effect = ["123", "456"]
  mock_client.return_value.request.side_effect = OSError(
      "Credential Path not found.")
  expected_message = "Failed with exception: Credential Path not found."

  # Method Call
  result = runner.invoke(delete, ["--credential_file", "dummy.json"])
  assert expected_message in result.output


@mock.patch(
    "forwarders.collectors.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.delete.click.prompt"
)
def test_delete_collector_internal_server_error_code(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    collector_500_response: Dict[str, Any]) -> None:
  """Test case to check the server error code.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    collector_500_response (Dict[str, Any]): Test data to fetch collector with
      server error status code.
  """
  input_patch.side_effect = ["123", "123"]
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [collector_500_response]

  # Method call
  result = runner.invoke(delete)
  assert ("\nError while fetching collector.\nResponse Code: 500\nError: "
          "Internal Server Error") in result.output


@mock.patch(
    "forwarders.collectors.commands.delete.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.delete.click.prompt"
)
def test_delete_collector_verbose_option(input_patch: mock.MagicMock,
                                         mock_client: mock.MagicMock) -> None:
  """Test case to check response for 200 response code with verbose option.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  input_patch.side_effect = ["123", "456"]
  mock_client.return_value.request.return_value = MockResponse(
      status_code=200, text="""{}""")

  # Method Call
  result = runner.invoke(delete, ["--verbose"])
  assert """Collector (ID: 456) deleted successfully.
==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: https://backstory.googleapis.com/v2/forwarders/123/collectors/456
  Method: DELETE
  Body: None
Response:
  Body: {}
""" in result.output
