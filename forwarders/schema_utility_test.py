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
"""Unit tests for schema_utility.py."""

from typing import Any, Dict, List
from unittest import mock

import pytest

from forwarders import schema_utility
from forwarders.constants import schema
from forwarders.tests.fixtures import *  # pylint: disable=wildcard-import


@mock.patch(
    "forwarders.schema_utility.click.prompt")
@pytest.mark.parametrize("field_type, input_data", [
    ("STRING", "test"),
    ("INT", 15),
    ("STRING_SECRET", "test secret"),
])
def test_process_field_input_string(input_patch: mock.MagicMock,
                                    field_type: str, input_data: Any):
  """Test generation of prompts for string type input field schema.

  Args:
    input_patch (mock.MagicMock): Mock object for click prompt.
    field_type (str): Type of field for input.
    input_data (Any): Input prompt data.
  """
  input_patch.return_value = input_data
  test_field_schema = {
      "fieldPath": "display_name",
      "displayName": "Display Name",
      "description": "User specified display name",
      "type": field_type
  }
  result_value = schema_utility.process_field_input(test_field_schema)
  assert result_value == input_data


@mock.patch(
    "forwarders.schema_utility.click.confirm")
def test_process_field_input_bool(confirm_patch: mock.MagicMock,
                                  bool_field_schema: Dict[str, Any]):
  """Test generation of prompts for boolean type input field schema.

  Args:
    confirm_patch (mock.MagicMock): Mock object for click confirm prompt.
    bool_field_schema (Dict): BOOL type field schema.
  """
  confirm_patch.return_value = True
  result_value = schema_utility.process_field_input(bool_field_schema)
  assert result_value


@mock.patch(
    "forwarders.schema_utility.click.prompt")
def test_process_field_input_enum(input_patch: mock.MagicMock, capfd: Any,
                                  enum_field_schema: Dict[str, Any]):
  """Test generation of prompts for enum input field schema.

  Args:
    input_patch (mock.MagickMock): Mock object for click prompt
    capfd: (Fixture) used to capture the stdout created during test execution.
    enum_field_schema (Dict): ENUM type field schema.
  """
  input_patch.return_value = 1
  result_value = schema_utility.process_field_input(enum_field_schema)
  output, _ = capfd.readouterr()
  assert result_value == "ALLOW"
  assert ("\nFilter Behavior (Filter behavior to apply when a match is "
          "found)\nChoose:\n1. allow\n2. block") in output


@mock.patch("forwarders.schema_utility.input")
def test_process_labels_input(input_patch: mock.MagicMock, capfd: Any):
  """Test generation of prompts for label type field schema.

  Args:
    input_patch: Mock object for click prompt
    capfd: (Fixture) used to capture the stdout created during test execution.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  input_patch.side_effect = ["sample:dummy", EOFError]
  result = schema_object.process_labels_input([{
      "key": "existing_key",
      "value": "existing_value"
  }])
  output, _ = capfd.readouterr()
  assert result == [{"key": "sample", "value": "dummy"}]
  assert """\nLabels (The ingestion metadata labels in 'key:value' format to apply to all logs ingested through this forwarder, as well as the resulting normalized data.)
Enter/Paste your content. On a new line, press Ctrl-D (Linux) / [Ctrl-Z + Enter (Windows)] to save it:
[{'existing_key': 'existing_value'}]
""" == output


@mock.patch("forwarders.schema_utility.input")
def test_process_labels_input_existing_value(input_patch: mock.MagicMock,
                                             capfd: Any):
  """Test generation of prompts for label type field schema.

  Args:
    input_patch: Mock object for click prompt
    capfd: (Fixture) used to capture the stdout created during test execution.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  input_patch.side_effect = [EOFError]
  result = schema_object.process_labels_input()
  output, _ = capfd.readouterr()
  assert isinstance(result, list)
  assert ("\nLabels (The ingestion metadata labels in 'key:value' format"
          " to apply to all logs ingested through this forwarder, "
          "as well as the resulting normalized data.)\n"
          "Enter/Paste your content. On a new line, press Ctrl-D (Linux)"
          " / [Ctrl-Z + Enter (Windows)] to save it:") in output


@mock.patch(
    "forwarders.schema_utility.click.prompt")
