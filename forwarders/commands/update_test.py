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
"""Unit tests for update.py."""

import json
import os
from typing import Any, Dict
from unittest import mock

from click._compat import WIN
from click.testing import CliRunner

from forwarders.commands.get import GetForwarderResponse
from forwarders.commands.update import update
from forwarders.tests.fixtures import *  # pylint: disable=wildcard-import
from forwarders.tests.fixtures import create_backup_file
from forwarders.tests.fixtures import TEMP_UPDATE_BACKUP_FILE
from mock_test_utility import MockResponse

runner = CliRunner()


@mock.patch(
    "forwarders.commands.update.click.confirm"
)
@mock.patch(
    "forwarders.commands.update.forwarder_utility.preview_changes"
)
@mock.patch(
    "forwarders.commands.update.schema_utility.Schema.prepare_request_body"
)
@mock.patch(
    "forwarders.commands.update.forwarder_utility.read_backup"
)
@mock.patch(
    "forwarders.commands.update.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.update.click.prompt")
def test_update_credential_file_invalid(
    mock_input: mock.MagicMock, mock_client: mock.MagicMock,
    mock_backup_file: mock.MagicMock, mock_prepare_request_body: mock.MagicMock,
    mock_preview_changes: mock.MagicMock, mock_choice: mock.MagicMock) -> None:
  """Test case for checking invalid credential path.

  Args:
    mock_input: Mock object for click prompt.
    mock_client: Mock object for client.
    mock_backup_file: Mock object for backup file.
    mock_prepare_request_body: Mock object for prepare_request_body method.
    mock_preview_changes: Mock object for preview_changes method.
    mock_choice: Mock object for click confirm.
  """
  mock_input.return_value = "123"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = OSError(
      "Credential Path not found.")
  req_body = {
      "display_name": "sample",
      "config": {
          "metadata": {
              "asset_namespace": "sample_name"
          }
      }
  }
  mock_backup_file.return_value = req_body
  mock_prepare_request_body.return_value = {}
  mock_preview_changes.return_value = {}
  mock_choice.return_value = True
  expected_message = "Failed with exception: Credential Path not found."
  result = runner.invoke(update, ["--credential_file", "dummy.json"])
  assert expected_message in result.output


@mock.patch(
    "forwarders.commands.update.click.prompt")
def test_update_forwarder_id_not_provided(mock_input: mock.MagicMock) -> None:
  """Test case to check if Forwarder ID is not provided.

  Args:
    mock_input: Mock object for click prompt
  """
  mock_input.return_value = ""

  # Method Call
  result = runner.invoke(update)
  assert "Forwarder ID not provided. Please enter Forwarder ID." in result.output


@mock.patch(
    "forwarders.commands.update.forwarder_utility.read_backup"
)
@mock.patch(
    "forwarders.commands.update.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.update.click.prompt")
def test_get_forwarder_with_internal_server_error(
    mock_input: mock.MagicMock, mock_client: mock.MagicMock,
    mock_backup_file: mock.MagicMock, internal_server_error: Dict[str,
                                                                  Any]) -> None:
  """Test case for checking collector not exist.

  Args:
    mock_input: Mock object for click prompt.
    mock_client: Mock object for client.
    mock_backup_file: Mock object for backup file.
    internal_server_error: Response with internal server error.
  """
  mock_input.side_effect = ["123"]
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.return_value = internal_server_error
  mock_backup_file.return_value = {}

  # Method call
  result = runner.invoke(update, ["--verbose"])
  assert """Error while fetching forwarder details.
Response Code: 500""" in result.output
  assert """Internal Server Error
==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: https://backstory.googleapis.com/v2/forwarders/123
  Method: GET
  Body: None
Response:
  Body: {'error': {'message': 'Internal Server Error'}}""" in result.output


