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
from typing import List, Dict, Any

import pytest

from mock_test_utility import MockResponse


@pytest.fixture()
def collector_does_not_exist_response() -> MockResponse:
  """Test data to fetch forwarder with not found status code."""
  data = MockResponse(
      status_code=404,
      text="""{"error": {"message":"Collector does not exist."}}""")
  return data


@pytest.fixture()
def get_collector_id_invalid_response() -> MockResponse:
  """Test data to fetch forwarder with bad request status code."""
  data = MockResponse(status_code=400, text="""{"dummy": "data"}""")
  return data


@pytest.fixture()
def get_collectors_response() -> MockResponse:
  """Test data to fetch list of collectors."""
  data = MockResponse(
      status_code=200,
      text="""{"name":"forwarders/asdf1234-1234-abcd-efgh-12345678abcd/collectors/asdf1234-1234-abcd-efgh-12345678abcd","displayName":"collector pqr","config":{"logType":"Type of logs collected.","metadata":{"assetNamespace":"test_namespace","labels":[{"key":"my_key_1","value":"my_value_1"},{"key":"my_key_2","value":"my_value_2"}]},"regexFilter":[{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"ALLOW"},{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"BLOCK"}],"diskBuffer":{"state":"ACTIVE","directoryPath":"Directory path for files written.","maxFileBufferBytes":3999},"maxSecondsPerBatch":10,"maxBytesPerBatch":1048576,"fileSettings":{"filePath":"Path of file to monitor."}},"state":"ACTIVE"}"""
  )
  return data


@pytest.fixture()
def collector_500_response() -> MockResponse:
  """Test data to fetch collector with internal server error status code."""
  data = MockResponse(
      status_code=500,
      text="""{"error": {"message": "Internal Server Error"}}""")
  return data


@pytest.fixture()
def list_collector_data() -> MockResponse:
  """Test data to fetch list of collectors."""
  data = MockResponse(
      status_code=200,
      text="""{
  "collectors": [
    {
      "name": "forwarders/abc123-def457-ghi891-567/collectors/abc123-def457-ghi891-234",
      "displayName": "SplunkCollector",
      "config": {
        "logType": "WINDOWS_DNS",
        "maxSecondsPerBatch": 10,
        "maxBytesPerBatch": "1048576",
        "splunkSettings": {
          "host": "127.0.0.1",
          "minimumWindowSize": 10,
          "maximumWindowSize": 30,
          "queryString": "search index=* sourcetype=dns",
          "queryMode": "realtime",
          "port": 8089
        }
      },
      "state": "ACTIVE"
    }
  ]
}""")
  return data


@pytest.fixture()
def list_empty_collector_data() -> MockResponse:
  """Test data to fetch list of collectors with empty response."""
  data = MockResponse(status_code=200, text="""{}""")
  return data


@pytest.fixture()
def list_error_collector_data() -> MockResponse:
  """Test data to fetch list of collectors with error response."""
  data = MockResponse(
      status_code=400,
      text="""{"error": {"message": "generic::invalid_argument: parent (forwarders/abx-22) does not contain a valid UUID: invalid argument"}}"""
  )
  return data


@pytest.fixture()
def list_forwarder_id_invalid_data() -> MockResponse:
  """Test data to fetch forwarder with bad request status code."""
  data = MockResponse(
      status_code=400,
      text="""{"error": {"message": "Forwarder id is invalid"}}""")
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
