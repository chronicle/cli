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
"""Fixtures for parsers commands."""

import os
from typing import Any

import pytest

from mock_test_utility import MockResponse

TEST_DATA_DIR = os.path.dirname(__file__)
TEMP_CONF_FILE = os.path.join(TEST_DATA_DIR,
                              "test_log_type_20220824062200.conf")
TEMP_SUBMIT_CONF_FILE = os.path.join(TEST_DATA_DIR, "test_config_file.conf")
TEMP_SUBMIT_LOG_FILE = os.path.join(TEST_DATA_DIR, "test_log_file.conf")
TEMP_TEST_JSON_FILE = os.path.join(TEST_DATA_DIR, "test.json")
TEMP_TEST_TXT_FILE = os.path.join(TEST_DATA_DIR, "test.txt")

os.system(f"chmod -R +rw {TEST_DATA_DIR}")


def create_temp_config_file(file_path: str, content: str) -> None:
  """Create temporary config file with the content.

  Args:
    file_path (str): Path to create the temp config file.
    content (str): content to be written in the file.
  """
  with open(file_path, "w") as file:
    if content:
      file.write(content)


def create_temp_log_file(file_path: str, content: str) -> None:
  """Create temporary log file with the content.

  Args:
    file_path (str): Path to create the temp config file.
    content (str): content to be written in the file.
  """
  with open(file_path, "w") as file:
    if content:
      file.write(content)


@pytest.fixture()
def test_data_list_command() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=200,
      text="""{"cbnParsers": [{"configId": "test_config_id",
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}]}""")


@pytest.fixture()
def test_data_list_cmd_missing_key() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=200,
      text="""{"cbnParsers": [{"configId": "config 1",
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}, {
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}, {"configId": "config 2",
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}]}""")


@pytest.fixture()
def test_500_resp() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=500,
      text="""{"error": {"code": 500, "message": "test error"}}""")


@pytest.fixture()
def test_run_validation_data() -> MockResponse:
  """Test validation data."""
  return MockResponse(
      status_code=200, text="""{"result": ["result 1", "result 2"]}""")


@pytest.fixture()
def test_run_validation_error_data() -> MockResponse:
  """Test validation data."""
  return MockResponse(
      status_code=200,
      text="""{"errors": [{"errorMsg": "test error", "logEntry": "sample log"}]}"""
  )


@pytest.fixture()
def test_history_data() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=200,
      text="""{"cbnParsers": [{"configId": "test_config_id",
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config",
              "validationErrors": {"errors": [{"error": "test error 1",
              "log": "dGVzdCBsb2cgMQ=="}, {"error": "test error 2"}]}}]}""")


@pytest.fixture()
def test_archive_data() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=200,
      text="""{"configId": "test_config_id",
              "author": "test_user", "state": "ARCHIVED", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}""")


@pytest.fixture()
def test_data_classify_log_type() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=200,
      text="""{"predictions": [
          { "logType": "LOG_TYPE_1", "score": 0.998 },
          { "logType": "LOG_TYPE_2", "score": 0.001 },
          { "logType": "LOG_TYPE_3", "score": 0.001 }]}""")


@pytest.fixture()
def error_list() -> MockResponse:
  """Test input data."""
  data = MockResponse(
      status_code=200,
      text="""{"errors": [{
      "errorId": "test_error_id",
      "configId": "test_config_id",
      "logType": "test_log_type",
      "errorTime": "2022-08-18T12:28:57.443376813Z",
      "category": "test_category",
      "errorMsg": "test_error_message",
      "logs": [
        "dGVzdF9sb2dz"
      ]
    }]}""")
  return data


@pytest.fixture()
def submit_parser() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=200,
      text="""{"configId": "test_config_id", "logType": "TEST_LOG_TYPE",
              "submitTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "state": "LIVE", "sha256": "test_sha256", "config": "test_config", 
              "author": "test_user"}""")


@pytest.fixture(scope="function", autouse=True)
def cleanup(request: Any):
  """Cleanup testing files once we are finished."""

  def remove_test_files():
    files = [
        TEMP_TEST_TXT_FILE, TEMP_TEST_JSON_FILE, TEMP_CONF_FILE,
        TEMP_SUBMIT_CONF_FILE, TEMP_SUBMIT_LOG_FILE,
    ]
    for file_path in files:
      try:
        os.remove(file_path)
      except FileNotFoundError:
        pass

  request.addfinalizer(remove_test_files)


@pytest.fixture()
def status_parser() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=200,
      text="""{"configId": "test_config_id",
              "author": "test_user", "state": "LIVE", "sha256": "test_sha256",
              "logType": "TEST_LOG_TYPE", "submitTime": "2022-04-01T08:08:44.217797Z",
              "lastLiveTime": "2022-04-01T08:08:44.217797Z",
              "stateLastChangedTime": "2022-04-01T08:08:44.217797Z",
              "config": "test_config"}""")


