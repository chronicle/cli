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
"""Tests for run_parser.py."""

from unittest import mock

from click import testing

from google3.third_party.chronicle.cli import mock_test_utility
from parsers import url
from parsers.commands import run_parser
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
    "log_type": "test_log_type",
}
RUN_URL = url.get_dataplane_url("us", "run_parser", "prod", RESOURCES)


@mock.patch("time.time")
@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_run_parser(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    mock_time: mock.MagicMock,
    test_data_run_parser: mock_test_utility.MockResponse) -> None:
  """Test case to check success response.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    mock_time (mock.MagicMock): Mock object
    test_data_run_parser (mock_test_utility.MockResponse): Test input data
  """
  mock_time.return_value = 0.0
  create_temp_config_file(TEMP_SUBMIT_CONF_FILE, "test_config")
  create_temp_log_file(TEMP_SUBMIT_LOG_FILE, "test_log1\ntest_log2")
  mock_get_dataplane_url.return_value = RUN_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_run_parser]
  mock_http_session.return_value = client
  result = runner.invoke(run_parser.run_parser, [
      "test_project", "test_instance", "test_log_type",
      TEMP_SUBMIT_CONF_FILE, TEMP_SUBMIT_LOG_FILE,
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Running parser(with extension) against given logs...

Log: test_log
Events: result
error: test_error_message

Runtime: 0.0s
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_run_parser_v2_flag_not_provided(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_v2flag_not_provided: mock_test_utility.MockResponse) -> None:
  """Test case to check response for v2 flag not provided.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_v2flag_not_provided (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = RUN_URL
  client = mock.Mock()
  client.request.side_effect = [test_v2flag_not_provided]
  mock_http_session.return_value = client
  result = runner.invoke(run_parser.run_parser, [])
  assert ("--v2 flag not provided. "
          "Please provide the flag to run the new commands\n") == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_run_parser_empty_project_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_project_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Project ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_project_id (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = RUN_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_project_id]
  mock_http_session.return_value = client
  result = runner.invoke(run_parser.run_parser, [
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Project ID not provided. Please enter Project ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_run_parser_empty_customer_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_customer_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Customer ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_customer_id (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = RUN_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_customer_id]
  mock_http_session.return_value = client
  result = runner.invoke(run_parser.run_parser, [
      "test_project",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Customer ID not provided. Please enter Customer ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_run_parser_empty_log_type(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_log_type: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Log Type.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_log_type (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = RUN_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_log_type]
  mock_http_session.return_value = client
  result = runner.invoke(run_parser.run_parser, [
      "test_project", "test_instance",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Log Type not provided. Please enter Log Type
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_run_parser_non_existing_config_file(
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
  mock_get_dataplane_url.return_value = RUN_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_non_existing_config_file]
  mock_http_session.return_value = client
  result = runner.invoke(run_parser.run_parser, [
      "test_project", "test_instance", "test_log_type",
      "test_config_file", "test_log_file",
      "--v2", "--env", "PROD", "--region", "US"])
  assert (
      "test_config_file does not exist. "
      "Please enter valid parser config file path\n") == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_run_parser_non_existing_log_file(
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
  mock_get_dataplane_url.return_value = RUN_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_non_existing_log_file]
  mock_http_session.return_value = client
  result = runner.invoke(run_parser.run_parser, [
      "test_project", "test_instance", "test_log_type",
      TEMP_SUBMIT_CONF_FILE, "test_log_file",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """test_log_file does not exist. Please enter valid log file path
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_run_parser_empty_response(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock) -> None:
  """Test case to check empty response.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
  """
  create_temp_config_file(TEMP_SUBMIT_CONF_FILE, "test_config")
  create_temp_log_file(TEMP_SUBMIT_LOG_FILE, "test_log1\ntest_log2")
  mock_get_dataplane_url.return_value = RUN_URL
  client = mock.Mock()
  client.request.side_effect = [
      mock_test_utility.MockResponse(status_code=200, text="""{}""")
  ]
  mock_http_session.return_value = client
  result = runner.invoke(run_parser.run_parser, [
      "test_project", "test_instance", "test_log_type",
      TEMP_SUBMIT_CONF_FILE, TEMP_SUBMIT_LOG_FILE,
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Running parser(with extension) against given logs...

Parser yielded no results.
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_run_parser_500(
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
  create_temp_log_file(TEMP_SUBMIT_LOG_FILE, "test_log1\ntest_log2")
  mock_get_dataplane_url.return_value = RUN_URL
  client = mock.Mock()
  client.request.side_effect = [test_500_resp]
  mock_http_session.return_value = client
  result = runner.invoke(run_parser.run_parser, [
      "test_project", "test_instance", "test_log_type",
      TEMP_SUBMIT_CONF_FILE, TEMP_SUBMIT_LOG_FILE,
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Running parser(with extension) against given logs...

Error while running parser(with extension).
Response Code: 500
Error: test error
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_run_parser_exception(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock) -> None:
  """Test case to verify console output in case of exception.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
  """
  create_temp_config_file(TEMP_SUBMIT_CONF_FILE, "test_config")
  create_temp_log_file(TEMP_SUBMIT_LOG_FILE, "test_log1\ntest_log2")
  mock_get_dataplane_url.return_value = RUN_URL
  client = mock.Mock()
  client.request.side_effect = Exception("test error message")
  mock_http_session.return_value = client
  result = runner.invoke(run_parser.run_parser, [
      "test_project", "test_instance", "test_log_type",
      TEMP_SUBMIT_CONF_FILE, TEMP_SUBMIT_LOG_FILE,
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Running parser(with extension) against given logs...

Failed with exception: test error message
""" == result.output
