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
"""Unit tests for feed_schema_utility.py."""

import datetime
import json
from typing import Any, Dict, List, Tuple
from unittest import mock

import pytest

from feeds import feed_schema_utility
from feeds.tests.fixtures import *  # pylint: disable=wildcard-import
from mock_test_utility import MockResponse


def test_get_latest_schema(get_schema_response: List[Any],
                           client: feed_schema_utility.FeedSchema):
  """Test case to check get_latest_schema method.

  Args:
    get_schema_response: Test data.
    client: Patch object of class FeedSchema.
  """
  expected_output = get_schema_response[1]
  client.client.request.return_value = MockResponse(
      status_code=200, text=json.dumps(expected_output))
  assert client.get_latest_schema() == expected_output


def test_get_latest_schema_400(client: feed_schema_utility.FeedSchema):
  """Test case to check handling of error while fetching feed schema.

  Args:
    client: Patch object of class FeedSchema.
  """
  client.client.request.return_value = MockResponse(
      status_code=400, text='{"error": {"message": "400 error"}}')
  with pytest.raises(Exception):
    client.get_latest_schema()


def test_get_detailed_schema_success(client: feed_schema_utility.FeedSchema,
                                     get_detailed_schema_input: Dict[str, str]):
  """Test case for get detailed schema.

  Args:
    client: Patch object of class FeedSchema.
    get_detailed_schema_input (Tuple): Test input data.
  """
  client.current_time = datetime.datetime.now()
  client.schema_response = get_detailed_schema_input
  result = client.get_detailed_schema("DUMMY", "DUMMY_LOGTYPE")
  assert result.display_source_type == "Dummy Source Type"


def test_get_detailed_schema_fail(client: feed_schema_utility.FeedSchema,
                                  get_detailed_schema_input: Dict[str, str]):
  """Test case for failed to get detailed schema.

  Args:
    client: Patch object of class FeedSchema.
    get_detailed_schema_input (Dict): Test input data.
  """
  client.current_time = datetime.datetime.now()
  client.schema_response = get_detailed_schema_input
  result = client.get_detailed_schema("DUMMY1", "DUMMY_LOGTYPE")
  assert result.error == "Schema Not Found."


def test_get_log_source_map(client: feed_schema_utility.FeedSchema,
                            get_detailed_schema_input: Tuple[str, Dict[str,
                                                                       str]]):
  """Test generation of log type and source mapping from feed schema.

  Args:
    client: Patch object of class FeedSchema
    get_detailed_schema_input (Tuple): Test input data
  """
  client.current_time = datetime.datetime.now()
  client.schema_response = get_detailed_schema_input
  result = client.get_log_source_map()
  assert result == {
      "DUMMY": {
          "displayName": "Dummy Source Type",
          "logTypes": [("DUMMY_LOGTYPE", "Dummy LogType")]
      }
  }


@mock.patch(
    "feeds.feed_schema_utility.process_field_input"
)
def test_process_input_detailed_schema(mock_process_field_input: mock.MagicMock,
                                       client: feed_schema_utility.FeedSchema):
  """Test processing of input feed detailed schema.

  Args:
    mock_process_field_input: Mock object
    client: Mock object
  """
  mock_process_field_input.return_value = "value"
  test_data = [{
      "enumFieldSchemas": [{
          "displayName": "test",
          "value": "testvalue"
      }],
      "fieldPath": "api.key",
      "type": "STRING_SECRET"
  }]
  client.process_input_detailed_schema(test_data, {})
  assert client.pre_body == {"api.key": "value"}


@mock.patch("feeds.feed_schema_utility.input")
@mock.patch(
    "feeds.commands.create.click.prompt")
@mock.patch(
    "feeds.feed_schema_utility.process_field_input"
)
def test_prepare_request_body(mock_process_field_input: mock.MagicMock,
                              mock_click_prompt: mock.MagicMock,
                              mock_input: mock.MagicMock,
                              client: feed_schema_utility.FeedSchema,
                              get_detailed_schema: Any):
  """Test generation of request body.

  Args:
    mock_process_field_input: Mock object
    mock_click_prompt: Mock object
    mock_input: Mock object
    client: Mock object
    get_detailed_schema: Test input data
  """
  mock_click_prompt.side_effect = [1, "sample_namespace"]
  mock_process_field_input.side_effect = ["dummy", "dummy", "dummy"]
  mock_input.side_effect = ["k:v", EOFError]
  result = client.prepare_request_body(get_detailed_schema.log_type_schema,
                                       "API", "WORKDAY", {},
                                       "Dummy feed display name")
  # pylint: disable=implicit-str-concat
  expected_output = (
      '{"details": {"httpSettings": {"oauthAccessToken": "dummy"}, '
      '"workdaySettings": {"hostname": "dummy", "tenantId": "dummy"}, '
      '"namespace": "sample_namespace", "labels": [{"key": "k", "value": '
      '"v"}], "feedSourceType": "API", "logType": "WORKDAY"}, "displayName": '
      '"Dummy feed display name"}', {
          "details.http_settings.oauth_access_token": "dummy",
          "details.workday_settings.hostname": "dummy",
          "details.workday_settings.tenant_id": "dummy",
          "details.namespace": "sample_namespace",
          "details.labels": [{
              "key": "k",
              "value": "v"
          }]
      })
  assert result == expected_output


@mock.patch(
    "feeds.commands.create.click.prompt")
