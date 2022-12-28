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
"""Define fixtures."""

import json
import os
from typing import Any, Dict, List

import pytest

from mock_test_utility import MockResponse

TEST_DATA_DIR = os.path.dirname(__file__)
TEMP_EXPORT_TXT_FILE = os.path.join(TEST_DATA_DIR, "dummy.txt")
TEMP_EXPORT_CSV_FILE = os.path.join(TEST_DATA_DIR, "dummy.csv")
TEMP_EXPORT_JSON_FILE = os.path.join(TEST_DATA_DIR, "dummy_export.json")
TEMP_CREATE_BACKUP_FILE = os.path.join(TEST_DATA_DIR, "create_backup.json")
TEMP_UPDATE_BACKUP_FILE = os.path.join(TEST_DATA_DIR, "update_backup.json")
TEMP_SERVICE_ACCOUNT_FILE = os.path.join(TEST_DATA_DIR, "service_account.json")
TEMP_GENERATE_FILES = os.path.join(TEST_DATA_DIR, "generate_files")
# Permissions are required to be set for test_data directory recursively,
# otherwise the test cases are failed.
os.system(f"chmod -R +rw {TEST_DATA_DIR}")


@pytest.fixture()
def list_forwarder_data() -> MockResponse:
  """Test data to fetch forwarder."""
  data = MockResponse(
      status_code=200,
      text="""{"forwarders":[{"name":"forwarders/asdf1234-1234-abcd-efgh-12345678abcd","displayName":"forwarder 1","config":{"uploadCompression":"TRUE","metadata":{"assetNamespace":"test_namespace","labels":[{"key":"my_key_1","value":"my_value_1"},{"key":"my_key_2","value":"my_value_2"}]},"regexFilter":[{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"ALLOW"},{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"BLOCK"}],"serverSetting":{"state":"ACTIVE","gracefulTimeout":234,"drainTimeout":567,"httpSettings":{"port":10000,"host":"10.0.1.3","readTimeout":29,"readHeaderTimeout":34,"writeTimeout":2,"idleTimeout":34,"routeSettings":{"availableStatusCode":12,"readyStatusCode":33,"unreadyStatusCode":43}}}},"state":"ACTIVE"}]}"""
  )
  return data


@pytest.fixture()
def get_forwarder_data() -> MockResponse:
  """Test data to fetch forwarder."""
  data = MockResponse(
      status_code=200,
      text="""{"name":"forwarders/asdf1234-1234-abcd-efgh-12345678abcd","displayName":"forwarder 1","config":{"uploadCompression":"TRUE","metadata":{"assetNamespace":"test_namespace","labels":[{"key":"my_key_1","value":"my_value_1"},{"key":"my_key_2","value":"my_value_2"}]},"regexFilter":[{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"ALLOW"},{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"BLOCK"}],"serverSetting":{"state":"ACTIVE","gracefulTimeout":234,"drainTimeout":567,"httpSettings":{"port":10000,"host":"10.0.1.3","readTimeout":29,"readHeaderTimeout":34,"writeTimeout":2,"idleTimeout":34,"routeSettings":{"availableStatusCode":12,"readyStatusCode":33,"unreadyStatusCode":43}}}},"state":"ACTIVE"}"""
  )
  return data


@pytest.fixture()
def list_forwarders_data() -> MockResponse:
  """Test data to fetch list of forwarders."""
  data = MockResponse(
      status_code=200,
      text="""{"forwarders":[{"name":"forwarders/asdf1234-1234-abcd-efgh-12345678abcd","displayName":"forwarder 1","config":{"uploadCompression":"TRUE","metadata":{"assetNamespace":"test_namespace","labels":[{"key":"my_key_1","value":"my_value_1"},{"key":"my_key_2","value":"my_value_2"}]},"regexFilter":[{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"ALLOW"},{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"BLOCK"}],"serverSetting":{"state":"ACTIVE","gracefulTimeout":234,"drainTimeout":567,"httpSettings":{"port":10000,"host":"10.0.1.3","readTimeout":29,"readHeaderTimeout":34,"writeTimeout":2,"idleTimeout":34,"routeSettings":{"availableStatusCode":12,"readyStatusCode":33,"unreadyStatusCode":43}}}},"state":"ACTIVE"},{"name":"forwarders/asdf1234-1234-abcd-efgh-12345678abcd","displayName":"forwarder 1","config":{"uploadCompression":"TRUE","metadata":{"assetNamespace":"test_namespace","labels":[{"key":"my_key_1","value":"my_value_1"},{"key":"my_key_2","value":"my_value_2"}]},"regexFilter":[{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"ALLOW"},{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"BLOCK"}],"serverSetting":{"state":"ACTIVE","gracefulTimeout":234,"drainTimeout":567,"httpSettings":{"port":10000,"host":"10.0.1.3","readTimeout":29,"readHeaderTimeout":34,"writeTimeout":2,"idleTimeout":34,"routeSettings":{"availableStatusCode":12,"readyStatusCode":33,"unreadyStatusCode":43}}}},"state":"ACTIVE"}]}"""
  )
  return data


