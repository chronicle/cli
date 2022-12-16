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
"""Fixtures for parsers commands."""

import os
from typing import Any

import pytest

from mock_test_utility import MockResponse

TEST_DATA_DIR = os.path.dirname(__file__)
TEMP_TEST_TXT_FILE = os.path.join(TEST_DATA_DIR, "test.txt")
TEMP_TEST_JSON_FILE = os.path.join(TEST_DATA_DIR, "test.json")
TEMP_CONF_FILE = os.path.join(TEST_DATA_DIR,
                              "test_log_type_20220824062200.conf")
TEMP_SUBMIT_CONF_FILE = os.path.join(TEST_DATA_DIR, "test_config_file.conf")

os.system(f"chmod -R +rw {TEST_DATA_DIR}")


def create_temp_config_file(file_path: str, content: str) -> None:
  """Create temporary config file with the content.

  Args:
    file_path (str): Path to create the temp config file.
    content (str): content to be written in the file.
  """
  with open(file_path, "w") as file:
    if content:
      file.write(content)


@pytest.fixture()
def test_data_list_command() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=200,
      text="""{"cbnParsers": [{"configId": "test_config_id",
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}]}""")


@pytest.fixture()
def test_data_list_cmd_missing_key() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=200,
      text="""{"cbnParsers": [{"configId": "config 1",
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}, {
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}, {"configId": "config 2",
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}]}""")


@pytest.fixture()
def test_500_resp() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=500,
      text="""{"error": {"code": 500, "message": "test error"}}""")


@pytest.fixture()
def test_run_validation_data() -> MockResponse:
  """Test validation data."""
  return MockResponse(
      status_code=200, text="""{"result": ["result 1", "result 2"]}""")


@pytest.fixture()
def test_run_validation_error_data() -> MockResponse:
  """Test validation data."""
  return MockResponse(
      status_code=200,
      text="""{"errors": [{"errorMsg": "test error", "logEntry": "sample log"}]}"""
  )


@pytest.fixture()
def test_history_data() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=200,
      text="""{"cbnParsers": [{"configId": "test_config_id",
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config",
              "validationErrors": {"errors": [{"error": "test error 1",
              "log": "dGVzdCBsb2cgMQ=="}, {"error": "test error 2"}]}}]}""")


@pytest.fixture()
def test_archive_data() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=200,
      text="""{"configId": "test_config_id",
              "author": "test_user", "state": "ARCHIVED", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}""")


@pytest.fixture()
def error_list() -> MockResponse:
  """Test input data."""
  data = MockResponse(
      status_code=200,
      text="""{"errors": [{
      "errorId": "test_error_id",
      "configId": "test_config_id",
      "logType": "test_log_type",
      "errorTime": "2022-08-18T12:28:57.443376813Z",
      "category": "test_category",
      "errorMsg": "test_error_message",
      "logs": [
        "dGVzdF9sb2dz"
      ]
    }]}""")
  return data


@pytest.fixture()
def submit_parser() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=200,
      text="""{"configId": "test_config_id", "logType": "TEST_LOG_TYPE",
              "submitTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "state": "LIVE", "sha256": "test_sha256", "config": "test_config", 
              "author": "test_user"}""")


@pytest.fixture(scope="function", autouse=True)
def cleanup(request: Any):
  """Cleanup testing files once we are finished."""

  def remove_test_files():
    files = [
        TEMP_TEST_TXT_FILE, TEMP_TEST_JSON_FILE, TEMP_CONF_FILE,
        TEMP_SUBMIT_CONF_FILE
    ]
    for file_path in files:
      try:
        os.remove(file_path)
      except FileNotFoundError:
        pass

  request.addfinalizer(remove_test_files)


@pytest.fixture()
def status_parser() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=200,
      text="""{"configId": "test_config_id",
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}""")


@pytest.fixture()
def test_400_resp_status_command() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=400,
      text="""{"error": {"code": 400, "message": "Invalid ID."}}""")


@pytest.fixture()
def test_500_resp_status_command() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=500,
      text="""{"error": {"code": 500, "message": "could not get CBN parser."}}"""
  )


@pytest.fixture()
def generate_logs() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=200,
      text="""{"data": ["MDAsMDcvMTQvMjEsMTE6Mjk6MTcsU3RhcnRlZCwsLCwsMCw2LCwsLCwsLCwsMA=="]}"""
  )
