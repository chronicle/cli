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
"""Fixtures for bigquery commands."""

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
  """Creates temporary config file with the content.

  Args:
    file_path (str): Path to create the temp config file.
    content (str): content to be written in the file.
  """
  with open(file_path, "w") as file:
    if content:
      file.write(content)


@pytest.fixture()
def test_500_resp() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=500,
      text="""{"error": {"code": 500, "message": "test error"}}""")


@pytest.fixture()
def test_provide_access_data() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=200, text="""{"email": "test_email_id@testcompany.com"}""")


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