@mock.patch(
    "forwarders.commands.update.click.confirm"
)
@mock.patch(
    "forwarders.commands.update.schema_utility.Schema.prepare_request_body"
)
@mock.patch(
    "forwarders.commands.update.get_forwarder"
)
@mock.patch(
    "forwarders.commands.update.forwarder_utility.read_backup"
)
@mock.patch(
    "forwarders.commands.update.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.update.click.prompt")
def test_update_success(mock_input: mock.MagicMock, mock_client: mock.MagicMock,
                        mock_backup_file: mock.MagicMock,
                        mock_get_forwarder: mock.MagicMock,
                        mock_prepare_request_body: mock.MagicMock,
                        mock_choice: mock.MagicMock) -> None:
  """Test case to check successful updation of forwarder.

  Args:
    mock_input: Mock object for click prompt.
    mock_client: Mock object for client.
    mock_backup_file: Mock object for backup file.
    mock_get_forwarder: Mock object for preview_changes method.
    mock_prepare_request_body: Mock object for prepare_request_body method.
    mock_choice: Mock object for click confirm.
  """
  mock_input.return_value = "123"
  mock_backup_file.return_value = {}
  mock_get_forwarder.return_value = GetForwarderResponse(
      {}, {"display_name": "test"}, {}, {})
  mock_prepare_request_body.return_value = {"display_name": "test"}
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.return_value = MockResponse(
      status_code=200, text="""{"name": "forwarder/123"}""")
  mock_choice.return_value = True
  result = runner.invoke(update)
  if WIN:
    assert """================================================================================
Press Enter if you don't want to update.
================================================================================

Preview changes:

  - Press ENTER key (scrolls one line at a time) or SPACEBAR key (display next screen).
  - Press 'q' to quit and confirm preview changes.
=============================================================================""" in result.output
  else:
    assert """================================================================================
Press Enter if you don't want to update.
================================================================================

Preview changes:

  - Press Up/b or Down/z keys to paginate.
  - To switch case-sensitivity, press '-i' and press enter. By default, search
    is case-sensitive.
  - To search for specific field, press '/' key, enter text and press enter.
  - Press 'q' to quit and confirm preview changes.
  - Press `h` for all the available options to navigate the list.
=============================================================================""" in result.output
  assert """Display name: test


Updating forwarder...

Forwarder updated successfully with Forwarder ID: 123""" in result.output


@mock.patch(
    "forwarders.commands.update.click.confirm"
)
@mock.patch(
    "forwarders.commands.update.UPDATE_FORWARDER_BACKUP_FILE",
    TEMP_UPDATE_BACKUP_FILE)
@mock.patch(
    "forwarders.commands.update.schema_utility.Schema.prepare_request_body"
)
@mock.patch(
    "forwarders.commands.update.forwarder_utility.read_backup"
)
@mock.patch(
    "forwarders.commands.update.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.update.click.prompt")
def test_update_backup_file_present_success(
    mock_input: mock.MagicMock, mock_client: mock.MagicMock,
    mock_backup_file: mock.MagicMock, mock_prepare_request_body: mock.MagicMock,
    mock_choice: mock.MagicMock) -> None:
  """Test case to check backup file is removed after successful updation of forwarder.

  Args:
    mock_input: Mock object for click prompt
    mock_client: Mock object for client
    mock_backup_file: Mock object for backup file
    mock_prepare_request_body: Mock object for prepare_request_body method
    mock_choice: Mock object for click confirm.
  """
  mock_input.return_value = "123"
  content = {
      "name": "forwarder/123",
      "display_name": "sample",
      "config.upload_compression": True,
      "config.metadata.asset_namespace": "sample_name",
      "config.metadata.labels": [{
          "key": "k",
          "value": "v"
      }]
  }
  req_body = {
      "display_name": "sample",
      "config": {
          "upload_compression": True,
          "metadata": {
              "asset_namespace": "sample_name",
              "labels": [{
                  "key": "k",
                  "value": "v"
              }]
          }
      }
  }
  req_body = {
      "config": {
          "metadata": {
              "asset_namespace": "sample_name",
              "labels": [{
                  "key": "k",
                  "value": "v"
              }]
          },
          "upload_compression": True,
      },
      "display_name": "sample"
  }
  create_backup_file(TEMP_UPDATE_BACKUP_FILE, content)
  mock_backup_file.return_value = req_body
  mock_prepare_request_body.return_value = req_body
  mock_client.return_value = mock.Mock()
  mock_choice.return_value = True
  mock_client.return_value.request.return_value = MockResponse(
      status_code=200, text="""{"name": "forwarder/123"}""")
  result = runner.invoke(update)

  assert "Forwarder updated successfully with Forwarder ID: 123" in result.output
  assert not os.path.exists(TEMP_UPDATE_BACKUP_FILE)


