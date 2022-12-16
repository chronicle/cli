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
"""Tests for generate."""

import shutil
from typing import Dict
from unittest import mock

from click.testing import CliRunner

from parsers.commands.generate import generate
from parsers.tests.fixtures import *  # pylint: disable=wildcard-import
from parsers.tests.fixtures import MockResponse
from parsers.tests.fixtures import TEST_DATA_DIR


runner = CliRunner()


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "parsers.commands.generate.click.prompt")
@mock.patch(
    "parsers.constants.path_constants.PARSER_DATA_DIR",
    TEST_DATA_DIR)
def test_generate_logs(mock_input: mock.MagicMock, mock_client: mock.MagicMock,
                       generate_logs: Dict[str, str]) -> None:
  """Test case to check response for generate logs.

  Args:
    mock_input (mock.MagicMock): Mock prompt object.
    mock_client (mock.MagicMock): Mock object.
    generate_logs (Tuple): Test input data.
  """
  result = runner.invoke(generate)
  mock_input.side_effect = [
      "2020-08-17T10:00:00Z", "2022-08-23T10:00:00Z", "WINDOWS_DHCP"
  ]

  # Check for non-empty response.
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      generate_logs, generate_logs, generate_logs
  ]
  result = runner.invoke(generate)
  assert "Generating sample size: 1" in result.output
  assert "Generating sample size: 10" in result.output
  assert "Generating sample size: 1k" in result.output

  try:
    shutil.rmtree(TEST_DATA_DIR + "/chronicle_cli/parsers/windows_dhcp")
  except FileNotFoundError:
    pass


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "parsers.commands.generate.click.prompt")
@mock.patch(
    "parsers.constants.path_constants.PARSER_DATA_DIR",
    TEST_DATA_DIR)
def test_empty_generate_logs(mock_input: mock.MagicMock,
                             mock_client: mock.MagicMock) -> None:
  """Test case to check empty response for generate logs.

  Args:
    mock_input (mock.MagicMock): Mock prompt object.
    mock_client (mock.MagicMock): Mock object.
  """
  result = runner.invoke(generate)
  mock_input.side_effect = [
      "2020-08-17T10:00:00Z", "2022-08-23T10:00:00Z", "WINDOWS_DHCP"
  ]
  mock_input.side_effect = [
      "2020-08-17T10:00:00Z", "2022-08-23T10:00:00Z", "WINDOWS_DHCP"
  ]
  # Check for empty response.
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=200, text="""{}"""),
      MockResponse(status_code=200, text="""{}"""),
      MockResponse(status_code=200, text="""{}""")
  ]
  result = runner.invoke(generate)
  assert "Generating sample size: 1" in result.output
  assert "Generating sample size: 10" in result.output
  assert "Generating sample size: 1k" in result.output
  assert "Generated sample data (WINDOWS_DHCP); run this to go there:" in result.output
  assert "cd" in result.output

  try:
    shutil.rmtree(TEST_DATA_DIR + "/chronicle_cli/parsers/windows_dhcp")
  except FileNotFoundError:
    pass


def test_prompt_text() -> None:
  """Test case to check prompt text."""
  result = runner.invoke(generate)
  assert "Enter Start Date (Format: yyyy-mm-ddThh:mm:ssZ):" in result.output
  assert "Enter End Date (Format: yyyy-mm-ddThh:mm:ssZ):" in result.output
  assert "Enter Log Type:" in result.output
