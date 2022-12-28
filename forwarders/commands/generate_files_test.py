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
"""Unit tests for generate_files.py."""

import os
from typing import Dict, Tuple, Any
from unittest import mock

from click.testing import CliRunner

from forwarders.commands.generate_files import generate_files
from forwarders.tests.fixtures import *  # pylint: disable=wildcard-import
from forwarders.tests.fixtures import TEMP_GENERATE_FILES

runner = CliRunner()


@mock.patch(
    "forwarders.commands.generate_files.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.generate_files.click.prompt"
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
  result = runner.invoke(generate_files)
  assert "Forwarder ID not provided. Please enter Forwarder ID." in result.output


@mock.patch(
    "forwarders.commands.generate_files.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.generate_files.click.prompt"
)
def test_generate_files_500(input_patch: mock.MagicMock,
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
  result = runner.invoke(generate_files, ["--verbose"])
  assert """Generating forwarder files ...

Error while generating forwarder files.
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
    "forwarders.commands.generate_files.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.generate_files.click.prompt"
)
def test_files_generated(input_patch: mock.MagicMock,
                         mock_client: mock.MagicMock,
                         generate_forwarder_file: str) -> None:
  """Test case to check config files generated.


  Args:
    input_patch (mock.MagicMock): Mock object.
    mock_client (mock.MagicMock): Mock object.
    generate_forwarder_file (str): Test data to fetch forwarder file.
  """
  input_patch.return_value = "123"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [generate_forwarder_file]
  result = runner.invoke(generate_files, ["--file-path", TEMP_GENERATE_FILES])
  file_path = f"{TEMP_GENERATE_FILES}_forwarder.conf"
  auth_file_path = f"{TEMP_GENERATE_FILES}_forwarder_auth.conf"
  assert os.path.exists(file_path)
  assert os.path.exists(auth_file_path)
  assert f"""Generating forwarder files ...
Forwarder files generated successfully.
Configuration file: {file_path}
Auth file: {auth_file_path}""" in result.output


@mock.patch(
    "forwarders.commands.generate_files.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.generate_files.click.prompt"
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

  result = runner.invoke(generate_files, ["--credential_file", "my_dummy.json"])
  assert expected_message in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""

  # Method call.
  result = runner.invoke(generate_files)
  assert "Enter Forwarder ID:" in result.output


@mock.patch(
    "forwarders.commands.generate_files.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.generate_files.click.prompt"
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
  result = runner.invoke(generate_files,
                         ["--file-path", TEMP_GENERATE_FILES, "--verbose"])
  assert """==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: https://backstory.googleapis.com/v2/forwarders/123:generateForwarderFiles
  Method: GET
  Body: None
Response:
  Body: {'config': 'output', 'auth': 'authoutput'}""" in result.output
