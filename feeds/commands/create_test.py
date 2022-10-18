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
"""Unit tests for create.py."""

import os
from typing import Tuple
from unittest import mock

from click._compat import WIN
from click.testing import CliRunner

from feeds.commands.create import create
from feeds.commands.create import Properties
from feeds.tests.fixtures import *  # pylint: disable=wildcard-import
from feeds.tests.fixtures import create_backup_file
from feeds.tests.fixtures import TEMP_CREATE_BACKUP_FILE
from mock_test_utility import MockResponse


runner = CliRunner()


@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
def test_create_credential_file_invalid(mock_client: mock.MagicMock) -> None:
  """Test case for checking invalid credential path.

  Args:
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = OSError(
      "Credential Path not found.")
  expected_message = "Failed with exception: Credential Path not found."
  result = runner.invoke(create, ["--credential_file", "dummy.json"])
  assert expected_message in result.output


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.create.CREATE_BACKUP_FILE",
    TEMP_CREATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.create.click.prompt")
def test_create_success(mock_input: mock.MagicMock, mock_client: mock.MagicMock,
                        mock_request_body: mock.MagicMock,
                        get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check successful creation of feed.

  Args:
    mock_input: Mock object for click prompt
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_schema: Test data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema,
      MockResponse(status_code=200, text="""{"name": "feeds/123"}""")
  ]
  mock_input.side_effect = [2, 1, "Dummy feed display name"]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  result = runner.invoke(create, ["--credential_file", ""])
  if WIN:
    assert """========== Set Properties ==========
====================================

List of Source types:
1. Dummy Source Type
2. Dummy Source Type 2
3. Dummy Source Type 3

You have selected Dummy Source Type 2
List of Log types:

(i) How to select log type?
  - Press ENTER key (scrolls one line at a time) or SPACEBAR key (display next screen).
  - Note down the choice number for the log type that you want to select.
  - Press 'q' to quit and enter that choice number.
=============================================================================
1. Dummy LogType2 (DUMMY_LOGTYPE2)


You have selected Dummy LogType2


======================================
=========== Input Parameters =========
======================================
(*) - Required fields.
Password/secret inputs are hidden.

Feed created successfully with Feed ID: 123""" in result.output
  else:
    assert """========== Set Properties ==========
====================================

List of Source types:
1. Dummy Source Type
2. Dummy Source Type 2
3. Dummy Source Type 3

You have selected Dummy Source Type 2
List of Log types:

(i) How to select log type?
  - Press Up/b or Down/z keys to paginate.
  - To switch case-sensitivity, press '-i' and press enter. By default, search
    is case-sensitive.
  - To search for specific log type, press '/' key, enter text and press enter.
  - Note down the choice number for the log type that you want to select.
  - Press 'q' to quit and enter that choice number.
  - Press `h` for all the available options to navigate the list.
=============================================================================
1. Dummy LogType2 (DUMMY_LOGTYPE2)


You have selected Dummy LogType2


======================================
=========== Input Parameters =========
======================================
(*) - Required fields.
Password/secret inputs are hidden.

Feed created successfully with Feed ID: 123""" in result.output


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.create.CREATE_BACKUP_FILE",
    TEMP_CREATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.create.click.prompt")
def test_create_error_code(mock_input: mock.MagicMock,
                           mock_client: mock.MagicMock,
                           mock_request_body: mock.MagicMock,
                           get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check failure of creation of feed.

  Args:
    mock_input: Mock object for click prompt
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_schema: Test data
  """
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema,
      MockResponse(status_code=400, text="""{"error": {"message": "test"}}""")
  ]
  mock_input.side_effect = [1, 1, "Dummy feed display name"]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = ("Error occurred while creating feed.\nResponse Code: "
                     "400.\nError: test")
  result = runner.invoke(create, ["--credential_file", ""])
  assert expected_output in result.output
  assert os.path.exists(TEMP_CREATE_BACKUP_FILE)


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.create.CREATE_BACKUP_FILE",
    TEMP_CREATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.create.click.confirm")
