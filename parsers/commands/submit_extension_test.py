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
"""Tests for submit_extension.py."""

from unittest import mock

from click import testing

from google3.third_party.chronicle.cli import mock_test_utility
from parsers import url
from parsers.commands import submit_extension
from parsers.tests.fixtures import *  # pylint: disable=wildcard-import
from parsers.tests.fixtures import create_temp_config_file
from parsers.tests.fixtures import create_temp_log_file
from parsers.tests.fixtures import TEMP_SUBMIT_CONF_FILE
from parsers.tests.fixtures import TEMP_SUBMIT_LOG_FILE


runner = testing.CliRunner()
RESOURCES = {
    "project": "test_project",
    "location": "us",
    "instance": "test_instance",
    "log_type": "test_log_type"
}
SUBMIT_URL = url.get_dataplane_url("us", "submit_extension", "prod", RESOURCES)


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_submit_extension(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_submit_extension: mock_test_utility.MockResponse) -> None:
  """Test case to check success response.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_submit_extension (mock_test_utility.MockResponse): Test input data
  """
  create_temp_config_file(TEMP_SUBMIT_CONF_FILE, "test_config")
  create_temp_log_file(TEMP_SUBMIT_LOG_FILE, "test_log")
  mock_get_dataplane_url.return_value = SUBMIT_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_submit_extension]
  mock_http_session.return_value = client
  result = runner.invoke(submit_extension.submit_extension, [
      "test_project", "test_instance", "test_log_type",
      TEMP_SUBMIT_CONF_FILE, TEMP_SUBMIT_LOG_FILE,
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Submitting Parser Extension...

ParserExtension Details:
  ParserExtension ID: test_parserextension_id
  Log type: test_log_type
  State: LIVE
  Validation Report ID: -
  Create Time: 2023-01-01T00:00:00.000000Z
  State Last Changed Time: 2023-01-01T00:00:00.000000Z
  Last Live Time: -

============================================================

""" == result.output
  mock_get_dataplane_url.assert_called_once_with(
      "US", "submit_extension", "prod", RESOURCES)
  mock_http_session.return_value.request.assert_called_once_with(
      "POST", SUBMIT_URL, json={
          "cbn_snippet": "dGVzdF9jb25maWc=",
          "log": "dGVzdF9sb2c=",
      }, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_submit_extension_v2_flag_not_provided(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_v2flag_not_provided: mock_test_utility.MockResponse) -> None:
  """Test case to check response for v2 flag not provided.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_v2flag_not_provided (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = SUBMIT_URL
  client = mock.Mock()
  client.request.side_effect = [test_v2flag_not_provided]
  mock_http_session.return_value = client
  result = runner.invoke(submit_extension.submit_extension, [])
  assert ("--v2 flag not provided. "
          "Please provide the flag to run the new commands\n") == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_submit_extension_empty_project_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_project_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Project ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_project_id (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = SUBMIT_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_project_id]
  mock_http_session.return_value = client
  result = runner.invoke(submit_extension.submit_extension, [
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Project ID not provided. Please enter Project ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_submit_extension_empty_customer_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_customer_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Customer ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_customer_id (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = SUBMIT_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_customer_id]
  mock_http_session.return_value = client
  result = runner.invoke(submit_extension.submit_extension, [
      "test_project",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Customer ID not provided. Please enter Customer ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_submit_extension_empty_log_type(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_log_type: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Log Type.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_log_type (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = SUBMIT_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_log_type]
  mock_http_session.return_value = client
  result = runner.invoke(submit_extension.submit_extension, [
      "test_project", "test_instance",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Log Type not provided. Please enter Log Type
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_submit_extension_non_existing_config_file(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_non_existing_config_file: mock_test_utility.MockResponse) -> None:
  """Test case to check response for non existing config file.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_non_existing_config_file (mock_test_utility.MockResponse): Test
      input data
  """
  mock_get_dataplane_url.return_value = SUBMIT_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_non_existing_config_file]
  mock_http_session.return_value = client
  result = runner.invoke(submit_extension.submit_extension, [
      "test_project", "test_instance", "test_log_type",
      "test_config_file", "test_log_file",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """test_config_file does not exist. Please enter valid config file path
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_submit_extension_non_existing_log_file(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_non_existing_log_file: mock_test_utility.MockResponse) -> None:
  """Test case to check response for non existing log file.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_non_existing_log_file (mock_test_utility.MockResponse): Test
      input data
  """
  create_temp_config_file(TEMP_SUBMIT_CONF_FILE, "test_config")
  mock_get_dataplane_url.return_value = SUBMIT_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_non_existing_log_file]
  mock_http_session.return_value = client
  result = runner.invoke(submit_extension.submit_extension, [
      "test_project", "test_instance", "test_log_type",
      TEMP_SUBMIT_CONF_FILE, "test_log_file",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """test_log_file does not exist. Please enter valid log file path
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_submit_extension_500(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_500_resp: mock_test_utility.MockResponse) -> None:
  """Test case to check response for 500 response code.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_500_resp (mock_test_utility.MockResponse): Test input data
  """
  create_temp_config_file(TEMP_SUBMIT_CONF_FILE, "test_config")
  create_temp_log_file(TEMP_SUBMIT_LOG_FILE, "test_log")
  mock_get_dataplane_url.return_value = SUBMIT_URL
  client = mock.Mock()
  client.request.side_effect = [test_500_resp]
  mock_http_session.return_value = client
  result = runner.invoke(submit_extension.submit_extension, [
      "test_project", "test_instance", "test_log_type",
      TEMP_SUBMIT_CONF_FILE, TEMP_SUBMIT_LOG_FILE,
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Submitting Parser Extension...
Error while submitting parser extension.
Response Code: 500
Error: test error
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_submit_extension_exception(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock) -> None:
  """Test case to verify console output in case of exception.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
  """
  create_temp_config_file(TEMP_SUBMIT_CONF_FILE, "test_config")
  create_temp_log_file(TEMP_SUBMIT_LOG_FILE, "test_log")
  mock_get_dataplane_url.return_value = SUBMIT_URL
  client = mock.Mock()
  client.request.side_effect = Exception("test error message")
  mock_http_session.return_value = client
  result = runner.invoke(submit_extension.submit_extension, [
      "test_project", "test_instance", "test_log_type",
      TEMP_SUBMIT_CONF_FILE, TEMP_SUBMIT_LOG_FILE,
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Submitting Parser Extension...
Failed with exception: test error message
""" == result.output
