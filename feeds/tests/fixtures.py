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

import datetime
import json
import os
from typing import Any, Dict, List
from unittest import mock

import pytest

from feeds import feed_schema_utility
from mock_test_utility import MockResponse

TEST_DATA_DIR = os.path.dirname(__file__)
TEMP_EXPORT_TXT_FILE = os.path.join(TEST_DATA_DIR, "dummy.txt")
TEMP_EXPORT_CSV_FILE = os.path.join(TEST_DATA_DIR, "dummy.csv")
TEMP_EXPORT_JSON_FILE = os.path.join(TEST_DATA_DIR, "dummy_export.json")
TEMP_CREATE_BACKUP_FILE = os.path.join(TEST_DATA_DIR, "create_backup.json")
TEMP_UPDATE_BACKUP_FILE = os.path.join(TEST_DATA_DIR, "update_backup.json")
TEMP_SERVICE_ACCOUNT_FILE = os.path.join(TEST_DATA_DIR, "service_account.json")
# Permissions are required to be set for test_data directory recursively,
# otherwise the test cases are failed.
os.system(f"chmod -R +rw {TEST_DATA_DIR}")


@pytest.fixture()
def list_empty_feeds_data() -> MockResponse:
  """Test input data."""
  data = MockResponse(status_code=200, text="""{}""")
  return data


@pytest.fixture()
def list_error_feeds_data() -> MockResponse:
  """Test input data."""
  data = MockResponse(
      status_code=400,
      text="""{"error": {"message": "Failed to find feeds."}}""")
  return data


@pytest.fixture()
def list_feeds_data() -> MockResponse:
  """Test input data."""
  data = MockResponse(
      status_code=200,
      text="""{"feeds": [{"name": "feeds/123","displayName": "Dummy feed display name","details": {
          "logType": "DUMMY_LOGTYPE", "feedSourceType": "DUMMY",
          "namespace": "sample_namespace", "labels": [{"key": "k", "value": "v"}],
            "dummySettings": {"field1": "abc.dummy.com", "field2": "ID"}},
            "feedState": "INACTIVE"}]}""")
  return data


@pytest.fixture()
def list_missing_key_feeds_data() -> MockResponse:
  """Test input data."""
  data = MockResponse(
      status_code=200,
      text="""{"feeds": [{"name": "feeds/123", "displayName": "Dummy feed display name", "details": {
          "logType": "DUMMY_LOGTYPE", "feedSourceType": "DUMMY",
            "dummySettings": {"field1": "abc.dummy.com", "field2": "ID"}},
            "feedState": "INACTIVE"},
            {"name": "feeds/321", "details": {
            "feedSourceType": "DUMMY",
            "dummySettings": {"field1": "abc.dummy.com", "field2": "ID"}},
            "feedState": "INACTIVE"}]}""")
  return data


@pytest.fixture()
def get_feed_schema() -> MockResponse:
  """Test input data."""
  data = MockResponse(
      status_code=200,
      text="""{
        "feedSourceTypeSchemas": [
            {
                "description": "Dummy Source Type",
                "displayName": "Dummy Source Type",
                "feedSourceType": "DUMMY",
                "logTypeSchemas": [
                    {
                        "detailsFieldSchemas": [
                            {
                                "description": "Dummy field data for logType.",
                                "displayName": "Field 1",
                                "fieldPath": "details.dummy_settings.field1",
                                "isRequired": true,
                                "type": "STRING"
                            },
                            {
                                "description": "Dummy field data for logType.",
                                "displayName": "Field 2",
                                "fieldPath": "details.dummy_settings.field2",
                                "isRequired": true,
                                "type": "STRING"
                            }
                        ],
                        "displayName": "Dummy LogType",
                        "logType": "DUMMY_LOGTYPE",
                        "name": "feedSourceTypeSchemas/API/logTypeSchemas/TEST"
                    }
                ],
                "name": "feedSourceTypeSchemas/API"
            },
            {
              "displayName": "Dummy Source Type 2",
              "feedSourceType": "DUMMY2",
                "logTypeSchemas": [
                    {
                        "detailsFieldSchemas": [
                            {
                                "description": "Dummy field data for logType.",
                                "displayName": "Field 1",
                                "fieldPath": "details.dummy_settings.field1",
                                "isRequired": true,
                                "type": "STRING"
                            },
                            {
                                "description": "Dummy field data for logType.",
                                "displayName": "Field 2",
                                "fieldPath": "details.dummy_settings.field2",
                                "isRequired": true,
                                "type": "STRING"
                            }
                        ],
                        "displayName": "Dummy LogType2",
                        "logType": "DUMMY_LOGTYPE2",
                        "name": "feedSourceTypeSchemas/API2/logTypeSchemas/TEST2"
                    }
                ],
                "name": "feedSourceTypeSchemas/API2"
            },
            {
              "displayName": "Dummy Source Type 3",
              "feedSourceType": "DUMMY3",
                "logTypeSchemas": [
                    {
                        "detailsFieldSchemas": [
                            {
                                "description": "Dummy field data for logType.",
                                "displayName": "Field 1",
                                "fieldPath": "details.dummy_settings.field1",
                                "isRequired": true,
                                "type": "STRING"
                            },
                            {
                                "description": "Dummy field data for logType.",
                                "displayName": "Field 2",
                                "fieldPath": "details.dummy_settings.field2",
                                "isRequired": true,
                                "type": "STRING"
                            }
                        ],
                        "displayName": "Dummy LogType3",
                        "logType": "DUMMY_LOGTYPE3",
                        "name": "feedSourceTypeSchemas/API3/logTypeSchemas/TEST3"
                    }
                ],
                "name": "feedSourceTypeSchemas/API3"
            }
        ]
    }""")
  return data