@pytest.fixture()
def list_collectors_data() -> MockResponse:
  """Test data to fetch list of collectors."""
  data = MockResponse(
      status_code=200,
      text="""{"collectors":[{"name":"forwarders/asdf1234-1234-abcd-efgh-12345678abcd/collectors/asdf1234-1234-abcd-efgh","displayName":"collector pqr","config":{"logType":"Type of logs collected.","metadata":{"assetNamespace":"test_namespace","labels":[{"key":"my_key_1","value":"my_value_1"},{"key":"my_key_2","value":"my_value_2"}]},"regexFilter":[{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"ALLOW"},{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"BLOCK"}],"diskBuffer":{"state":"ACTIVE","directoryPath":"Directory path for files written.","maxFileBufferBytes":3999},"maxSecondsPerBatch":10,"maxBytesPerBatch":1048576,"fileSettings":{"filePath":"Path of file to monitor."}},"state":"ACTIVE"}]}"""
  )
  return data


@pytest.fixture()
def list_empty_forwarders_data() -> MockResponse:
  """Test data to fetch list of forwarders with empty response."""
  data = MockResponse(status_code=200, text="""{}""")
  return data


@pytest.fixture()
def list_empty_collectors_data() -> MockResponse:
  """Test data to fetch list of collectors with empty response."""
  data = MockResponse(status_code=200, text="""{}""")
  return data


@pytest.fixture()
def list_error_forwarders_data() -> MockResponse:
  """Test data to fetch list of forwarders with error response."""
  data = MockResponse(
      status_code=400,
      text="""{"error": {"message": "Failed to list forwarders."}}""")
  return data


@pytest.fixture()
def list_error_collectors_data() -> MockResponse:
  """Test data to fetch list of collectors with error response."""
  data = MockResponse(
      status_code=400,
      text="""{"error": {"message": "generic::invalid_argument: parent (forwarders/abx-22) does not contain a valid UUID: invalid argument"}}"""
  )
  return data


@pytest.fixture()
def get_forwarder_not_exist_data() -> MockResponse:
  """Test data to fetch forwarder with not found status code."""
  data = MockResponse(
      status_code=404,
      text="""{"error": {"message":"Forwarder does not exist."}}""")
  return data


@pytest.fixture()
def get_forwarder_id_invalid_data() -> MockResponse:
  """Test data to fetch forwarder with bad request status code."""
  data = MockResponse(status_code=400, text="""{"dummy": "data"}""")
  return data


@pytest.fixture()
def internal_server_error() -> MockResponse:
  """Test data to fetch forwarder with server error status code."""
  data = MockResponse(
      status_code=500,
      text="""{"error": {"message": "Internal Server Error"}}""")
  return data


@pytest.fixture()
def regex_filters() -> List[Dict[str, Any]]:
  """Test data contains list of regex filters.

  Returns:
    List of regex filters.
  """
  filters = [{
      "description":
          "Describes what is being filtered and why",
      "regexp":
          "The regular expression used to match against each incoming line",
      "behavior":
          "ALLOW"
  }, {
      "description":
          "Describes what is being filtered and why",
      "regexp":
          "The regular expression used to match against each incoming line",
      "behavior":
          "BLOCK"
  }]
  return filters


