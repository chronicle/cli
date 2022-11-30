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
"""Unit tests for get.py."""

from typing import Dict, Tuple, Any
from unittest import mock

from click.testing import CliRunner

from forwarders.commands.get import get
from forwarders.tests.fixtures import *  # pylint: disable=wildcard-import
from mock_test_utility import MockResponse

runner = CliRunner()


@mock.patch(
    "forwarders.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.get.click.prompt")
def test_forwarder_not_exist(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    get_forwarder_not_exist_data: Tuple[Dict[str, str], str]) -> None:
  """Test case to check if forwarder does not exist.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_forwarder_not_exist_data (Tuple): Test data to fetch forwarder with not
      found status code.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [get_forwarder_not_exist_data]

  # Method Call
  result = runner.invoke(get)
  assert ("Fetching forwarder and its all associated collectors...\nForwarder "
          "does not exist.") in result.output


@mock.patch(
    "forwarders.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.get.click.prompt")
def test_forwarder_id_invalid(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    get_forwarder_id_invalid_data: Tuple[Dict[str, str], str]) -> None:
  """Test case for handling invalid forwarder ID.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_forwarder_id_invalid_data (Tuple): Test data to fetch forwarder with bad
      request status code.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [get_forwarder_id_invalid_data]

  # Method Call
  result = runner.invoke(get)
  assert "Invalid Forwarder ID. Please enter valid Forwarder ID.\n" in result.output


@mock.patch(
    "forwarders.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.get.click.prompt")
def test_get_200(input_patch: mock.MagicMock, mock_client: mock.MagicMock,
                 get_forwarder_data: Dict[str, Any],
                 list_collectors_data: Dict[str, Any]) -> None:
  """Test case to check response for 200 response code.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_forwarder_data (Dict): Test data to fetch forwarder.
    list_collectors_data (Dict): Test data to fetch list of collectors.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      get_forwarder_data, list_collectors_data
  ]

  # Method Call
  result = runner.invoke(get)
  assert """Forwarder Details:

Name: asdf1234-1234-abcd-efgh-12345678abcd
Display name: forwarder 1
State: ACTIVE
Config:
  Upload compression: 'TRUE'
  Metadata:
    Asset namespace: test_namespace
    Labels:
    - key: my_key_1
      value: my_value_1
    - key: my_key_2
      value: my_value_2
  Regex filter:
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: ALLOW
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: BLOCK
  Server setting:
    State: ACTIVE
    Graceful timeout: 234
    Drain timeout: 567
    Http settings:
      Port: 10000
      Host: 10.0.1.3
      Read timeout: 29
      Read header timeout: 34
      Write timeout: 2
      Idle timeout: 34
      Route settings:
        Available status code: 12
        Ready status code: 33
        Unready status code: 43

Collectors:
  Collector [asdf1234-1234-abcd-efgh]:
    Name: asdf1234-1234-abcd-efgh
    Display name: collector pqr
    State: ACTIVE
    Config:
      Log type: Type of logs collected.
      Metadata:
        Asset namespace: test_namespace
        Labels:
        - key: my_key_1
          value: my_value_1
        - key: my_key_2
          value: my_value_2
      Regex filter:
      - description: Describes what is being filtered and why
        regexp: The regular expression used to match against each incoming line
        behavior: ALLOW
      - description: Describes what is being filtered and why
        regexp: The regular expression used to match against each incoming line
        behavior: BLOCK
      Disk buffer:
        State: ACTIVE
        Directory path: Directory path for files written.
        Max file buffer bytes: 3999
      Max seconds per batch: 10
      Max bytes per batch: 1048576
      File settings:
        File path: Path of file to monitor.

================================================================================""" in result.output


@mock.patch(
    "forwarders.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.get.click.prompt")
def test_forwarder_id_absent(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    get_forwarder_data: Tuple[Dict[str, str], str]) -> None:
  """Test case to check for input absent.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_forwarder_data (Tuple): Test data to fetch forwarder.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = ""
  mock_client.return_value.request.side_effect = [get_forwarder_data]

  # Method Call
  result = runner.invoke(get)
  assert "Forwarder ID not provided. Please enter Forwarder ID." in result.output