def test_process_field_input_other(input_patch: mock.MagicMock):
  """Test generation of prompts for field schema.

  Args:
    input_patch: Mock object for click prompt
  """
  input_patch.return_value = "test"
  test_field_data = {
      "fieldPath": "details.duo_auth_settings.authentication.user",
      "displayName": "Username",
      "description": "Username to authenticate as",
      "type": "OTHER",
      "isRequired": True
  }
  result_value = feed_schema_utility.process_field_input(test_field_data, [])
  assert result_value == "test"


@mock.patch(
    "feeds.commands.create.click.prompt")
def test_process_field_input_enum(input_patch: mock.MagicMock, capfd: Any):
  """Test generation of prompts for ENUM field type.

  Args:
    input_patch: Mock object for click prompt
    capfd: Fixture (Ref:
      https://docs.pytest.org/en/6.2.x/capture.html#accessing-captured-output-from-a-test-function)
  """
  input_patch.return_value = 2
  test_field_data = {
      "fieldPath": "api.region",
      "displayName": "Region",
      "description": "Region",
      "type": "ENUM"
  }
  test_choices = [("us-east-1", "US_EAST_1"), ("asia", "ASIA"),
                  ("europe", "EUROPE")]
  result_value = feed_schema_utility.process_field_input(
      test_field_data, test_choices)
  assert result_value == "ASIA"
  output, _ = capfd.readouterr()
  assert "\nRegion (Region)\nChoose:\n1. us-east-1\n2. asia\n3. europe" in output
  assert "You have selected asia\n" in output


@mock.patch(
    "feeds.commands.create.click.confirm")
def test_process_field_input_bool(confirm_patch: mock.MagicMock):
  """Test generation of prompts for BOOL field type.

  Args:
    confirm_patch: Mock object for click confirm prompt
  """
  confirm_patch.return_value = True
  test_field_data = {
      "displayName": "Bool field",
      "description": "bool",
      "type": "BOOL"
  }
  result_value = feed_schema_utility.process_field_input(test_field_data, [])
  assert result_value


@mock.patch(
    "feeds.commands.create.click.prompt")
def test_process_field_input_str_list(input_patch: mock.MagicMock):
  """Test generation of prompts for STRING_LIST field type.

  Args:
    input_patch: Mock object for click prompt
  """
  input_patch.return_value = "a,b"
  test_field_data = {
      "displayName": "Test field",
      "description": "str list",
      "type": "STRING_LIST"
  }
  result_value = feed_schema_utility.process_field_input(test_field_data, [])
  assert result_value == ["a", "b"]


@mock.patch(
    "feeds.commands.create.click.prompt")
def test_process_field_input_str_secret(input_patch: mock.MagicMock):
  """Test generation of prompts for STRING_SECRET field type.

  Args:
    input_patch: Mock object for click prompt
  """
  input_patch.return_value = "test secret"
  test_field_data = {
      "displayName": "Test secret field",
      "description": "str secret",
      "type": "STRING_SECRET"
  }
  result_value = feed_schema_utility.process_field_input(test_field_data, [])
  assert result_value == "test secret"


@mock.patch("feeds.feed_schema_utility.input")
def test_process_field_input_kv_list(input_patch: mock.MagicMock):
  """Test generation of prompts for KEY_VALUE_LIST field type.

  Args:
    input_patch: Mock object for click prompt
  """
  input_patch.side_effect = ["k:v", EOFError]
  test_field_data = {
      "displayName": "KEY_VALUE_LIST field",
      "description": "KEY_VALUE_LIST",
      "type": "KEY_VALUE_LIST"
  }
  result_value = feed_schema_utility.process_field_input(test_field_data, [])
  assert result_value == [{"key": "k", "value": "v"}]


@mock.patch("feeds.feed_schema_utility.input")
def test_process_field_input_map_str(input_patch: mock.MagicMock):
  """Test generation of prompts for MAP_STRING_STRING field type.

  Args:
    input_patch: Mock object for click prompt
  """
  input_patch.side_effect = ["k:v", EOFError]
  test_field_data = {
      "displayName": "MAP_STRING_STRING field",
      "description": "MAP_STRING_STRING",
      "type": "MAP_STRING_STRING"
  }
  result_value = feed_schema_utility.process_field_input(test_field_data, [])
  assert result_value == {"k": "v"}


@mock.patch(
    "feeds.feed_schema_utility.getpass.getpass"
)
def test_process_field_input_str_multiline(input_patch: mock.MagicMock):
  """Test generation of prompts for STRING_MULTILINE_SECRET field type.

  Args:
    input_patch: Mock object for click prompt
  """
  input_patch.side_effect = ["k:v", EOFError]
  test_field_data = {
      "displayName": "STRING_MULTILINE_SECRET field",
      "description": "STRING_MULTILINE_SECRET",
      "type": "STRING_MULTILINE_SECRET"
  }
  result_value = feed_schema_utility.process_field_input(test_field_data, [])
  assert result_value == "k:v"


@mock.patch(
    "feeds.feed_schema_utility.click.prompt")
def test_process_namespace_input(mock_input: mock.MagicMock,
                                 client: feed_schema_utility.FeedSchema):
  """Test processing of input namespace.

  Args:
    mock_input: Mock object
    client: Mock object
  """
  mock_input.return_value = "sample_namespace"
  client.process_namespace_input({})
  assert client.pre_body == {"details.namespace": "sample_namespace"}


@mock.patch("feeds.feed_schema_utility.input")
def test_process_labels_input(input_patch: mock.MagicMock,
                              client: feed_schema_utility.FeedSchema):
  """Test processing of input labels.

  Args:
    input_patch: Mock object for click prompt
    client: Mock object
  """
  input_patch.side_effect = ["k:v", EOFError]
  client.process_labels_input({})
  assert client.pre_body == {"details.labels": [{"key": "k", "value": "v"}]}