@pytest.fixture()
def forwarder_response() -> Dict[str, Any]:
  """Test data of sample forwarder response body."""
  response = {
      "forwarder": {
          "name": "forwarder 1",
          "displayName": "User-specified forwarder name",
          "config": {
              "uploadCompression": "TRUE",
              "metadata": {
                  "assetNamespace":
                      "test_namespace",
                  "labels": [{
                      "key": "my_key_1",
                      "value": "my_value_1"
                  }, {
                      "key": "my_key_2",
                      "value": "my_value_2"
                  }]
              },
              "regexFilter": [{
                  "description": "Describes what is being filtered and why",
                  "regexp": "The regular expression used to match against each "
                            "incoming line",
                  "behavior": "ALLOW"
              }, {
                  "description": "Describes what is being filtered and why",
                  "regexp": "The regular expression used to match against each "
                            "incoming line",
                  "behavior": "BLOCK"
              }],
              "serverSetting": {
                  "state": "ACTIVE",
                  "gracefulTimeout": 234,
                  "drainTimeout": 567,
                  "httpSettings": {
                      "port": 10000,
                      "host": "10.0.1.3",
                      "readTimeout": 29,
                      "readHeaderTimeout": 34,
                      "writeTimeout": 2,
                      "idleTimeout": 34,
                      "routeSettings": {
                          "availableStatusCode": 12,
                          "readyStatusCode": 33,
                          "unreadyStatusCode": 43
                      }
                  }
              }
          },
          "state": "ACTIVE"
      }
  }
  return response


@pytest.fixture(scope="function", autouse=True)
def cleanup(request: Any):
  """Cleanup a testing file once we are finished."""

  def remove_test_files():
    files = [
        TEMP_EXPORT_CSV_FILE, TEMP_EXPORT_TXT_FILE, TEMP_EXPORT_JSON_FILE,
        TEMP_SERVICE_ACCOUNT_FILE
    ]
    for file_path in files:
      try:
        os.remove(file_path)
      except FileNotFoundError:
        pass

  request.addfinalizer(remove_test_files)


@pytest.fixture()
def get_forwarder_schema() -> Any:
  """Test data of sample forwarder schema."""
  data = {
      "forwarderSchema": [{
          "fieldPath": "display_name",
          "displayName": "Forwarder Display Name",
          "description": "User-specified forwarder name",
          "type": "STRING",
          "isRequired": True
      }]
  }

  return data


@pytest.fixture()
def get_collector_schema() -> Any:
  """Test data of sample collector schema."""
  data = {
      "collectorSchema": [{
          "fieldPath": "displayName",
          "displayName": "Collector Display Name",
          "description": "User-specified collector name",
          "type": "STRING",
          "isRequired": True
      }]
  }

  return data


@pytest.fixture()
def non_primitive_schema() -> Any:
  """Test data of non-primitive type field schema."""
  data = [{
      "fieldPath":
          "metadata",
      "displayName":
          "Forwarder Metadata",
      "description":
          "Metadata applied at the Forwarder level",
      "type":
          "metadata",
      "metadata": [{
          "fieldPath": "asset_namespace",
          "displayName": "Asset Namespace",
          "description": "Namespace used for Forwarder or collection",
          "type": "STRING"
      }]
  }, {
      "fieldPath":
          "regex_filters",
      "displayName":
          "Collector Regex Filters",
      "description":
          "Filters applied at the collector level",
      "type":
          "regexFilters",
      "isRequired":
          True,
      "regexFilters": [{
          "fieldPath": "description",
          "displayName": "Filter Description",
          "description": "Describes what is being filtered and why",
          "type": "STRING"
      }]
  }, {
      "fieldPath":
          "config",
      "displayName":
          "Forwarder Cofiguration",
      "description":
          "Forwarder configuration settings",
      "type":
          "config",
      "config": [{
          "fieldPath": "upload_compression",
          "displayName": "Upload Compression",
          "description": "Determines if uploaded data will be compressed",
          "defaultValue": True,
          "type": "BOOL"
      }]
  }]

  return data


@pytest.fixture()
def bool_field_schema() -> Any:
  """Test data of bool type field schema."""
  data = {
      "fieldPath": "upload_compression",
      "displayName": "Upload Compression",
      "description": "Determines if uploaded data will be compressed",
      "defaultValue": True,
      "isRequired": True,
      "type": "BOOL"
  }
  return data


@pytest.fixture()
def str_field_schema() -> Any:
  """Test data of bool type field schema."""
  data = [{
      "fieldPath": "display_name",
      "displayName": "Forwarder Display Name",
      "description": "User-specified forwarder name",
      "type": "STRING",
      "isRequired": True
  }]
  return data


@pytest.fixture()
def int_field_schema() -> Any:
  """Test data of bool type field schema."""
  data = [{
      "fieldPath": "max_bytes",
      "displayName": "Maximum bytes",
      "type": "INT",
  }]
  return data


