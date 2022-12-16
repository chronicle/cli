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
"""Unit tests for generate_file.py."""

import os
from typing import Dict, Tuple, Any
from unittest import mock

from click.testing import CliRunner

from forwarders.commands.generate_file import generate_file
from forwarders.tests.fixtures import *  # pylint: disable=wildcard-import
from forwarders.tests.fixtures import TEMP_GENERATE_FILE

runner = CliRunner()


@mock.patch(
    "forwarders.commands.generate_file.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.generate_file.click.prompt"
)
def test_forwarder_id_absent(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    get_forwarder_data: Tuple[Dict[str, str], str]) -> None:
  """Test case to check for input absent.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    get_forwarder_data (Tuple): Test data to fetch forwarder.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = ""
  mock_client.return_value.request.side_effect = [get_forwarder_data]

  # Method call.
  result = runner.invoke(generate_file)
  assert "Forwarder ID not provided. Please enter Forwarder ID." in result.output


@mock.patch(
    "forwarders.commands.generate_file.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.generate_file.click.prompt"
)
def test_generate_file_500(input_patch: mock.MagicMock,
                           mock_client: mock.MagicMock,
                           internal_server_error: Dict[str, Any]) -> None:
  """Test case to check the server error code.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    internal_server_error: Test data to fetch forwarder with error code.
  """
  input_patch.return_value = "123"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [internal_server_error]

  # Method call.
  result = runner.invoke(generate_file, ["--verbose"])
  assert """Generating forwarder file ...

Error while generating forwarder file.
Response Code: 500""" in result.output
  assert """==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: https://backstory.googleapis.com/v2/forwarders/123:generateForwarderFiles
  Method: GET
  Body: None
Response:
  Body: {'error': {'message': 'Internal Server Error'}}""" in result.output


@mock.patch(
    "forwarders.commands.generate_file.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.generate_file.click.prompt"
)
def test_file_generated(input_patch: mock.MagicMock,
                        mock_client: mock.MagicMock,
                        generate_forwarder_file: str) -> None:
  """Test case to check config file generated.


  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    generate_forwarder_file (str): Test data to fetch forwarder file.
  """
  input_patch.return_value = "123"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [generate_forwarder_file]
  result = runner.invoke(generate_file,
                         ["--file-path", TEMP_GENERATE_FILE[:-5]])
  assert os.path.exists(TEMP_GENERATE_FILE)
  assert f"""Generating forwarder file ...
Forwarder configuration generated successfully at the following path: {TEMP_GENERATE_FILE}""" in result.output


@mock.patch(
    "forwarders.commands.generate_file.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.generate_file.click.prompt"
)
def test_get_credential_file_invalid(input_patch: mock.MagicMock,
                                     mock_client: mock.MagicMock) -> None:
  """Test case for checking invalid credential path.

  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.side_effect = OSError("Credential Path not found.")
  expected_message = "Failed with exception: Credential Path not found."

  result = runner.invoke(generate_file, ["--credential_file", "my_dummy.json"])
  assert expected_message in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""

  # Method call.
  result = runner.invoke(generate_file)
  assert "Enter Forwarder ID:" in result.output


@mock.patch(
    "forwarders.commands.generate_file.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.generate_file.click.prompt"
)
def test_verbose_output(input_patch: mock.MagicMock,
                        mock_client: mock.MagicMock,
                        generate_forwarder_file: str) -> None:
  """Test case to check the verbose text displayed on the output console.


  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    generate_forwarder_file (str): Test data to fetch forwarder file.
  """
  input_patch.return_value = "123"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [generate_forwarder_file]
  result = runner.invoke(generate_file,
                         ["--file-path", TEMP_GENERATE_FILE[:-5], "--verbose"])
  assert """==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: https://backstory.googleapis.com/v2/forwarders/123:generateForwarderFiles
  Method: GET
  Body: None
Response:
  Body: {'config': 'output'}""" in result.output