@pytest.fixture()
def test_400_resp_status_command() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=400,
      text="""{"error": {"code": 400, "message": "Invalid ID."}}""")


@pytest.fixture()
def test_500_resp_status_command() -> MockResponse:
  """Test response data."""
  return MockResponse(
      status_code=500,
      text="""{"error": {"code": 500, "message": "could not get CBN parser."}}"""
  )


@pytest.fixture()
def generate_logs() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=200,
      text="""{"data": ["MDAsMDcvMTQvMjEsMTE6Mjk6MTcsU3RhcnRlZCwsLCwsMCw2LCwsLCwsLCwsMA=="]}"""
  )


@pytest.fixture()
def test_v2flag_not_provided() -> MockResponse:
  """Test input data for v2 flag not provided."""
  return MockResponse(
      status_code=200,
      text="--v2 flag not provided. "
      "Please provide the flag to run the new commands"
  )


@pytest.fixture()
def test_empty_project_id() -> MockResponse:
  """Test input data for empty Project ID."""
  return MockResponse(
      status_code=200,
      text="Project ID not provided. Please enter Porject ID")


@pytest.fixture()
def test_empty_customer_id() -> MockResponse:
  """Test input data for empty Customer ID."""
  return MockResponse(
      status_code=200,
      text="Customer ID not provided. Please enter Customer ID")


@pytest.fixture()
def test_empty_log_type() -> MockResponse:
  """Test input data for empty Log type."""
  return MockResponse(
      status_code=200,
      text="Log Type not provided. Please enter Log Type")


@pytest.fixture()
def test_empty_parser_id() -> MockResponse:
  """Test input data for empty Parser ID."""
  return MockResponse(
      status_code=200,
      text="Parser ID not provided. Please enter Parser ID")


@pytest.fixture()
def test_empty_parser_id_and_parserextension_id() -> MockResponse:
  """Test input data for empty Parser and ParserExtension ID."""
  return MockResponse(
      status_code=200,
      text="Parser ID or ParserExtension ID not provided. "
      "Please enter Parser or ParserExtension ID")


@pytest.fixture()
def test_empty_parserextension_id() -> MockResponse:
  """Test input data for empty ParserExtension ID."""
  return MockResponse(
      status_code=200,
      text="ParserExtension ID not provided. Please enter ParserExtension ID")


@pytest.fixture()
def test_empty_valdiation_report_id() -> MockResponse:
  """Test input data for empty ValidationReport ID."""
  return MockResponse(
      status_code=200,
      text="Validation Report ID not provided. "
      "Please enter Validation Report ID")


@pytest.fixture()
def test_non_empty_parser_id_and_parserextension_id() -> MockResponse:
  """Test input data for non empty Parser and ParserExtension ID."""
  return MockResponse(
      status_code=200,
      text="Parser ID and ParserExtension ID provided. "
      "Please enter Parser or ParserExtension ID")


@pytest.fixture()
def test_data_activate_parser() -> MockResponse:
  """Test input data for activate parser."""
  return MockResponse(
      status_code=200,
      text="""{}""")


@pytest.fixture()
def test_data_deactivate_parser() -> MockResponse:
  """Test input data for deactivate parser."""
  return MockResponse(
      status_code=200,
      text="""{}""")


@pytest.fixture()
def test_data_delete_parser() -> MockResponse:
  """Test input data for delete parser."""
  return MockResponse(
      status_code=200,
      text="""{}""")


@pytest.fixture()
def test_data_delete_extension() -> MockResponse:
  """Test input data for delete extension."""
  return MockResponse(
      status_code=200,
      text="""{}""")


@pytest.fixture()
def test_data_get_extension() -> MockResponse:
  """Test input data for get parserextension."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "cbnSnippet": "test_cbn_snippet",
          "createTime": "2023-01-01T00:00:00.000000Z",
          "extensionValidationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id",
          "log": "test_log",
          "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id",
          "state": "LIVE",
          "stateLastChangedTime": "2023-01-01T00:00:00.000000Z",
          "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id/validationReports/test_validation_report_id"
      }
      """)


@pytest.fixture()
def test_data_get_extension_missing_key() -> MockResponse:
  """Test input data for missing key in get parserextension."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "cbnSnippet": "test_cbn_snippet",
          "createTime": "2023-01-01T00:00:00.000000Z",
          "extensionValidationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id2",
          "log": "test_log",
          "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id2",
          "stateLastChangedTime": "2023-01-01T00:00:00.000000Z",
          "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id2/validationReports/test_validation_report_id"
      }
      """)