def test_prepare_request_body_forwarder(input_patch: mock.MagicMock,
                                        get_forwarder_schema: Dict[str, Any]):
  """Test generation of prompts for prepare request body for forwarders.

  Args:
    input_patch: Mock object for click prompt
    get_forwarder_schema: To get The forwarder schema data for prepare body.
  """
  schema_object = schema_utility.Schema(schema.KEY_FORWARDER_SCHEMA, {})
  input_patch.return_value = "test"
  schema_object.schema = get_forwarder_schema
  result = schema_object.prepare_request_body()

  assert result == {"display_name": "test"}


@mock.patch(
    "forwarders.schema_utility.click.prompt")
def test_prepare_request_body_collector(input_patch: mock.MagicMock,
                                        get_collector_schema: Dict[str, Any]):
  """Test generation of prompts for prepare request body for collectors.

  Args:
    input_patch: Mock object for click prompt
    get_collector_schema: (fixture) To get The collector schema data for prepare
      body.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  input_patch.return_value = "test"
  schema_object.schema = get_collector_schema
  result = schema_object.prepare_request_body()

  assert result == {"displayName": "test"}


@mock.patch(
    "forwarders.schema_utility.Schema.process_labels_input"
)
def test_process_input_detailed_schema_label(
    process_labels_input: mock.MagicMock, capfd: Any,
    label_field_schema: List[Dict[str, Any]]):
  """Test generation of adding the label type schema value in pre_body.

  Args:
    process_labels_input: Mock the method of Schema schema_object.
    capfd: (Fixture) used to capture the stdout created during test execution.
    label_field_schema: LABEL type field schema.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  process_labels_input.return_value = [{"key": "sample", "value": "abc"}]
  req_body = {}
  schema_object.process_input_detailed_schema(label_field_schema, req_body,
                                              None)
  output, _ = capfd.readouterr()
  assert """========================================
=========== Forwarder Labels ===========
========================================""" in output
  assert req_body == {"labels": [{"key": "sample", "value": "abc"}]}


@mock.patch(
    "forwarders.schema_utility.click.prompt")
@mock.patch(
    "forwarders.schema_utility.click.confirm")
def test_process_input_detailed_schema_non_primitive(
    confirm_patch: mock.MagicMock, input_patch: mock.MagicMock,
    non_primitive_schema: List[Dict[str, Any]], capfd: Any):
  """Test case to process input detailed schema for non primitive type.

  Args:
    confirm_patch: Mock object for click confirm.
    input_patch: Mock object for click prompt.
    non_primitive_schema: (fixture) To get The other type's field schema.
    capfd: (Fixture) used to capture the stdout created during test execution.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  confirm_patch.side_effect = [False, True, True]
  input_patch.side_effect = [".*", True]
  req_body = {}
  schema_object.process_input_detailed_schema(non_primitive_schema, req_body,
                                              None)
  output, _ = capfd.readouterr()
  assert req_body == {
      "config": {
          "upload_compression": True
      },
      "regex_filters": {
          "description": ".*"
      }
  }
  assert """========================================
======= Collector Regex Filters =======
========================================

========================================
======= Forwarder Configuration ========
========================================""" in output


@mock.patch(
    "forwarders.schema_utility.click.prompt")
def test_process_oneof_input(input_patch: mock.MagicMock,
                             oneof_field_schema: List[Dict[str,
                                                           Any]], capfd: Any):
  """Test generation of prompts for ONEOF field type.

  Args:
    input_patch: Mock object for click prompt
    oneof_field_schema: (Fixture) To get The oneof field schema.
    capfd: (Fixture) used to capture the stdout created during test execution.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  input_patch.side_effect = [1, "", "path/to/file.txt"]
  req_body = {}
  schema_object.process_input_detailed_schema(oneof_field_schema, req_body,
                                              None)
  output, _ = capfd.readouterr()
  assert req_body == {"file_settings": {"file_path": "path/to/file.txt"}}

  assert """========================================
===== Configure Ingestion Settings =====
========================================

Choose:
1. File Settings
2. Kafka Settings
3. Pcap Settings
4. Splunk Settings
5. Syslog Settings

You haven't given any information regarding ingestion settings.
Please set one of the settings to continue.
""" in output


@mock.patch(
    "forwarders.schema_utility.click.prompt")