@mock.patch(
    "forwarders.commands.update.click.confirm"
)
@mock.patch(
    "forwarders.commands.update.schema_utility.Schema.prepare_request_body"
)
@mock.patch(
    "forwarders.commands.update.get_forwarder"
)
@mock.patch(
    "forwarders.commands.update.forwarder_utility.read_backup"
)
@mock.patch(
    "forwarders.commands.update.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.update.click.prompt")
def test_update_verbose(mock_input: mock.MagicMock, mock_client: mock.MagicMock,
                        mock_backup_file: mock.MagicMock,
                        mock_get_forwarder: mock.MagicMock,
                        mock_prepare_request_body: mock.MagicMock,
                        mock_choice: mock.MagicMock) -> None:
  """Test case to check updation of forwarder with verbose.

  Args:
    mock_input: Mock object for click prompt
    mock_client: Mock object for client
    mock_backup_file: Mock object for backup file
    mock_get_forwarder: Mock object for preview_changes method
    mock_prepare_request_body: Mock object for prepare_request_body method
    mock_choice: Mock object for click confirm.
  """
  mock_input.return_value = "123"
  mock_backup_file.return_value = {}
  mock_get_forwarder.return_value = GetForwarderResponse(
      {}, {"display_name": "test"}, {}, {})
  mock_prepare_request_body.return_value = {"display_name": "test"}
  mock_client.return_value = mock.Mock()
  mock_choice.return_value = True
  mock_client.return_value.request.return_value = MockResponse(
      status_code=200, text="""{"name": "forwarder/123"}""")
  result = runner.invoke(update, ["--verbose"])
  if WIN:
    assert """================================================================================
Press Enter if you don't want to update.
================================================================================

Preview changes:

  - Press ENTER key (scrolls one line at a time) or SPACEBAR key (display next screen).
  - Press 'q' to quit and confirm preview changes.
=============================================================================""" in result.output
  else:
    assert """================================================================================
Press Enter if you don't want to update.
================================================================================

Preview changes:

  - Press Up/b or Down/z keys to paginate.
  - To switch case-sensitivity, press '-i' and press enter. By default, search
    is case-sensitive.
  - To search for specific field, press '/' key, enter text and press enter.
  - Press 'q' to quit and confirm preview changes.
  - Press `h` for all the available options to navigate the list.
=============================================================================""" in result.output
  assert """
Display name: test


Updating forwarder...

Forwarder updated successfully with Forwarder ID: 123
==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: https://backstory.googleapis.com/v2/forwarders/123
  Method: PATCH
  Body: None
Response:
  Body: {'display_name': 'test'}

==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: https://backstory.googleapis.com/v2/forwarders/123
  Method: PATCH
  Body: {'display_name': 'test'}
Response:
  Body: {'name': 'forwarder/123'}""" in result.output


@mock.patch(
    "forwarders.commands.update.click.confirm"
)
@mock.patch(
    "forwarders.commands.update.schema_utility.Schema.prepare_request_body"
)
@mock.patch(
    "forwarders.commands.update.get_forwarder"
)
@mock.patch(
    "forwarders.commands.update.forwarder_utility.read_backup"
)
@mock.patch(
    "forwarders.commands.update.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.update.click.prompt")
