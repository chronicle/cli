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

import os
from typing import Dict, Tuple
from unittest import mock

from click.testing import CliRunner

from feeds.commands.update import update
from feeds.tests.fixtures import *  # pylint: disable=wildcard-import
from feeds.tests.fixtures import create_backup_file
from feeds.tests.fixtures import TEMP_UPDATE_BACKUP_FILE
from mock_test_utility import MockResponse


runner = CliRunner()


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_update_credential_file_invalid(mock_client: mock.MagicMock) -> None:
  """Test case for checking invalid credential path.

  Args:
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = OSError(
      "Credential Path not found.")
  expected_message = "Failed with exception: Credential Path not found."
  result = runner.invoke(update, ["--credential_file", "dummy.json"])
  assert expected_message in result.output


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.update.UPDATE_BACKUP_FILE",
    TEMP_UPDATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.update.click.prompt")
def test_update_success(mock_input: mock.MagicMock, mock_client: mock.MagicMock,
                        mock_request_body: mock.MagicMock,
                        get_feed_data: Tuple[Dict[str, str], str],
                        get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check successful updation of feed.

  Args:
    mock_input: Mock object for click prompt
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_data: Test data
    get_feed_schema: Test data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_feed_data,
      MockResponse(status_code=200, text="""{"name": "feeds/123"}""")
  ]
  mock_input.side_effect = [1, 1]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = "Feed updated successfully with Feed ID: 123"
  result = runner.invoke(update, ["--credential_file", ""])
  assert "Press Enter if you don't want to update." in result.output
  assert expected_output in result.output


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.update.UPDATE_BACKUP_FILE",
    TEMP_UPDATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.update.click.prompt")
def test_update_error_code(mock_input: mock.MagicMock,
                           mock_client: mock.MagicMock,
                           mock_request_body: mock.MagicMock,
                           get_feed_data: Tuple[Dict[str, str], str],
                           get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check failure of updation of feed.

  Args:
    mock_input: Mock object for click prompt
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_data: Test data
    get_feed_schema: Test data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_feed_data,
      MockResponse(status_code=400, text="""{"error": {"message": "test"}}""")
  ]
  mock_input.side_effect = [1, 1]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = ("Error occurred while updating feed. Response code: "
                     "400.\nError: test")
  result = runner.invoke(update, ["--credential_file", ""])
  assert expected_output in result.output
  assert os.path.exists(TEMP_UPDATE_BACKUP_FILE)


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.update.UPDATE_BACKUP_FILE",
    TEMP_UPDATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.update.click.prompt")
def test_feed_id_absent(mock_input: mock.MagicMock, mock_client: mock.MagicMock,
                        mock_request_body: mock.MagicMock,
                        get_feed_data: Tuple[Dict[str, str], str],
                        get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check feed id not exist.

  Args:
    mock_input (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    mock_request_body: Mock object
    get_feed_data (Tuple): Test input data
    get_feed_schema (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_feed_data,
      MockResponse(status_code=400, text="""{"error": {"message": "test"}}""")
  ]

  mock_input.return_value = ""
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})

  expected_output = "Feed ID not provided. Please enter Feed ID."
  result = runner.invoke(update, ["--credential_file", ""])
  assert expected_output in result.output


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.update.UPDATE_BACKUP_FILE",
    TEMP_UPDATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.update.click.prompt")
def test_schema_not_found(mock_input: mock.MagicMock,
                          mock_client: mock.MagicMock,
                          mock_request_body: mock.MagicMock,
                          get_fail_feed_data: Tuple[Dict[str, str], str],
                          get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check schema not found.

  Args:
    mock_input (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    mock_request_body: Mock object
    get_fail_feed_data (Tuple): Test input data
    get_feed_schema (Tuple): Test input data
  """
  mock_client.return_value = mock.Mock()
  mock_input.return_value = "123"
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_fail_feed_data
  ]

  # Method Call
  result = runner.invoke(update)
  assert "Schema Not Found." in result.output


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.update.UPDATE_BACKUP_FILE",
    TEMP_UPDATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.update.click.prompt")
@mock.patch(
    "feeds.commands.update.click.confirm")