def test_process_oneof_input_backup(input_patch: mock.MagicMock,
                                    oneof_field_schema: List[Dict[str, Any]]):
  """Test generation of prompts for ONEOF field type with backup request body.

  Args:
    input_patch: Mock object for click prompt
    oneof_field_schema: (Fixture) To get The oneof field schema.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  input_patch.side_effect = [1, "", "path/to/file.txt"]
  req_body = {}
  backup_request_body = {"file_settings": {"file_path": "sample"}}
  schema_object.process_input_detailed_schema(oneof_field_schema, req_body,
                                              backup_request_body)
  assert req_body == {"file_settings": {"file_path": "path/to/file.txt"}}


def test_validate_oneof_input_true(oneof_validate_data: Any):
  """Test case to whether oneof type field is set or not.

  Args:
    oneof_validate_data: (Fixture) Oneof type field schema.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  request_body = {"file_path": "c:/user/jay"}
  result = schema_object.validate_oneof_input(oneof_validate_data, request_body)

  assert result


def test_validate_oneof_input_false(oneof_validate_data: Any):
  """Test generation of prompts for prepare request body for forwarders.

  Args:
    oneof_validate_data: (Fixture) To get The oneof field schema for validation.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  result = schema_object.validate_oneof_input(oneof_validate_data, {})

  assert not result


@mock.patch("forwarders.schema_utility.input")
def test_process_labels_input_backup(input_patch: mock.MagicMock):
  """Test generation of prompts for label type field schema.

  Args:
    input_patch: Mock object for click prompt.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  input_patch.side_effect = [EOFError]
  result = schema_object.process_labels_input([{
      "key": "sample",
      "value": "abc"
  }])

  assert result == [{"key": "sample", "value": "abc"}]


@mock.patch(
    "forwarders.schema_utility.click.prompt")
def test_process_input_detailed_schema_repeated_string(
    input_patch: Any, repeated_field_schema: List[Dict[str, Any]]):
  """Test generation of prompts for repeated type field schema.

  Args:
    input_patch: Mock object for click prompt.
    repeated_field_schema: (Fixture) REPEATED_STRING type field schema.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  input_patch.return_value = "test1, test2,test3"
  req_body = {}
  schema_object.process_input_detailed_schema(repeated_field_schema, req_body,
                                              None)
  assert req_body == {"brokers": ["test1", "test2", "test3"]}


@mock.patch(
    "forwarders.schema_utility.click.prompt")
def test_process_input_detailed_schema_string(
    input_patch: Any, str_field_schema: List[Dict[str, Any]]):
  """Test generation of prompts for string type field schema.

  Args:
    input_patch: Mock object for click prompt.
    str_field_schema: (Fixture) STRING type field schema.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  input_patch.return_value = "sample"
  req_body = {}
  schema_object.process_input_detailed_schema(str_field_schema, req_body, None)
  assert req_body == {"display_name": "sample"}


@mock.patch(
    "forwarders.schema_utility.click.prompt")
def test_process_input_detailed_schema_string_empty_value(
    input_patch: Any, str_field_schema: List[Dict[str, Any]]):
  """Test generation of prompts for string type field schema with empty string.

  Args:
    input_patch: Mock object for click prompt
    str_field_schema: (Fixture) STRING type field schema
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  input_patch.return_value = ""
  req_body = {}
  schema_object.process_input_detailed_schema(str_field_schema, req_body, None)
  assert not bool(req_body)


@mock.patch(
    "forwarders.schema_utility.click.prompt")
@mock.patch(
    "forwarders.schema_utility.click.confirm")
def test_process_input_detailed_schema_repeated_message_fields(
    confirm_patch: mock.MagicMock, input_patch: Any,
    repeated_message_fields_schema: List[Dict[str, Any]]):
  """Test all repeated fields of schema are stored in repeated_message_fields attribute.

  Args:
    confirm_patch: Mock object for click confirm.
    input_patch: Mock object for click prompt.
    repeated_message_fields_schema: (Fixture) Repeated fields type schema.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  confirm_patch.side_effect = [True, False]
  input_patch.side_effect = [2, "sample"]
  req_body = {}
  key = "config"
  expected_output = ["config.kafka_settings.regex_filters"]

  schema_object.process_input_detailed_schema(repeated_message_fields_schema,
                                              req_body, None, key)
  assert req_body == {
      "kafka_settings": {
          "regex_filters": [{
              "description": "sample"
          }]
      }
  }
  assert list(schema_object.repeated_message_fields) == expected_output


def test_validate_syslog_udp_settings():
  """Test to validate syslog settings for UDP protocol to process field schema.
  """
  schema_object = schema_utility.Schema(schema.KEY_COLLECTOR_SCHEMA, {})
  request_body = {"protocol": "UDP"}
  field_schema = {
      "fieldPath": "connection_timeout",
      "displayName": "Connection Timeout",
      "type": "INT"
  }
  assert schema_object.validate_syslog_udp_settings(field_schema, request_body)