@pytest.fixture()
def test_data_get_parser() -> MockResponse:
  """Test input data for get parser."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "cbn": "test_cbn",
          "changelogs": {},
          "createTime": "2023-01-01T00:00:00.000000Z",
          "creator": {
              "customer": "projects/test_project/locations/us/instances/test_instance",
              "author": "test_author",
              "source": "CUSTOMER"
          },
          "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id",
          "releaseStage": "RELEASE",
          "state": "ACTIVE",
          "type": "CUSTOM",
          "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id/validationReports/test_validation_report_id",
          "validationStage": "PASSED"
      }
      """)


@pytest.fixture()
def test_data_get_parser_missing_key() -> MockResponse:
  """Test input data for missing key in get parser."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "cbn": "test_cbn",
          "changelogs": {},
          "createTime": "2023-01-01T00:00:00.000000Z",
          "creator": {
              "customer": "projects/test_project/locations/us/instances/test_instance",
              "author": "test_author",
              "source": "CUSTOMER"
          },
          "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id",
          "releaseStage": "RELEASE",
          "type": "CUSTOM",
          "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id/validationReports/test_validation_report_id",
          "validationStage": "PASSED"
      }
      """)


@pytest.fixture()
def test_data_get_validation_report_for_parser() -> MockResponse:
  """Test input data for validation report."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id/validationReports/test_validation_report_id",
          "stats": {
              "logEntryCount": "1",
              "successfullyNormalizedLogCount": "1",
              "onErrorCount": "1",
              "eventCount": "1",
              "genericEventCount": "1",
              "eventCategoryCounts": {
                  "valid_event": "1"
              },
              "dropTagCounts": {
                  "TAG_UNSUPPORTED": "0"
              },
              "maxParseDuration": "1s",
              "avgParseDuration": "1s",
              "normalizationPercentage": "100",
              "genericEventPercentage": "100"
          },
          "verdict": "PASS"
      }
      """)


@pytest.fixture()
def test_data_get_validation_report_for_parserextension() -> MockResponse:
  """Test input data for validation report."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id/validationReports/test_validation_report_id",
          "stats": {
              "logEntryCount": "1",
              "successfullyNormalizedLogCount": "1",
              "onErrorCount": "1",
              "eventCount": "1",
              "genericEventCount": "1",
              "eventCategoryCounts": {
                  "valid_event": "1"
              },
              "dropTagCounts": {
                  "TAG_UNSUPPORTED": "0"
              },
              "maxParseDuration": "1s",
              "avgParseDuration": "1s",
              "normalizationPercentage": "100",
              "genericEventPercentage": "100"
          },
          "verdict": "PASS"
      }
      """)


@pytest.fixture()
def test_data_get_validation_report_missing_key() -> MockResponse:
  """Test input data for missing key in validation report."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id/validationReports/test_validation_report_id"
      }
      """)


@pytest.fixture()
def test_data_list_extensions() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "parserExtensions": [
              {
                  "cbnSnippet": "test_cbn_snippet",
                  "createTime": "2023-01-01T00:00:00.000000Z",
                  "extensionValidationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id",
                  "log": "test_log",
                  "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id",
                  "state": "LIVE",
                  "stateLastChangedTime": "2023-01-01T00:00:00.000000Z",
                  "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id/validationReports/test_validation_report_id"
              }
          ]
      }
      """)


@pytest.fixture()
def test_data_list_extensions_missing_key() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "parserExtensions": [
              {
                  "cbnSnippet": "test_cbn_snippet",
                  "createTime": "2023-01-01T00:00:00.000000Z",
                  "extensionValidationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id1",
                  "log": "test_log",
                  "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id1",
                  "state": "LIVE",
                  "stateLastChangedTime": "2023-01-01T00:00:00.000000Z",
                  "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id1/validationReports/test_validation_report_id1"
              },
              {
                  "cbnSnippet": "test_cbn_snippet",
                  "createTime": "2023-01-01T00:00:00.000000Z",
                  "extensionValidationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id2",
                  "log": "test_log",
                  "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id2",
                  "stateLastChangedTime": "2023-01-01T00:00:00.000000Z",
                  "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id2/validationReports/test_validation_report_id2"
              },
              {
                  "cbnSnippet": "test_cbn_snippet",
                  "createTime": "2023-01-01T00:00:00.000000Z",
                  "extensionValidationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id3",
                  "log": "test_log",
                  "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id3",
                  "state": "REJECTED",
                  "stateLastChangedTime": "2023-01-01T00:00:00.000000Z",
                  "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id3/validationReports/test_validation_report_id3"
              }
          ]
      }
      """)


