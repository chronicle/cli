# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Tests for provide_access.py."""

from unittest import mock

from click.testing import CliRunner

from common import uri
from mock_test_utility import MockResponse
from tools import url
from tools.commands.provide_access import provide_access
from tools.constants import key_constants as bigquery_constants
from tools.tests.fixtures import *  # pylint: disable=wildcard-import

runner = CliRunner()
TEST_PROVIDE_ACCESS_URL = f"{uri.BASE_URL}/tools/bigqueryAccess:update"


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("tools.url.get_url")
@mock.patch(
    "tools.commands.provide_access.click.prompt"
)
def test_provide_access_command(mock_input: mock.MagicMock,
                                mock_url: mock.MagicMock,
                                mock_client: mock.MagicMock,
                                test_provide_access_data: MockResponse) -> None:
  """Test case to check response for status of command.

  Args:
    mock_input (mock.MagicMock): Mock prompt object
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_provide_access_data (Tuple): Test input data
  """
  mock_url.return_value = TEST_PROVIDE_ACCESS_URL
  mock_input.side_effect = ["test_email_id@testcompany.com"]
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_provide_access_data]
  data = {bigquery_constants.KEY_EMAIL_ID: "test_email_id@testcompany.com"}
  result = runner.invoke(provide_access)
  assert """Providing Bigquery access...

Access provided to email: test_email_id@testcompany.com
""" in result.output
  mock_url.assert_called_once_with("US", "provide_bq_access", "prod")
  mock_client.return_value.request.assert_called_once_with(
      "PATCH",
      TEST_PROVIDE_ACCESS_URL,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS,
      data=data)
  mock_input.assert_called_once_with(
      "Enter email", show_default=False, default="")


@mock.patch(
    "common.chronicle_auth.initialize_http_session"
)
@mock.patch("tools.url.get_url")
@mock.patch(
    "tools.commands.provide_access.click.prompt"
)
def test_provide_access_bigquery_500(mock_input: mock.MagicMock,
                                     mock_url: mock.MagicMock,
                                     mock_client: mock.MagicMock,
                                     test_500_resp: MockResponse) -> None:
  """Test case to check response for provide_access bigquery 500 response code.

  Args:
    mock_input (mock.MagicMock): Mock prompt object
    mock_url (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    test_500_resp (Tuple): Test response data
  """
  mock_input.side_effect = ["test_email_id@testcompany.com"]
  mock_url.return_value = TEST_PROVIDE_ACCESS_URL
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [test_500_resp]
  result = runner.invoke(provide_access)
  assert """Providing Bigquery access...

Error while providing access:
  Response code: 500
  Error: test error
""" in result.output


@mock.patch(
    "tools.commands.provide_access.click.prompt"
)
def test_provide_access_empty_email(mock_input: mock.MagicMock) -> None:
  """Test case to check the console output if no input provided for log type.

  Args:
    mock_input (mock.MagicMock): Mock object
  """
  mock_input.return_value = ""
  result = runner.invoke(provide_access)
  assert """Email not provided. Please enter email.""" in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""
  result = runner.invoke(provide_access)
  assert "Enter email:" in result.output