def test_create_retry_true(mock_confirm: mock.MagicMock,
                           mock_client: mock.MagicMock,
                           mock_request_body: mock.MagicMock,
                           get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check retry of creation of feed.

  Args:
    mock_confirm: Mock object for click confirm
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_schema: Test data
  """
  content = {
      "details.key": "value",
      "displayName": "Dummy feed display name",
      "feed_state": "INACTIVE",
      "feedSourceType": "DUMMY",
      "display_source_type": "Dummy Source Type",
      "logType": "DUMMY_LOGTYPE",
      "display_log_type": "Dummy LogType"
  }
  create_backup_file(TEMP_CREATE_BACKUP_FILE, content)
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema,
      MockResponse(status_code=200, text="""{"name": "feeds/123"}""")
  ]
  mock_confirm.side_effect = [True]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = "Feed created successfully with Feed ID: 123"
  result = runner.invoke(create, ["--credential_file", ""])
  assert expected_output in result.output
  assert not os.path.exists(TEMP_CREATE_BACKUP_FILE)


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.create.CREATE_BACKUP_FILE",
    TEMP_CREATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.create.log_source_types_from_user"
)
@mock.patch(
    "feeds.commands.create.click.confirm")
@mock.patch(
    "feeds.commands.create.click.prompt")
def test_create_retry_false_400(mock_input: mock.MagicMock,
                                mock_confirm: mock.MagicMock,
                                mock_user_log_source: mock.MagicMock,
                                mock_client: mock.MagicMock,
                                mock_request_body: mock.MagicMock,
                                get_feed_schema: Tuple[str, str]) -> None:
  """Test case to not do retry creation of feed when retry confirm is false.

  Args:
    mock_input: Mock object for click prompt
    mock_confirm: Mock object for click confirm
    mock_user_log_source: Mock object
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_schema: Test data
  """
  content = {
      "details.key": "value",
      "displayName": "Dummy feed display name",
      "feed_state": "INACTIVE",
      "feedSourceType": "TEST",
      "display_source_type": "Dummy Source Type",
      "logType": "DUMMY_LOGTYPE",
      "display_log_type": "Dummy LogType"
  }
  create_backup_file(TEMP_CREATE_BACKUP_FILE, content)
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema,
      MockResponse(status_code=400, text="""{"error": {"message": "test"}}""")
  ]
  mock_confirm.side_effect = [False]
  mock_input.side_effect = [1, 1, "Dummy feed display name"]
  mock_user_log_source.return_value = Properties("DUMMY_LOGTYPE", "TEST",
                                                 "DUMMY_FEED_DISPLAY_NAME")
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = "Schema Not Found."
  result = runner.invoke(create, ["--credential_file", ""])
  assert expected_output in result.output
  assert not os.path.exists(TEMP_CREATE_BACKUP_FILE)


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.create.CREATE_BACKUP_FILE",
    TEMP_CREATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.create.click.confirm")
@mock.patch(
    "feeds.commands.create.click.prompt")
def test_create_retry_false(mock_input: mock.MagicMock,
                            mock_confirm: mock.MagicMock,
                            mock_client: mock.MagicMock,
                            mock_request_body: mock.MagicMock,
                            get_feed_schema: Tuple[str, str]) -> None:
  """Test case to not do retry creation of feed when retry confirm is false.

  Args:
    mock_input: Mock object for click prompt
    mock_confirm: Mock object for click confirm
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_schema: Test data
  """
  content = {
      "details.key": "value",
      "displayName": "Dummy feed display name",
      "feed_state": "INACTIVE",
      "feedSourceType": "TEST",
      "display_source_type": "Dummy Source Type",
      "logType": "DUMMY_LOGTYPE",
      "display_log_type": "Dummy LogType"
  }
  create_backup_file(TEMP_CREATE_BACKUP_FILE, content)
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema,
      MockResponse(status_code=200, text="""{"name": "feeds/123"}""")
  ]
  mock_confirm.side_effect = [False]
  mock_input.side_effect = [1, 1, "Dummy feed display name"]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = "Feed created successfully with Feed ID: 123"
  result = runner.invoke(create, ["--credential_file", ""])
  assert expected_output in result.output
  assert not os.path.exists(TEMP_CREATE_BACKUP_FILE)


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.create.CREATE_BACKUP_FILE",
    TEMP_CREATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.create.click.confirm")
def test_create_retry_true_400(mock_confirm: mock.MagicMock,
                               mock_client: mock.MagicMock,
                               mock_request_body: mock.MagicMock,
                               get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check retry of creation of feed.

  Args:
    mock_confirm: Mock object for click confirm
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_schema: Test data
  """
  content = {
      "details.key": "value",
      "displayName": "Feed Display Name",
      "feed_state": "INACTIVE",
      "feedSourceType": "TEST",
      "display_source_type": "Dummy Source Type",
      "logType": "DUMMY_LOGTYPE",
      "display_log_type": "Dummy LogType"
  }
  create_backup_file(TEMP_CREATE_BACKUP_FILE, content)
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema,
      MockResponse(status_code=400, text="""{"error": {"message": "test"}}""")
  ]
  mock_confirm.side_effect = [True]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = "Schema Not Found."
  result = runner.invoke(create, ["--credential_file", ""])
  assert expected_output in result.output
  assert os.path.exists(TEMP_CREATE_BACKUP_FILE)


@mock.patch(
    "feeds.feed_schema_utility.FeedSchema.prepare_request_body"
)
@mock.patch(
    "feeds.commands.create.CREATE_BACKUP_FILE",
    TEMP_CREATE_BACKUP_FILE)
@mock.patch(
    "feeds.feed_schema_utility.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "feeds.commands.create.click.prompt")
def test_create_success_empty_backup(mock_input: mock.MagicMock,
                                     mock_client: mock.MagicMock,
                                     mock_request_body: mock.MagicMock,
                                     get_feed_schema: Tuple[str, str]) -> None:
  """Test case to check successful creation of feed.

  Args:
    mock_input: Mock object for click prompt
    mock_client: Mock object
    mock_request_body: Mock object
    get_feed_schema: Test data
  """
  create_backup_file(TEMP_CREATE_BACKUP_FILE, None)
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_feed_schema,
      MockResponse(status_code=200, text="""{"name": "feeds/123"}""")
  ]
  mock_input.side_effect = [1, 1, "Dummy feed display name"]
  mock_request_body.return_value = ({
      "details": {
          "key": "value",
          "feedSourceType": "DUMMY",
          "logType": "DUMMY_LOGTYPE"
      }
  }, {})
  expected_output = "Feed created successfully with Feed ID: 123"
  result = runner.invoke(create, ["--credential_file", ""])
  assert expected_output in result.output
