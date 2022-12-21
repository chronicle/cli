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
"""Unit tests for list.py."""

import os
from typing import Any, Dict
from unittest import mock

from click.testing import CliRunner

from forwarders.collectors.commands.list import list_command
from forwarders.collectors.tests.fixtures import *  # pylint: disable=wildcard-import
from forwarders.tests.fixtures import TEMP_EXPORT_CSV_FILE
from forwarders.tests.fixtures import TEMP_EXPORT_JSON_FILE
from forwarders.tests.fixtures import TEMP_EXPORT_TXT_FILE

runner = CliRunner()


@mock.patch(
    "forwarders.collectors.commands.list.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.list.click.prompt"
)
def test_list_collectors_200(input_patch: mock.MagicMock,
                             mock_client: mock.MagicMock,
                             list_collector_data: Dict[str, str]) -> None:
  """Test case to check response for 200 response code.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    list_collector_data (Tuple): Test data to fetch list of collectors
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [list_collector_data]
  result = runner.invoke(list_command)
  assert """Collector Details:

ID: abc123-def457-ghi891-234
Display name: SplunkCollector
State: ACTIVE
Config:
  Log type: WINDOWS_DNS
  Max seconds per batch: 10
  Max bytes per batch: '1048576'
  Splunk settings:
    Host: 127.0.0.1
    Minimum window size: 10
    Maximum window size: 30
    Query string: search index=* sourcetype=dns
    Query mode: realtime
    Port: 8089

================================================================================""" in result.output


@mock.patch(
    "forwarders.collectors.commands.list.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.list.click.prompt"
)
def test_list_no_collectors_found(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    list_empty_collector_data: Dict[str, Any]) -> None:
  """Test to check if forwarder id is not provided.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    list_empty_collector_data (Dict): Test data to fetch list of Collectors.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [list_empty_collector_data]
  result = runner.invoke(list_command)
  assert """Collectors:
  Message: No collectors found for this forwarder.""" in result.output


@mock.patch(
    "forwarders.collectors.commands.list.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.list.click.prompt"
)
def test_list_forwarder_id_not_provided(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    list_collector_data: Dict[str, str]) -> None:
  """Test to check if forwarder id is not provided.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    list_collector_data (Tuple): Test data to fetch list of Collectors.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = ""
  mock_client.return_value.request.side_effect = [list_collector_data]
  result = runner.invoke(list_command)
  assert "Forwarder ID not provided. Please enter Forwarder ID." in result.output


@mock.patch(
    "forwarders.commands.list.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.list.click.prompt"
)
def test_list_fetch_collectors_error(
    input_patch: mock.MagicMock,
    mock_client: mock.MagicMock,
    list_error_collectors_data: Dict[str, Any],
) -> None:
  """Test to check error response while fetching list of collectors.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object.
    list_error_collectors_data (Tuple): Test data to fetch list of collectors
      with error response.
  """

  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [list_error_collectors_data]

  result = runner.invoke(list_command)

  assert """Collectors:
  Error:
    Response code: 400
    Message: 'generic::invalid_argument: parent (forwarders/abx-22) does not contain
      a valid UUID: invalid argument'""" in result.output


@mock.patch(
    "forwarders.collectors.commands.list.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.list.click.prompt"
)
def test_list_collector_export_csv(input_patch: mock.MagicMock,
                                   mock_client: mock.MagicMock,
                                   list_collector_data: Dict[str, str]) -> None:
  """Test case to check collector list details exported in csv format.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    list_collector_data (Tuple): Test data to fetch list of Collectors.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [list_collector_data]
  result = runner.invoke(
      list_command,
      ["--export", TEMP_EXPORT_CSV_FILE[:-4], "--file-format", "CSV"])
  assert "Collectors list details exported successfully" in result.output
  assert os.path.exists(TEMP_EXPORT_CSV_FILE)


@mock.patch(
    "forwarders.collectors.commands.list.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.list.click.prompt"
)
def test_list_collector_export_txt(input_patch: mock.MagicMock,
                                   mock_client: mock.MagicMock,
                                   list_collector_data: Dict[str, str]) -> None:
  """Test case to check collector list details exported in txt format.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    list_collector_data (Tuple): Test data to fetch list of Collectors.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [list_collector_data]
  result = runner.invoke(
      list_command,
      ["--export", TEMP_EXPORT_TXT_FILE[:-4], "--file-format", "TXT"])

  assert "Collectors list details exported successfully" in result.output
  assert os.path.exists(TEMP_EXPORT_TXT_FILE)


@mock.patch(
    "forwarders.collectors.commands.list.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.list.click.prompt"
)
def test_list_collector_export_json(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    list_collector_data: Dict[str, str]) -> None:
  """Test case to check collector list details exported in json format.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    list_collector_data (Tuple): Test data to fetch list of Collectors.
  """
  mock_client.return_value = mock.Mock()
  input_patch.return_value = "123"
  mock_client.return_value.request.side_effect = [list_collector_data]
  result = runner.invoke(
      list_command,
      ["--export", TEMP_EXPORT_JSON_FILE[:-5], "--file-format", "JSON"])

  assert "Collectors list details exported successfully" in result.output
  assert os.path.exists(TEMP_EXPORT_JSON_FILE)


@mock.patch(
    "forwarders.collectors.commands.list.chronicle_auth.initialize_http_session"
)
@mock.patch(
    "forwarders.collectors.commands.list.click.prompt"
)
def test_list_collector_verbose_option(
    input_patch: mock.MagicMock, mock_client: mock.MagicMock,
    list_collector_data: Dict[str, str]) -> None:
  """Test case to check response for 200 response code with verbose option.

  Args:
    input_patch (mock.MagicMock): Mock object
    mock_client (mock.MagicMock): Mock object
    list_collector_data (Tuple): Test data to fetch collector.
  """
  mock_client.return_value = mock.Mock()
  input_patch.side_effect = "123"
  mock_client.return_value.request.side_effect = [list_collector_data]

  # Method Call
  result = runner.invoke(list_command, ["--verbose"])
  assert """Collector Details:

ID: abc123-def457-ghi891-234
Display name: SplunkCollector
State: ACTIVE
Config:
  Log type: WINDOWS_DNS
  Max seconds per batch: 10
  Max bytes per batch: '1048576'
  Splunk settings:
    Host: 127.0.0.1
    Minimum window size: 10
    Maximum window size: 30
    Query string: search index=* sourcetype=dns
    Query mode: realtime
    Port: 8089

================================================================================
==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: https://backstory.googleapis.com/v2/forwarders/1/collectors
  Method: GET
  Body: None
Response:
  Body: {'collectors': [{'name': 'forwarders/abc123-def457-ghi891-567/collectors/abc123-def457-ghi891-234', 'displayName': 'SplunkCollector', 'config': {'logType': 'WINDOWS_DNS', 'maxSecondsPerBatch': 10, 'maxBytesPerBatch': '1048576', 'splunkSettings': {'host': '127.0.0.1', 'minimumWindowSize': 10, 'maximumWindowSize': 30, 'queryString': 'search index=* sourcetype=dns', 'queryMode': 'realtime', 'port': 8089}}, 'state': 'ACTIVE'}]}""" in result.output


def test_prompt_text() -> None:
  """Test case to check prompt text."""

  # Method call
  result = runner.invoke(list_command)
  assert "Enter Forwarder ID:" in result.output
