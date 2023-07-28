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
"""Tests for get_validation_report.py."""

from unittest import mock

from click import testing

from google3.third_party.chronicle.cli import mock_test_utility
from common.constants import http_method
from parsers import url
from parsers.commands import get_validation_report
from parsers.tests.fixtures import *  # pylint: disable=wildcard-import


runner = testing.CliRunner()
PARSER_RESOURCES = {
    "project": "test_project",
    "location": "us",
    "instance": "test_instance",
    "log_type": "test_log_type",
    "parser": "test_parser_id",
    "validationReport": "test_validation_report_id"
}
PARSEREXTENSION_RESOURCES = {
    "project": "test_project",
    "location": "us",
    "instance": "test_instance",
    "log_type": "test_log_type",
    "parserExtension": "test_parserextension_id",
    "validationReport": "test_validation_report_id"
}
GET_PARSER_VALIDATION_REPORT_URL = url.get_dataplane_url(
    "us",
    "get_parser_validation_report",
    "prod",
    PARSER_RESOURCES)
GET_PARSEREXTENSION_VALIDATION_REPORT_URL = url.get_dataplane_url(
    "us",
    "get_parserextension_validation_report",
    "prod",
    PARSEREXTENSION_RESOURCES)
LIST_PARSER_PARSING_ERRORS_URL = url.get_dataplane_url(
    "us",
    "list_parser_parsing_errors",
    "prod",
    PARSER_RESOURCES,
)
LIST_PARSEREXTENSION_PARSING_ERRORS_URL = url.get_dataplane_url(
    "us",
    "list_parserextension_parsing_errors",
    "prod",
    PARSEREXTENSION_RESOURCES,
)


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_for_parser(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_get_validation_report_for_parser: mock_test_utility.MockResponse
) -> None:
  """Test case to check success response.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_get_validation_report_for_parser: Test input data
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_get_validation_report_for_parser]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "test_project", "test_instance", "test_log_type",
      "test_validation_report_id",
      "--parser_id", "test_parser_id",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Fetching Validation report for Parser...

Validation Report:
  Verdict: PASS
  Stats:
    LogEntry Count: 1
    Successfully Normalized Log Count: 1
    Failed Log Count: 0
    Invalid Log Count: 0
    On Error Count: 1
    Event Count: 1
    Generic Event Count: 1
    Event Category:
      Valid_event: 1
    Drop Tag:
      TAG_UNSUPPORTED: 0
    Max Parse Duration: 1s
    Avg Parse Duration: 1s
    Normalization percent: 100
    Generic Event percent: 100
  Errors: -
""" == result.output
  mock_get_dataplane_url.assert_called_once_with(
      "US", "get_parser_validation_report", "prod", PARSER_RESOURCES)
  mock_http_session.return_value.request.assert_called_once_with(
      http_method.GET,
      GET_PARSER_VALIDATION_REPORT_URL,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_for_parserextension(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_get_validation_report_for_parserextension: mock_test_utility.MockResponse
) -> None:
  """Test case to check success response.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_get_validation_report_for_parserextension: Test input data
  """
  mock_get_dataplane_url.return_value = (
      GET_PARSEREXTENSION_VALIDATION_REPORT_URL)
  client = mock.Mock()
  client.request.side_effect = [
      test_data_get_validation_report_for_parserextension]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "test_project", "test_instance", "test_log_type",
      "test_validation_report_id",
      "--parserextension_id", "test_parserextension_id",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Fetching Validation report for ParserExtension...

Validation Report:
  Verdict: PASS
  Stats:
    LogEntry Count: 1
    Successfully Normalized Log Count: 1
    Failed Log Count: 0
    Invalid Log Count: 0
    On Error Count: 1
    Event Count: 1
    Generic Event Count: 1
    Event Category:
      Valid_event: 1
    Drop Tag:
      TAG_UNSUPPORTED: 0
    Max Parse Duration: 1s
    Avg Parse Duration: 1s
    Normalization percent: 100
    Generic Event percent: 100
  Errors: -
""" == result.output
  mock_get_dataplane_url.assert_called_once_with(
      "US", "get_parserextension_validation_report", "prod",
      PARSEREXTENSION_RESOURCES)
  mock_http_session.return_value.request.assert_called_once_with(
      http_method.GET,
      GET_PARSEREXTENSION_VALIDATION_REPORT_URL,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_v2_flag_not_provided(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_v2flag_not_provided: mock_test_utility.MockResponse) -> None:
  """Test case to check response for v2 flag not provided.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_v2flag_not_provided (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = [test_v2flag_not_provided]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [])
  assert ("--v2 flag not provided. "
          "Please provide the flag to run the new commands\n") == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_empty_project_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_project_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Project ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_project_id (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_project_id]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Project ID not provided. Please enter Project ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_empty_customer_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_customer_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Customer ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_customer_id (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_customer_id]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "test_project",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Customer ID not provided. Please enter Customer ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_empty_log_type(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_log_type: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Log Type.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_log_type (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_log_type]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "test_project", "test_instance",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Log Type not provided. Please enter Log Type
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_empty_validation_report_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_valdiation_report_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Parser ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_valdiation_report_id (mock_test_utility.MockResponse): Test input
      data
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_valdiation_report_id]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "test_project", "test_instance", "test_log_type",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Validation Report ID not provided. Please enter Validation Report ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_empty_parser_id_and_parserextension_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_parser_id_and_parserextension_id: mock_test_utility.MockResponse
) -> None:
  """Test case to check response for empty Parser ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_parser_id_and_parserextension_id: Test input data
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_parser_id_and_parserextension_id]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "test_project", "test_instance", "test_log_type",
      "test_validation_report_id",
      "--v2", "--env", "PROD", "--region", "US"])
  assert ("Parser ID or ParserExtension ID not provided. "
          "Parser ID or ParserExtension ID not provided\n") == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_non_empty_parser_id_and_parserextension_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_non_empty_parser_id_and_parserextension_id: mock_test_utility.MockResponse
) -> None:
  """Test case to check response for empty Parser ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_non_empty_parser_id_and_parserextension_id: Test input data
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = [test_non_empty_parser_id_and_parserextension_id]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "test_project", "test_instance", "test_log_type",
      "test_validation_report_id",
      "--parser_id", "test_parser_id",
      "--parserextension_id", "test_parserextension_id",
      "--v2", "--env", "PROD", "--region", "US"])
  assert ("Parser ID and ParserExtension ID provided. "
          "Please enter Parser or ParserExtension ID\n") == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_empty_response(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock) -> None:
  """Test case to check empty response.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = [
      mock_test_utility.MockResponse(status_code=200, text="""{}""")
  ]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "test_project", "test_instance", "test_log_type",
      "test_validation_report_id",
      "--parser_id", "test_parser_id",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Fetching Validation report for Parser...
No Validation report found for Parser.
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_500(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_500_resp: mock_test_utility.MockResponse) -> None:
  """Test case to check response for 500 response code.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_500_resp (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = [test_500_resp]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "test_project", "test_instance", "test_log_type",
      "test_validation_report_id",
      "--parser_id", "test_parser_id",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Fetching Validation report for Parser...
Error while fetching validation report for Parser.
Response Code: 500
Error: test error
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_missing_key(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_get_validation_report_missing_key: mock_test_utility.MockResponse
    ) -> None:
  """Test case to verify if key is missing from one of the parser details dict.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_get_validation_report_missing_key: Test input data
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_get_validation_report_missing_key]
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "test_project", "test_instance", "test_log_type",
      "test_validation_report_id",
      "--parser_id", "test_parser_id",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Fetching Validation report for Parser...

Key 'verdict' not found in the response.
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_get_validation_report_exception(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock) -> None:
  """Test case to verify console output in case of exception.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
  """
  mock_get_dataplane_url.return_value = GET_PARSER_VALIDATION_REPORT_URL
  client = mock.Mock()
  client.request.side_effect = Exception("test error message")
  mock_http_session.return_value = client
  result = runner.invoke(get_validation_report.get_validation_report, [
      "test_project", "test_instance", "test_log_type",
      "test_validation_report_id",
      "--parser_id", "test_parser_id",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Fetching Validation report for Parser...
Failed with exception: test error message
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsing_errors_for_parser(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_list_parsing_errors_for_parser: mock_test_utility.MockResponse
) -> None:
  """Test case to check success response.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_list_parsing_errors_for_parser: Test input data
  """
  mock_get_dataplane_url.return_value = LIST_PARSER_PARSING_ERRORS_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_list_parsing_errors_for_parser]
  mock_http_session.return_value = client
  got = get_validation_report.list_parsing_errors(
      credential_file="",
      region="US",
      env="prod",
      project_id="test_project",
      customer_id="test_instance",
      log_type="test_log_type",
      validation_report_id="test_validation_report_id",
      parser_id="test_parser_id",
      parserextension_id="",
  )
  assert """
    Log: test_log
    Error: test_error""" == got
  mock_get_dataplane_url.assert_called_once_with(
      "US",
      "list_parser_parsing_errors",
      "prod",
      PARSER_RESOURCES)
  mock_http_session.return_value.request.assert_called_once_with(
      http_method.GET,
      LIST_PARSER_PARSING_ERRORS_URL,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsing_errors_for_parserextension(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_list_parsing_errors_for_parserextension: mock_test_utility.MockResponse
) -> None:
  """Test case to check success response.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_list_parsing_errors_for_parserextension: Test input data
  """
  mock_get_dataplane_url.return_value = (
      LIST_PARSEREXTENSION_PARSING_ERRORS_URL)
  client = mock.Mock()
  client.request.side_effect = [
      test_data_list_parsing_errors_for_parserextension]
  mock_http_session.return_value = client
  got = get_validation_report.list_parsing_errors(
      credential_file="",
      region="US",
      env="prod",
      project_id="test_project",
      customer_id="test_instance",
      log_type="test_log_type",
      validation_report_id="test_validation_report_id",
      parser_id="",
      parserextension_id="test_parserextension_id",
  )
  assert """
    Log: test_log
    Error: test_error""" == got
  mock_get_dataplane_url.assert_called_once_with(
      "US",
      "list_parserextension_parsing_errors",
      "prod",
      PARSEREXTENSION_RESOURCES)
  mock_http_session.return_value.request.assert_called_once_with(
      http_method.GET,
      LIST_PARSEREXTENSION_PARSING_ERRORS_URL,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_list_parsing_errors_empty_response(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock) -> None:
  """Test case to check empty response.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
  """
  mock_get_dataplane_url.return_value = LIST_PARSER_PARSING_ERRORS_URL
  client = mock.Mock()
  client.request.side_effect = [
      mock_test_utility.MockResponse(status_code=200, text="""{}""")
  ]
  mock_http_session.return_value = client
  got = get_validation_report.list_parsing_errors(
      credential_file="",
      region="US",
      env="prod",
      project_id="test_project",
      customer_id="test_instance",
      log_type="test_log_type",
      validation_report_id="test_validation_report_id",
      parser_id="test_parser_id",
      parserextension_id="",
  )
  assert "-" == got