@mock.patch(
    "forwarders.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.get.click.prompt")
def test_get_404(input_patch: mock.MagicMock,
                 mock_client: mock.MagicMock) -> None:
  """Test case to check for invalid Forwarder ID.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      MockResponse(status_code=404, text="""{}""")
  ]

  # Method Call
  result = runner.invoke(get)
  assert "Forwarder does not exist." in result.output


@mock.patch(
    "forwarders.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.get.click.prompt")
def test_get_server_error_code(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    get_forwarder_server_error_code: Dict[str, Any]) -> None:
  input_patch.return_value = "123"
  mock_client.return_value = mock.Mock()
  mock_client.return_value.request.side_effect = [
      get_forwarder_server_error_code
  ]

  # Method call
  result = runner.invoke(get)
  assert ("Error while fetching forwarder details.\nResponse Code: 500"
         ) in result.output


@mock.patch(
    "forwarders.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.get.click.prompt")
def test_get_credential_file_invalid(input_patch: mock.MagicMock,
                                     mock_client: mock.MagicMock) -> None:
  """Test case for checking invalid credential path.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.side_effect = OSError("Credential Path not found.")
  expected_message = "Failed with exception: Credential Path not found."

  result = runner.invoke(get, ["--credential_file", "my_dummy.json"])
  assert expected_message in result.output


@mock.patch(
    "forwarders.commands.get.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.commands.get.click.prompt")
def test_get_verbose_option(input_patch: mock.MagicMock,
                            mock_client: mock.MagicMock,
                            get_forwarder_data: Tuple[Dict[str, str], str],
                            list_collectors_data: Dict[str, Any]) -> None:
  """Test case to check response for 200 response code with verbose option.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    get_forwarder_data (Tuple): Test data to fetch forwarder.
    list_collectors_data (Tuple): Test data to fetch list of collectors.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [
      get_forwarder_data, list_collectors_data
  ]

  # Method Call
  result = runner.invoke(get, ["--verbose"])
  assert """Forwarder Details:

Name: asdf1234-1234-abcd-efgh-12345678abcd
Display name: forwarder 1
State: ACTIVE
Config:
  Upload compression: 'TRUE'
  Metadata:
    Asset namespace: test_namespace
    Labels:
    - key: my_key_1
      value: my_value_1
    - key: my_key_2
      value: my_value_2
  Regex filter:
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: ALLOW
  - description: Describes what is being filtered and why
    regexp: The regular expression used to match against each incoming line
    behavior: BLOCK
  Server setting:
    State: ACTIVE
    Graceful timeout: 234
    Drain timeout: 567
    Http settings:
      Port: 10000
      Host: 10.0.1.3
      Read timeout: 29
      Read header timeout: 34
      Write timeout: 2
      Idle timeout: 34
      Route settings:
        Available status code: 12
        Ready status code: 33
        Unready status code: 43

Collectors:
  Collector [asdf1234-1234-abcd-efgh]:
    Name: asdf1234-1234-abcd-efgh
    Display name: collector pqr
    State: ACTIVE
    Config:
      Log type: Type of logs collected.
      Metadata:
        Asset namespace: test_namespace
        Labels:
        - key: my_key_1
          value: my_value_1
        - key: my_key_2
          value: my_value_2
      Regex filter:
      - description: Describes what is being filtered and why
        regexp: The regular expression used to match against each incoming line
        behavior: ALLOW
      - description: Describes what is being filtered and why
        regexp: The regular expression used to match against each incoming line
        behavior: BLOCK
      Disk buffer:
        State: ACTIVE
        Directory path: Directory path for files written.
        Max file buffer bytes: 3999
      Max seconds per batch: 10
      Max bytes per batch: 1048576
      File settings:
        File path: Path of file to monitor.""" in result.output
  assert "HTTP Request Details" in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""

  # Method call
  result = runner.invoke(get)
  assert "Enter Forwarder ID:" in result.output