@pytest.fixture()
def get_feed_data() -> MockResponse:
  """Test input data."""
  data = MockResponse(
      status_code=200,
      text="""{"name": "feeds/123", "displayName": "Dummy feed display name","details": {"logType": "DUMMY_LOGTYPE",
        "namespace": "sample_namespace", "labels": [{"key": "k", "value": "v"}],
        "feedSourceType": "DUMMY",
            "dummySettings": {"field1": "abc.dummy.com", "field2": "ID"}},
            "feedState": "INACTIVE"}""")
  return data


@pytest.fixture()
def get_fail_feed_data() -> MockResponse:
  """Test input data."""
  data = MockResponse(
      status_code=200,
      text="""{"name": "feeds/123", "displayName": "Dummy feed display name", "details": {"logType": "TEMP_LOGTYPE",
            "feedSourceType": "DUMMY",
            "dummySettings": {"field1": "abc.dummy.com", "field2": "ID"}},
            "feedState": "INACTIVE"}""")
  return data


@pytest.fixture()
def get_feed_not_exist_data() -> MockResponse:
  """Test input data."""
  data = MockResponse(
      status_code=400, text="""{"error": {"message":"Feed does not exist."}}""")
  return data


@pytest.fixture()
def get_feed_id_invalid_data() -> MockResponse:
  """Test input data."""
  data = MockResponse(status_code=404, text="""{"dummy": "data"}""")
  return data


@pytest.fixture()
def get_flattened_response() -> Dict[str, str]:
  """Test input data."""
  data = {
      "name": "feeds/123",
      "displayName": "Dummy feed display name",
      "details.log_type": "WORKDAY",
      "details.feed_source_type": "API",
      "details.workday_settings.hostname": "abc.workday.com",
      "details.workday_settings.tenant_id": "ID"
  }
  return data


@pytest.fixture()
def get_detailed_schema() -> Any:
  """Test input data."""
  data = feed_schema_utility.DetailedSchema(
      "Third party API", {
          "name":
              "feedSourceTypeSchemas/API/logTypeSchemas/WORKDAY",
          "displayName":
              "Workday",
          "logType":
              "WORKDAY",
          "detailsFieldSchemaAlternatives": [{
              "detailsFieldSchemaSets": [{
                  "displayName":
                      "OAuth non-expiring access token",
                  "description":
                      "OAuth 2.0 authorization",
                  "detailsFieldSchemas": [{
                      "fieldPath": "details.http_settings.oauth_access_token",
                      "displayName": "Access token",
                      "type": "STRING"
                  }]
              }]
          }],
          "detailsFieldSchemas": [{
              "fieldPath": "details.workday_settings.hostname",
              "displayName": "API Hostname",
              "type": "STRING"
          }, {
              "fieldPath": "details.workday_settings.tenant_id",
              "displayName": "Tenant",
              "type": "STRING"
          }]
      }, None)
  return data


@pytest.fixture()
def get_detailed_schema_input() -> Dict[str, Any]:
  """Test input data."""
  data = {
      "feedSourceTypeSchemas": [{
          "description": "Dummy Source Type",
          "displayName": "Dummy Source Type",
          "feedSourceType": "DUMMY",
          "logTypeSchemas": [{
              "detailsFieldSchemas": [{
                  "description": "Dummy field data for the logType.",
                  "displayName": "Field 1",
                  "fieldPath": "details.dummy_settings.field1",
                  "isRequired": True,
                  "type": "STRING"
              }, {
                  "description": "Dummy field data for the logType.",
                  "displayName": "Field 2",
                  "fieldPath": "details.dummy_settings.field2",
                  "isRequired": True,
                  "type": "STRING"
              }],
              "displayName": "Dummy LogType",
              "logType": "DUMMY_LOGTYPE",
              "name": "feedSourceTypeSchemas/API/logTypeSchemas/WORKDAY"
          }],
          "name": "feedSourceTypeSchemas/API"
      }]
  }
  return data