def test_update_retry_true(mock_confirm: mock.MagicMock,
                           mock_input: mock.MagicMock,
                           mock_client: mock.MagicMock,
                           mock_request_body: mock.MagicMock,
                           get_feed_data: Tuple[Dict[str, str], str],
                           get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check retry of updation of feed.

  Args:
    mock_confirm: Mock object for click confirm
    mock_input: Mock object for click prompt
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_data: Test data
    get_feed_schema: Test data
  """
  content = {
      "name": "feeds/123",
      "details.log_type": "DUMMY_LOGTYPE",
      "details.feed_source_type": "DUMMY",
      "details.key": "value",
      "feed_state": "INACTIVE",
      "feedSourceType": "DUMMY",
      "display_source_type": "Dummy Source Type",
      "logType": "DUMMY_LOGTYPE",
      "display_log_type": "Dummy LogType"
  }
  create_backup_file(TEMP_UPDATE_BACKUP_FILE, content)
  mock_client.return_value = mock.Mock()
  mock_confirm.side_effect = [True]
  mock_input.side_effect = ["123"]
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_feed_data,
      MockResponse(status_code=200, text="""{"name": "feeds/123"}""")
  ]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = "Feed updated successfully with Feed ID: 123"
  result = runner.invoke(update, ["--credential_file", ""])
  assert expected_output in result.output
  assert not os.path.exists(TEMP_UPDATE_BACKUP_FILE)


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.update.UPDATE_BACKUP_FILE",
    TEMP_UPDATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.update.click.prompt")
@mock.patch(
    "feeds.commands.update.click.confirm")
def test_update_retry_true_400(mock_confirm: mock.MagicMock,
                               mock_input: mock.MagicMock,
                               mock_client: mock.MagicMock,
                               mock_request_body: mock.MagicMock,
                               get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check retry of updation of feed.

  Args:
    mock_confirm: Mock object for click confirm
    mock_input: Mock object for click prompt
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_schema: Test data
  """
  content = {
      "name": "feeds/123",
      "details.log_type": "DUMMY_LOGTYPE",
      "details.feed_source_type": "TEST",
      "details.key": "value",
      "feed_state": "INACTIVE",
      "feedSourceType": "TEST",
      "display_source_type": "Dummy Source Type",
      "logType": "DUMMY_LOGTYPE",
      "display_log_type": "Dummy LogType"
  }
  create_backup_file(TEMP_UPDATE_BACKUP_FILE, content)
  mock_client.return_value = mock.Mock()
  mock_confirm.side_effect = [True]
  mock_input.side_effect = ["123"]
  mock_client.return_value.request.side_effect = [
      get_feed_schema,
      MockResponse(
          status_code=400,
          text="""{"error": {"message": "Feed does not exist."}}""")
  ]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = "Schema Not Found."
  result = runner.invoke(update, ["--credential_file", ""])
  assert expected_output in result.output
  assert os.path.exists(TEMP_UPDATE_BACKUP_FILE)


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.update.UPDATE_BACKUP_FILE",
    TEMP_UPDATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.update.click.prompt")
def test_update_retry_id_unmatched(mock_input: mock.MagicMock,
                                   mock_client: mock.MagicMock,
                                   mock_request_body: mock.MagicMock,
                                   get_feed_data: Tuple[Dict[str, str], str],
                                   get_feed_schema: Tuple[str, str]) -> None:
  """Test case to skip retry of updation feed when ID not matched.

  Args:
    mock_input: Mock object for click prompt
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_data: Test data
    get_feed_schema: Test data
  """
  content = {
      "name": "feeds/123",
      "details.log_type": "DUMMY_LOGTYPE",
      "details.feed_source_type": "DUMMY",
      "details.key": "value",
      "feed_state": "INACTIVE",
      "feedSourceType": "DUMMY",
      "display_source_type": "Dummy Source Type",
      "logType": "DUMMY_LOGTYPE",
      "display_log_type": "Dummy LogType"
  }
  create_backup_file(TEMP_UPDATE_BACKUP_FILE, content)
  mock_client.return_value = mock.Mock()
  mock_input.side_effect = ["321"]
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_feed_data,
      MockResponse(status_code=200, text="""{"name": "feeds/123"}""")
  ]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = "Feed updated successfully with Feed ID: 123"
  result = runner.invoke(update, ["--credential_file", ""])
  assert expected_output in result.output


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.update.UPDATE_BACKUP_FILE",
    TEMP_UPDATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.update.click.prompt")
@mock.patch(
    "feeds.commands.update.click.confirm")
def test_update_retry_false_400(mock_confirm: mock.MagicMock,
                                mock_input: mock.MagicMock,
                                mock_client: mock.MagicMock,
                                mock_request_body: mock.MagicMock,
                                get_feed_not_exist_data: Tuple[Dict[str, str],
                                                               str],
                                get_feed_schema: Tuple[str, str]) -> None:
  """Test case to not do retry updation of feed when retry confirm is false.

  Args:
    mock_confirm: Mock object for click confirm
    mock_input: Mock object for click prompt
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_not_exist_data: Test data
    get_feed_schema: Test data
  """
  content = {
      "name": "feeds/123",
      "details.log_type": "DUMMY_LOGTYPE",
      "details.feed_source_type": "DUMMY",
      "details.key": "value",
      "feed_state": "INACTIVE",
      "feedSourceType": "DUMMY",
      "display_source_type": "Dummy Source Type",
      "logType": "DUMMY_LOGTYPE",
      "display_log_type": "Dummy LogType"
  }
  create_backup_file(TEMP_UPDATE_BACKUP_FILE, content)
  mock_client.return_value = mock.Mock()
  mock_confirm.side_effect = [False]
  mock_input.side_effect = ["123"]
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_feed_not_exist_data,
      MockResponse(status_code=200, text="""{"name": "feeds/123"}""")
  ]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = "Feed does not exist."
  result = runner.invoke(update, ["--credential_file", ""])
  assert expected_output in result.output
  assert not os.path.exists(TEMP_UPDATE_BACKUP_FILE)


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.update.click.prompt")
def test_update_fail_get_call(mock_input: mock.MagicMock,
                              mock_client: mock.MagicMock,
                              mock_request_body: mock.MagicMock,
                              get_feed_not_exist_data: Tuple[Dict[str, str],
                                                             str],
                              get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check fail call of Get request for feed id.

  Args:
    mock_input: Mock object for click prompt
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_not_exist_data: Test data
    get_feed_schema: Test data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema, get_feed_not_exist_data,
      MockResponse(status_code=200, text="""{"name": "feeds/123"}""")
  ]
  mock_input.side_effect = [1, 1]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = "Feed does not exist."
  result = runner.invoke(update, ["--credential_file", ""])
  assert expected_output in result.output