def test_update_error_code(mock_input: mock.MagicMock,
                           mock_client: mock.MagicMock,
                           mock_backup_file: mock.MagicMock,
                           mock_get_forwarder: mock.MagicMock,
                           mock_prepare_request_body: mock.MagicMock,
                           mock_choice: mock.MagicMock) -> None:
  """Test case to check failure of updation of forwarder.

  Args:
    mock_input: Mock object for click prompt
    mock_client: Mock object for client
    mock_backup_file: Mock object for backup file
    mock_get_forwarder: Mock object for preview_changes method
    mock_prepare_request_body: Mock object for prepare_request_body method
    mock_choice: Mock object for click confirm
  """
  mock_input.return_value = "123"
  mock_backup_file.return_value = {}
  mock_get_forwarder.return_value = GetForwarderResponse(
      {}, {"display_name": "test"}, {}, {})
  mock_prepare_request_body.return_value = {}
  mock_client.return_value = mock.Mock()
  mock_choice.return_value = True
  mock_client.return_value.request.return_value = MockResponse(
      status_code=400, text="""{"error": {"message": "sample"}}""")
  result = runner.invoke(update)

  expected_output = ("Error occurred while updating forwarder.\nResponse Code: "
                     "400.\nError: sample")
  assert expected_output in result.output


@mock.patch(
    "forwarders.commands.update.click.confirm"
)
@mock.patch(
    "forwarders.commands.update.UPDATE_FORWARDER_BACKUP_FILE",
    TEMP_UPDATE_BACKUP_FILE)
@mock.patch(
    "forwarders.commands.update.schema_utility.Schema.prepare_request_body"
)
@mock.patch(
    "forwarders.commands.update.forwarder_utility.read_backup"
)
@mock.patch(
    "forwarders.commands.update.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.update.click.prompt")
def test_update_backup_file_present_error_code(
    mock_input: mock.MagicMock, mock_client: mock.MagicMock,
    mock_backup_file: mock.MagicMock, mock_prepare_request_body: mock.MagicMock,
    mock_choice: mock.MagicMock) -> None:
  """Test case to check backup file is created if forwarder updation fails.

  Args:
    mock_input: Mock object for click prompt
    mock_client: Mock object for client
    mock_backup_file: Mock object for backup file
    mock_prepare_request_body: Mock object for prepare_request_body method
    mock_choice: Mock object for click confirm.
  """
  content = {
      "name": "forwarder/123",
      "display_name": "sample",
      "config": {
          "upload_compression": True,
          "metadata": {
              "asset_namespace": "sample_name",
              "labels": [{
                  "key": "k",
                  "value": "v"
              }]
          }
      },
  }
  create_backup_file(TEMP_UPDATE_BACKUP_FILE, content)
  req_body = {
      "config": {
          "metadata": {
              "asset_namespace": "sample_name",
              "labels": [{
                  "key": "k",
                  "value": "v"
              }]
          },
          "upload_compression": True,
      },
      "display_name": "sample"
  }
  mock_input.return_value = "123"
  mock_backup_file.return_value = req_body
  mock_prepare_request_body.return_value = req_body
  mock_client.return_value = mock.Mock()
  mock_choice.return_value = True
  mock_client.return_value.request.return_value = MockResponse(
      status_code=400, text="""{"error": {"message": "sample"}}""")
  result = runner.invoke(update)

  expected_output = ("Error occurred while updating forwarder.\nResponse Code: "
                     "400.\nError: sample")
  assert expected_output in result.output
  assert os.path.exists(TEMP_UPDATE_BACKUP_FILE)

  with open(TEMP_UPDATE_BACKUP_FILE) as file:
    data = json.load(file)
  assert data == req_body


def test_prompt_text() -> None:
  """Test case to check prompt text."""

  # Method call
  result = runner.invoke(update)
  assert "Enter Forwarder ID:" in result.output
