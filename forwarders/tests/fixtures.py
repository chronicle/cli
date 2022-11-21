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
from typing import Any, Dict

import pytest

from mock_test_utility import MockResponse

TEST_DATA_DIR = os.path.dirname(__file__)
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
def list_forwarders_data() -> MockResponse:
  """Test data to fetch list of forwarders."""
  data = MockResponse(
      status_code=200,
      text="""{"forwarders":[{"name":"forwarders/asdf1234-1234-abcd-efgh-12345678abcd","displayName":"forwarder 1","config":{"uploadCompression":"TRUE","metadata":{"assetNamespace":"test_namespace","labels":[{"key":"my_key_1","value":"my_value_1"},{"key":"my_key_2","value":"my_value_2"}]},"regexFilter":[{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"ALLOW"},{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"BLOCK"}],"serverSetting":{"state":"ACTIVE","gracefulTimeout":234,"drainTimeout":567,"httpSettings":{"port":10000,"host":"10.0.1.3","readTimeout":29,"readHeaderTimeout":34,"writeTimeout":2,"idleTimeout":34,"routeSettings":{"availableStatusCode":12,"readyStatusCode":33,"unreadyStatusCode":43}}}},"state":"ACTIVE"},{"name":"forwarders/asdf1234-1234-abcd-efgh-12345678abcd","displayName":"forwarder 1","config":{"uploadCompression":"TRUE","metadata":{"assetNamespace":"test_namespace","labels":[{"key":"my_key_1","value":"my_value_1"},{"key":"my_key_2","value":"my_value_2"}]},"regexFilter":[{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"ALLOW"},{"description":"Describes what is being filtered and why","regexp":"The regular expression used to match against each incoming line","behavior":"BLOCK"}],"serverSetting":{"state":"ACTIVE","gracefulTimeout":234,"drainTimeout":567,"httpSettings":{"port":10000,"host":"10.0.1.3","readTimeout":29,"readHeaderTimeout":34,"writeTimeout":2,"idleTimeout":34,"routeSettings":{"availableStatusCode":12,"readyStatusCode":33,"unreadyStatusCode":43}}}},"state":"ACTIVE"}]}"""
  )
  return data


@pytest.fixture()
def list_empty_forwarders_data() -> MockResponse:
  """Test data to fetch list of forwarders with empty response."""
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
