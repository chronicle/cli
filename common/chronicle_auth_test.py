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
"""Unit tests for chronicle_auth.py."""

from unittest import mock
from google.oauth2 import service_account
from common import chronicle_auth
from feeds.tests.fixtures import create_service_account_file
from feeds.tests.fixtures import TEMP_SERVICE_ACCOUNT_FILE


@mock.patch.object(service_account.Credentials, "from_service_account_file")
def test_initialize_http_session(mock_from_service_account_file):
  """Test to check if http session is initialize or not.

  Args:
    mock_from_service_account_file (mock.MagicMock): Mock object
  """
  create_service_account_file()
  chronicle_auth.initialize_http_session("")
  mock_from_service_account_file.assert_called_once_with(
      filename=str(chronicle_auth.default_cred_file_path),
      scopes=chronicle_auth.AUTHORIZATION_SCOPES)


@mock.patch.object(service_account.Credentials, "from_service_account_file")
def test_initialize_http_session_with_custom_json_credentials(
    mock_from_service_account_file):
  """Test to check if http session is initialize with custom credentials.

  Args:
    mock_from_service_account_file (mock.MagicMock): Mock object
  """
  create_service_account_file()
  chronicle_auth.initialize_http_session(TEMP_SERVICE_ACCOUNT_FILE)
  mock_from_service_account_file.assert_called_once_with(
      filename=TEMP_SERVICE_ACCOUNT_FILE,
      scopes=chronicle_auth.AUTHORIZATION_SCOPES)