@pytest.fixture()
def test_data_list_parsers() -> MockResponse:
  """Test input data for list parsers."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "parsers": [
              {
                  "cbn": "test_cbn",
                  "changelogs": {},
                  "createTime": "2023-01-01T00:00:00.000000Z",
                  "creator": {
                      "customer": "projects/test_project/locations/us/instances/test_instance",
                      "author": "test_author",
                      "source": "CUSTOMER"
                  },
                  "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id",
                  "releaseStage": "RELEASE",
                  "state": "ACTIVE",
                  "type": "CUSTOM",
                  "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id/validationReports/test_validation_report_id",
                  "validationStage": "PASSED"
              }
          ]
      }
      """)


@pytest.fixture()
def test_data_list_parsing_errors_for_parser() -> MockResponse:
  """Test input data for list parsers."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "parsingErrors": [
              {
                  "logData": "test_log",
                  "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id/validationReports/test_validation_report_id",
                  "error": "test_error"
              }
          ]
      }
      """)


@pytest.fixture()
def test_data_list_parsing_errors_for_parserextension() -> MockResponse:
  """Test input data for list parsers."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "parsingErrors": [
              {
                  "logData": "test_log",
                  "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id/validationReports/test_validation_report_id",
                  "error": "test_error"
              }
          ]
      }
      """)


@pytest.fixture()
def test_data_list_parsers_missing_key() -> MockResponse:
  """Test input data for list parsers."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "parsers": [
              {
                  "cbn": "test_cbn",
                  "changelogs": {},
                  "createTime": "2023-01-01T00:00:00.000000Z",
                  "creator": {
                      "customer": "projects/test_project/locations/us/instances/test_instance",
                      "author": "test_author1",
                      "source": "CUSTOMER"
                  },
                  "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type1/parsers/test_parser_id1",
                  "state": "ACTIVE",
                  "type": "CUSTOM",
                  "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type1/parsers/test_parser_id1/validationReports/test_validation_report_id1",
                  "validationStage": "PASSED"
              },
              {
                  "cbn": "test_cbn",
                  "changelogs": {},
                  "creator": {
                      "customer": "projects/test_project/locations/us/instances/test_instance",
                      "author": "test_author2",
                      "source": "CUSTOMER"
                  },
                  "createTime": "2023-01-01T00:00:00.000000Z",
                  "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type2/parsers/test_parser_id2",
                  "type": "CUSTOM",
                  "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type2/parsers/test_parser_id2/validationReports/test_validation_report_id2",
                  "validationStage": "PASSED"
              },
              {
                  "cbn": "test_cbn",
                  "changelogs": {},
                  "createTime": "2023-01-01T00:00:00.000000Z",
                  "creator": {
                      "customer": "projects/test_project/locations/us/instances/test_instance",
                      "author": "test_author3",
                      "source": "CUSTOMER"
                  },
                  "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type3/parsers/test_parser_id3",
                  "state": "INACTIVE",
                  "type": "CUSTOM",
                  "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type3/parsers/test_parser_id3/validationReports/test_validation_report_id3",
                  "validationStage": "FAILED"
              }
          ]
      }
      """)


@pytest.fixture()
def test_data_non_existing_config_file() -> MockResponse:
  """Test input data for non existing config file."""
  return MockResponse(
      status_code=200,
      text="test_config_file does not exist. "
      "Please enter valid config file path")


@pytest.fixture()
def test_data_non_existing_log_file() -> MockResponse:
  """Test input data."""
  return MockResponse(
      status_code=200,
      text="test_log_file does not exist. "
      "Please enter valid log file path")


@pytest.fixture()
def test_data_run_parser() -> MockResponse:
  """Test input data for run parser."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "runParserResults": [
              {
                  "log": "dGVzdF9sb2c=",
                  "parsedEvents": "result"
              },
              {
                  "error": {
                      "message": "error: test_error_message"
                  }
              }
          ]
      }
      """)


@pytest.fixture()
def test_data_submit_extension() -> MockResponse:
  """Test input data for submit extension."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "cbnSnippet": "test_cbn_snippet",
          "createTime": "2023-01-01T00:00:00.000000Z",
          "extensionValidationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id",
          "log": "test_log",
          "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id",
          "state": "LIVE",
          "stateLastChangedTime": "2023-01-01T00:00:00.000000Z",
          "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id/validationReports/test_validation_report_id"
      }
      """)


@pytest.fixture()
def test_data_submit_parser() -> MockResponse:
  """Test input data for submit parser."""
  return MockResponse(
      status_code=200,
      text="""
      {
          "cbn": "test_cbn",
          "changelogs": {},
          "createTime": "2023-01-01T00:00:00.000000Z",
          "creator": {
              "customer": "projects/test_project/locations/us/instances/test_instance",
              "author": "test_author",
              "source": "CUSTOMER"
          },
          "name": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id",
          "releaseStage": "RELEASE",
          "state": "INACTIVE",
          "type": "CUSTOM",
          "validationReport": "projects/test_project/locations/us/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id/validationReports/test_validation_report_id",
          "validationStage": "NEW"
      }
      """)