@pytest.fixture()
def enum_field_schema() -> Any:
  """Test data of enum type field schema."""
  data = {
      "fieldPath":
          "behavior",
      "displayName":
          "Filter Behavior",
      "description":
          "Filter behavior to apply when a match is found",
      "type":
          "ENUM",
      "enumFieldSchemas": [{
          "value": "ALLOW",
          "displayName": "allow"
      }, {
          "value": "BLOCK",
          "displayName": "block"
      }]
  }
  return data


@pytest.fixture()
def label_field_schema() -> Any:
  """Test data of label type field schema."""
  data = [{
      "fieldPath": "labels",
      "displayName": "Forwarder Labels",
      "description": "Arbitrary KV labels",
      "type": "LABEL"
  }]
  return data


@pytest.fixture()
def oneof_field_schema() -> Any:
  """Test data of oneof type field schema."""
  data = [{
      "fieldPath":
          "settings",
      "displayName":
          "Configure Ingestion Settings",
      "description":
          "Ingestion settings of the collector",
      "type":
          "ONEOF",
      "oneOfFieldSchemas": [{
          "fieldPath":
              "file_settings",
          "displayName":
              "File Settings",
          "type":
              "fileSettings",
          "fileSettings": [{
              "fieldPath": "file_path",
              "displayName": "File Path",
              "description": "Path of file to monitor",
              "type": "STRING"
          }]
      }, {
          "fieldPath": "kafka_settings",
          "displayName": "Kafka Settings",
          "type": "kafkaSettings"
      }, {
          "fieldPath": "pcap_settings",
          "displayName": "Pcap Settings",
          "type": "pcapSettings"
      }, {
          "fieldPath": "splunk_settings",
          "displayName": "Splunk Settings",
          "type": "splunkSettings",
      }, {
          "fieldPath": "syslog_settings",
          "displayName": "Syslog Settings",
          "description": "Syslog settings",
      }]
  }]
  return data


@pytest.fixture()
def repeated_message_fields_schema() -> Any:
  """Test data of repeated_message_fields schema."""
  data = [{
      "fieldPath":
          "settings",
      "displayName":
          "Configure Ingestion Settings",
      "description":
          "Ingestion settings of the collector",
      "type":
          "ONEOF",
      "oneOfFieldSchemas": [{
          "fieldPath": "file_settings",
          "displayName": "File Settings",
          "type": "STRING"
      }, {
          "fieldPath":
              "kafka_settings",
          "displayName":
              "Kafka Settings",
          "type":
              "kafkaSettings",
          "kafkaSettings": [{
              "fieldPath":
                  "regex_filters",
              "displayName":
                  "Forwarder Regex Filters",
              "description":
                  "Filters applied at the Forwarder level",
              "type":
                  "regexFilters",
              "isRepeated":
                  True,
              "regexFilters": [{
                  "fieldPath": "description",
                  "displayName": "Filter Description",
                  "description": "Describes what is being filtered and why",
                  "type": "STRING"
              },]
          }]
      }, {
          "fieldPath": "pcap_settings",
          "displayName": "Pcap Settings",
          "type": "pcapSettings"
      }]
  }]
  return data


@pytest.fixture()
def oneof_validate_data() -> Any:
  """Test data to validate oneof input."""
  data = [{
      "fieldPath": "file_path",
      "displayName": "File Path",
      "description": "Path of file to monitor",
      "type": "STRING"
  }]
  return data


def create_backup_file(file_path: str, content: Dict[str, Any]) -> None:
  """Create a temporary backup file at the test_data dir with the content.

  Args:
    file_path (str): Path to create the temp backup file.
    content (Dict): JSON content to be written in the file.
  """
  if not os.path.exists(file_path):
    with open(file_path, "w") as file:
      if content:
        file.write(json.dumps(content))


@pytest.fixture()
def repeated_field_schema() -> Any:
  """Test data of repeated field schema."""
  data = [{
      "fieldPath": "brokers",
      "displayName": "Kafka Brokers",
      "type": "REPEATED_STRING"
  }]
  return data


@pytest.fixture()
def generate_forwarder_file() -> MockResponse:
  """Test data of API to generate forwarder file."""
  data = MockResponse(
      status_code=200, text="""{"config": "output","auth": "authoutput"}""")
  return data
