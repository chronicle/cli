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
"""Tests for list_parsers.py."""

import os
from unittest import mock

from click import _compat
from click import testing

from google3.third_party.chronicle.cli import mock_test_utility
from common import file_utility
from parsers import url
from parsers.commands import list_parsers
from parsers.tests import fixtures
from parsers.tests.fixtures import *  # pylint: disable=wildcard-import


runner = testing.CliRunner()
RESOURCES = {
    "project": "test_project",
    "location": "us",
    "instance": "test_instance",
    "log_type": "test_log_type",
}
LIST_URL = url.get_dataplane_url("us", "list_parsers", "prod", RESOURCES)


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsers(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_list_parsers: mock_test_utility.MockResponse) -> None:
  """Test case to check response for list parsers.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_list_parsers (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = LIST_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_list_parsers]
  mock_http_session.return_value = client
  result = runner.invoke(list_parsers.list_parsers, [
      "test_project", "test_instance", "test_log_type",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Fetching list of parsers...

Parser Details:
  Parser ID: test_parser_id
  Log type: test_log_type
  State: ACTIVE
  Type: CUSTOM
  Author: test_author
  Validation Report ID: test_validation_report_id
  Create Time: 2023-01-01T00:00:00.000000Z

============================================================

""" == result.output
  mock_get_dataplane_url.assert_called_once_with(
      "US", "list_parsers", "prod",
      RESOURCES, filter="TYPE = CUSTOM", page_size=1000)
  mock_http_session.return_value.request.assert_called_once_with(
      "GET", LIST_URL, timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsers_v2_flag_not_provided(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_v2flag_not_provided: mock_test_utility.MockResponse) -> None:
  """Test case to check response for v2 flag not provided.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_v2flag_not_provided (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = LIST_URL
  client = mock.Mock()
  client.request.side_effect = [test_v2flag_not_provided]
  mock_http_session.return_value = client
  result = runner.invoke(list_parsers.list_parsers, [])
  assert ("--v2 flag not provided. "
          "Please provide the flag to run the new commands\n") == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsers_empty_project_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_project_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Project ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_project_id (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = LIST_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_project_id]
  mock_http_session.return_value = client
  result = runner.invoke(list_parsers.list_parsers, [
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Project ID not provided. Please enter Project ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsers_empty_customer_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_customer_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Customer ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_customer_id (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = LIST_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_customer_id]
  mock_http_session.return_value = client
  result = runner.invoke(list_parsers.list_parsers, [
      "test_project",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Customer ID not provided. Please enter Customer ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsers_empty_response(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock) -> None:
  """Test case to check empty response for list parsers.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
  """
  mock_get_dataplane_url.return_value = LIST_URL
  client = mock.Mock()
  client.request.side_effect = [
      mock_test_utility.MockResponse(status_code=200, text="""{}""")
  ]
  mock_http_session.return_value = client
  result = runner.invoke(list_parsers.list_parsers, [
      "test_project", "test_instance", "test_log_type",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Fetching list of parsers...
No Parsers currently configured.
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsers_command_500(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_500_resp: mock_test_utility.MockResponse
    ) -> None:
  """Test case to check response for list parsers for 500 response code.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_500_resp (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = LIST_URL
  client = mock.Mock()
  client.request.side_effect = [test_500_resp]
  mock_http_session.return_value = client
  result = runner.invoke(list_parsers.list_parsers, [
      "test_project", "test_instance", "test_log_type",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Fetching list of parsers...
Error while fetching list of parsers.
Response Code: 500
Error: test error
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsers_missing_key(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_list_parsers_missing_key: mock_test_utility.MockResponse) -> None:
  """Test case to verify if key is missing from one of the parser details dict.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_list_parsers_missing_key (mock_test_utility.MockResponse): Test
      input data
  """
  mock_get_dataplane_url.return_value = LIST_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_list_parsers_missing_key]
  mock_http_session.return_value = client
  result = runner.invoke(list_parsers.list_parsers, [
      "test_project", "test_instance", "test_log_type",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Fetching list of parsers...

Parser Details:
  Parser ID: test_parser_id1
  Log type: test_log_type1
  State: ACTIVE
  Type: CUSTOM
  Author: test_author1
  Validation Report ID: test_validation_report_id1
  Create Time: 2023-01-01T00:00:00.000000Z

============================================================

Key 'state' not found in the response.

============================================================

Parser Details:
  Parser ID: test_parser_id3
  Log type: test_log_type3
  State: INACTIVE
  Type: CUSTOM
  Author: test_author3
  Validation Report ID: test_validation_report_id3
  Create Time: 2023-01-01T00:00:00.000000Z

============================================================

""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsers_exception(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock) -> None:
  """Test case to verify console output in case of exception.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
  """
  mock_get_dataplane_url.return_value = LIST_URL
  client = mock.Mock()
  client.request.side_effect = Exception("test error message")
  mock_http_session.return_value = client
  result = runner.invoke(list_parsers.list_parsers, [
      "test_project", "test_instance", "test_log_type",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Fetching list of parsers...
Failed with exception: test error message
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsers_export(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_list_parsers: mock_test_utility.MockResponse) -> None:
  """Test case to check export option with TXT file format for list command.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_list_parsers (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = LIST_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_list_parsers]
  mock_http_session.return_value = client
  result = runner.invoke(list_parsers.list_parsers, [
      "test_project", "test_instance", "test_log_type",
      "--v2", "--env", "PROD", "--region", "US",
      "--export", f"{fixtures.TEST_DATA_DIR}/test"])
  assert f"""Fetching list of parsers...

Parser Details:
  Parser ID: test_parser_id
  Log type: test_log_type
  State: ACTIVE
  Type: CUSTOM
  Author: test_author
  Validation Report ID: test_validation_report_id
  Create Time: 2023-01-01T00:00:00.000000Z

============================================================


Parser details exported successfully to:\
 {os.path.join(os.getcwd(), fixtures.TEMP_TEST_TXT_FILE)}
""" == result.output
  output = file_utility.read_file(fixtures.TEMP_TEST_TXT_FILE)
  output = output.decode("utf-8")

  # "\n" is the Unix/linux for new line whereas "\r\n" is the default Windows
  # style for line separator. Hence, below condition is to handle the tests for
  # Windows OS platform.
  if _compat.WIN:
    output = "\n".join(output.splitlines()) + "\n"

  assert output == """\

Parser Details:
  Parser ID: test_parser_id
  Log type: test_log_type
  State: ACTIVE
  Type: CUSTOM
  Author: test_author
  Validation Report ID: test_validation_report_id
  Create Time: 2023-01-01T00:00:00.000000Z

============================================================
"""


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsers_export_json(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_list_parsers: mock_test_utility.MockResponse) -> None:
  """Test case to check export option with JSON format for list parsers command.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_list_parsers (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = LIST_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_list_parsers]
  mock_http_session.return_value = client
  result = runner.invoke(list_parsers.list_parsers, [
      "test_project", "test_instance", "test_log_type",
      "--v2", "--env", "PROD", "--region", "US",
      "--export", f"{fixtures.TEST_DATA_DIR}/test",
      "--file-format", "JSON"])
  assert f"""Fetching list of parsers...

Parser Details:
  Parser ID: test_parser_id
  Log type: test_log_type
  State: ACTIVE
  Type: CUSTOM
  Author: test_author
  Validation Report ID: test_validation_report_id
  Create Time: 2023-01-01T00:00:00.000000Z

============================================================


Parser details exported successfully to:\
 {os.path.join(os.getcwd(), fixtures.TEMP_TEST_JSON_FILE)}
""" == result.output
  test_file_content = file_utility.read_file(fixtures.TEMP_TEST_JSON_FILE)
  test_file_content = test_file_content.decode("utf-8")

  # "\n" is the Unix/linux for new line whereas "\r\n" is the default Windows
  # style for line separator. Hence, below condition is to handle the tests for
  # Windows OS platform.
  if _compat.WIN:
    test_file_content = "\n".join(test_file_content.splitlines())

  assert test_file_content == """{
  "parsers": [
    {
      "parserID": "test_parser_id",
      "logType": "test_log_type",
      "state": "ACTIVE",
      "type": "CUSTOM",
      "author": "test_author",
      "validationReportID": "test_validation_report_id",
      "createTime": "2023-01-01T00:00:00.000000Z"
    }
  ]
}"""
