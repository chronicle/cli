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
"""Tests for delete_parser.py."""

from unittest import mock

from click import testing

from google3.third_party.chronicle.cli import mock_test_utility
from parsers import url
from parsers.commands import delete_parser
from parsers.tests.fixtures import *  # pylint: disable=wildcard-import

runner = testing.CliRunner()
RESOURCES = {
    "project": "test_project",
    "location": "us",
    "instance": "test_instance",
    "log_type": "test_log_type",
    "parser": "test_parser_id",
}
DELETE_URL = url.get_dataplane_url("us", "delete_parser", "prod", RESOURCES)


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_delete_parser(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_data_delete_parser: mock_test_utility.MockResponse) -> None:
  """Test case to check response for delete parser.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_data_delete_parser (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = DELETE_URL
  client = mock.Mock()
  client.request.side_effect = [test_data_delete_parser]
  mock_http_session.return_value = client
  result = runner.invoke(delete_parser.delete_parser, [
      "test_project", "test_instance", "test_log_type", "test_parser_id",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Deleting Parser...
Parser deleted successfully.
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_delete_parser_v2_flag_not_provided(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_v2flag_not_provided: mock_test_utility.MockResponse) -> None:
  """Test case to check response for v2 flag not provided.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_v2flag_not_provided (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = DELETE_URL
  client = mock.Mock()
  client.request.side_effect = [test_v2flag_not_provided]
  mock_http_session.return_value = client
  result = runner.invoke(delete_parser.delete_parser, [])
  assert ("--v2 flag not provided. "
          "Please provide the flag to run the new commands\n") == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_delete_parser_empty_project_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_project_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Project ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_project_id (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = DELETE_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_project_id]
  mock_http_session.return_value = client
  result = runner.invoke(delete_parser.delete_parser, [
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Project ID not provided. Please enter Porject ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_delete_parser_empty_customer_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_customer_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Customer ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_customer_id (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = DELETE_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_customer_id]
  mock_http_session.return_value = client
  result = runner.invoke(delete_parser.delete_parser, [
      "test_project",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Customer ID not provided. Please enter Customer ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_delete_parser_empty_log_type(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_log_type: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Log Type.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_log_type (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = DELETE_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_log_type]
  mock_http_session.return_value = client
  result = runner.invoke(delete_parser.delete_parser, [
      "test_project", "test_instance",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Log Type not provided. Please enter Log Type
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_delete_parser_empty_parser_id(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_empty_parser_id: mock_test_utility.MockResponse) -> None:
  """Test case to check response for empty Parser ID.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_empty_parser_id (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = DELETE_URL
  client = mock.Mock()
  client.request.side_effect = [test_empty_parser_id]
  mock_http_session.return_value = client
  result = runner.invoke(delete_parser.delete_parser, [
      "test_project", "test_instance", "test_log_type",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Parser ID not provided. Please enter Parser ID
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_delete_parser_500(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock,
    test_500_resp: mock_test_utility.MockResponse) -> None:
  """Test case to check response for 500 response code.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
    test_500_resp (mock_test_utility.MockResponse): Test input data
  """
  mock_get_dataplane_url.return_value = DELETE_URL
  client = mock.Mock()
  client.request.side_effect = [test_500_resp]
  mock_http_session.return_value = client
  result = runner.invoke(delete_parser.delete_parser, [
      "test_project", "test_instance", "test_log_type", "test_parser_id",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Deleting Parser...
Error while deleting parser.
Response Code: 500
Error: test error
""" == result.output


@mock.patch(
    "common.chronicle_auth.initialize_dataplane_http_session"
)
@mock.patch("parsers.url.get_dataplane_url")
def test_delete_parser_exception(
    mock_get_dataplane_url: mock.MagicMock,
    mock_http_session: mock.MagicMock) -> None:
  """Test case to verify console output in case of exception.

  Args:
    mock_get_dataplane_url (mock.MagicMock): Mock object
    mock_http_session (mock.MagicMock): Mock object
  """
  mock_get_dataplane_url.return_value = DELETE_URL
  client = mock.Mock()
  client.request.side_effect = Exception("test error message")
  mock_http_session.return_value = client
  result = runner.invoke(delete_parser.delete_parser, [
      "test_project", "test_instance", "test_log_type", "test_parser_id",
      "--v2", "--env", "PROD", "--region", "US"])
  assert """Deleting Parser...
Failed with exception: test error message
""" == result.output