@pytest.fixture()
def get_schema_response() -> List[Any]:
  """Test input data."""
  data = ([
      "2022-03-05 11:00:00.000000", {
          "feedSourceTypeSchemas": [{
              "description": "Dummy Source Type",
              "displayName": "Dummy Source Type",
              "feedSourceType": "DUMMY",
              "logTypeSchemas": [{
                  "detailsFieldSchemas": [{
                      "description": "Dummy field data for the logType.",
                      "displayName": "Field 1",
                      "fieldPath": "details.dummy_settings.field1",
                      "isRequired": True,
                      "type": "STRING"
                  }, {
                      "description": "Dummy field data for the logType.",
                      "displayName": "Field 2",
                      "fieldPath": "details.dummy_settings.field2",
                      "isRequired": True,
                      "type": "STRING"
                  }],
                  "displayName": "Dummy LogType",
                  "logType": "DUMMY_LOGTYPE",
                  "name": "feedSourceTypeSchemas/API/logTypeSchemas/WORKDAY"
              }],
              "name": "feedSourceTypeSchemas/API"
          }]
      }
  ])
  return data


@pytest.fixture()
def get_schema_str_response() -> Dict[str, Any]:
  """Test input data."""
  data = {
      "feedSourceTypeSchemas": [{
          "description": "Dummy Source Type",
          "displayName": "Dummy Source Type",
          "feedSourceType": "DUMMY",
          "logTypeSchemas": [{
              "detailsFieldSchemas": [{
                  "description": "Dummy field data for logType.",
                  "displayName": "Field 1",
                  "fieldPath": "details.dummy_settings.field1",
                  "isRequired": True,
                  "type": "STRING"
              }, {
                  "description": "Dummy field data for logType.",
                  "displayName": "Field 2",
                  "fieldPath": "details.dummy_settings.field2",
                  "isRequired": True,
                  "type": "STRING"
              }],
              "displayName": "Dummy LogType",
              "logType": "DUMMY_LOGTYPE",
              "name": "feedSourceTypeSchemas/API/logTypeSchemas/TEST"
          }],
          "name": "feedSourceTypeSchemas/API"
      }]
  }
  return data


@pytest.fixture()
def log_source_map() -> Dict[str, Any]:
  """Return test data containing log type and source type map.

  Returns:
    Dict[str, Any]: Test data
  """
  return {
      "AMAZON_S3": {
          "displayName": "Amazon S3",
          "logTypes": [("ONEPASSWORD", "1Password")]
      }
  }


@pytest.fixture()
def client() -> Any:
  """Return mock object of FeedSchema.

  Returns:
    mock.MagicMock: Mock object
  """
  with mock.patch.object(feed_schema_utility.FeedSchema, "__init__",
                         lambda w, x, y, z: None):
    mocked_client = feed_schema_utility.FeedSchema("dummy.json", "US",
                                                   "test.com")
    mocked_client.client = mock.MagicMock()
    mocked_client.current_time = datetime.datetime.now()
    mocked_client.schema_response = mock.MagicMock()
    mocked_client.region = "US"
    mocked_client.custom_url = "https://dummy.com"
    mocked_client.pre_body = {}
  return mocked_client


@pytest.fixture(scope="function", autouse=True)
def cleanup(request: Any):
  """Cleanup a testing file once we are finished."""

  def remove_test_files():
    files = [
        TEMP_EXPORT_CSV_FILE, TEMP_EXPORT_TXT_FILE, TEMP_CREATE_BACKUP_FILE,
        TEMP_UPDATE_BACKUP_FILE, TEMP_EXPORT_JSON_FILE,
        TEMP_SERVICE_ACCOUNT_FILE
    ]
    for file_path in files:
      try:
        os.remove(file_path)
      except FileNotFoundError:
        pass

  request.addfinalizer(remove_test_files)


def create_backup_file(file_path: str, content: Dict[str, Any]) -> None:
  """Create temporary backup file at the test_data dir with the content.

  Args:
    file_path (str): Path to create the temp backup file.
    content (Dict): JSON content to be written in the file.
  """
  if not os.path.exists(file_path):
    with open(file_path, "w") as file:
      if content:
        file.write(json.dumps(content))


@pytest.fixture()
def get_active_feed_data() -> MockResponse:
  """Test input data."""
  data = MockResponse(
      status_code=200,
      text="""{"name": "feeds/123", "displayName": "Dummy feed display name", "details": {"logType": "DUMMY_LOGTYPE",
        "feedSourceType": "DUMMY",
            "dummySettings": {"field1": "abc.dummy.com", "field2": "ID"}},
            "feedState": "ACTIVE"}""")
  return data


