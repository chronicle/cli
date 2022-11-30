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

import os
from typing import Any, Dict, List

import pytest

from mock_test_utility import MockResponse

TEST_DATA_DIR = os.path.dirname(__file__)
TEMP_EXPORT_TXT_FILE = os.path.join(TEST_DATA_DIR, "dummy.txt")
TEMP_EXPORT_CSV_FILE = os.path.join(TEST_DATA_DIR, "dummy.csv")
TEMP_EXPORT_JSON_FILE = os.path.join(TEST_DATA_DIR, "dummy_export.json")
TEMP_SERVICE_ACCOUNT_FILE = os.path.join(TEST_DATA_DIR, "service_account.json")
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
def get_forwarder_server_error_code() -> MockResponse:
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