def create_service_account_file():
  """Test credential data."""
  fake_json_credentials = b"""{
    "client_email": "fake-username@fake-project.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com/token",
    "private_key": "
  """
  fake_private_key = b"""-----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDemycWcEiVMMKm
    /S3f8oRkgxVvbi14D0TWFBUPZq9w1nc7L4Udz7NZ8BKC49DuKi1EgwxF8z0Bve5i
    k6UMfb4JeXLkSSQN4Zy5IbZUr9Mm3w0sjIzTeA1JmIqY+r3EbUxeqFjpqc02HW4h
    j0L7Wj2on9KTvMd0zFRCsLLz7KoZyykDKW3jbvDBNx9n3uUNBb+ZriYNbuAWCSlC
    XD8QbVHq3dqFQFpsofHknDX/+UUS7Q85War4Y2qqdV7SwtTdy2LoNHKLLBHU0WMG
    8x6PZueahkO2tipebJN6js4tSxSyk8sYFkU6onZJV91ysE+7QuS0HdhHTYfZSnC5
    zHmJgyHVAgMBAAECggEABWtajsHKCpPG0WDtinuxfG7yiSVyBu+8OcgAYUEbOVCH
    U5ILGBgz4hclpDken4W4V2gnVtaeoBm7IXw9summxD1ILkWXkpzw/1LSSQqExff9
    Lp33Wbic/jMwAJxuHUeZ6d4IWBvxqoUZ5shBlbPzN1U4v68DXhURYhRCLw0OcRVE
    9I3Ohwy6MntjHAkNTvFrYxQBUnCsTKFKwkimn6huhwE8/nrMpYS8H/8DxPFsBprw
    AznRqWWfJ28yVoEzN+J1aIz631zk+LwSqY0m/TJra1uwMQ5J6bYqWlH8pS/UaI4s
    6Lbhukubpi7P03XpP1aHMwCpwcsZ6hGD7XpELDZBgQKBgQD8fF2lgDcX0ksvcgk2
    KKy4dPqwcONfB41lxbIYE9JZRo3hiWsAwQxfbW6Zt6cEdEqOnROw0jcaJhaKD+qf
    d14ciUA+NjeHyE1yJjbytOnO7fx5wlVamHUI0ykFH4NoN+GOI7zt3kLIb20Zvqab
    4Dt5e5qY5s+Mnr2wJVI8k4NcQQKBgQDhtFJ38bz7ehl9prTQ1AaAxAviU3XOBkko
    uDTglE2aoKjc3qoWoX6vT0iamsM3EYYVZxxbqzjSUCrhpSetKdP/NZNN3mtMvFzj
    ODXyhC43Ro3fVe+JvHzdxRtXbSwZ2GLmkbR8oyi7w4pU8rx9+/UfFOoiqcLIGQbb
    N03t8TJwlQKBgB2fVblaHpyb3phVb8E76m/Fwbe7tuFqWGuNU0TB5pb00SaZ4cT3
    4US86RH92wmJv0mWIj5Hm5Fk0JYoIeXNsmv0qmXiJIe4t2ViGGZHVXsirtF2PF9h
    rbF4XMKuHNO4Yq0zgjICNqGfeRRhKtj06OVq3At+YPFlmmm1Jz3WLL5BAoGAQ3hL
    Gs3px2cVjaky7iYjl4SDZPG8Co14ezKto+DRXgLe17+8Kq22GCPkOUtARgr4ARfk
    s0Z44u3SE8fyF2Kkm+rhEOsHOlYokkfwYIHA6wctS/D9fTgaP5U3eigJgeRclD5E
    LOn9ODvY81HopOSXvuXao+gJcRWCJi/fHNz4Tg0CgYEA0ruTbieHIzCjg8C1Sp40
    GBixMpHsZ2ld1OaqQvidYIUL48TutyQhWHaRIqaziSZJBaNIYB73pIQfLdHIi0hx
    3KHskc16JPhKgWLsl9cTP5GAIP2cqvSqBmnbvX+ArSRbqy4v7kxJwKPai+iaFi5H
    1njcNc79W7qohKZshYNUq/0=
    -----END PRIVATE KEY-----
  """
  fake_private_key = fake_private_key.replace(b" " * 4, b"")
  fake_private_key = fake_private_key.replace(b"\n", b"\\n")
  file_content = fake_json_credentials.strip() + fake_private_key + b'"\n}\n'
  with open(TEMP_SERVICE_ACCOUNT_FILE, "w") as file:
    file.write(str(file_content))
