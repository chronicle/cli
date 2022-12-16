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
"""Utility functions."""
from typing import Any

from common import api_utility
from common import uri
from common.constants import key_constants
from common.constants import status
from forwarders.constants import schema

API_VERSION = "v2"


def get_collector_url(region: str, custom_url: str, forwarder_id: str) -> str:
  """Gets collector URL according to selected region.

  Args:
    region (str): Region (US, EUROPE, ASIA_SOUTHEAST1).
    custom_url (str): Base URL to be used for API calls.
    forwarder_id (str): Forwarder uuid to which collector belongs.

  Returns:
    str: Collector URL.
  """

  return uri.get_base_url(
      region,
      custom_url) + f"/{API_VERSION}/forwarders/{forwarder_id}/collectors"


def fetch_collectors(url: str, method: str, client: Any) -> Any:
  """Fetches list of collectors for respective forwarders.

  Args:
    url (str): Url to be used for API calls.
    method (str): Method to be used for API calls.
    client (Any):  HTTP session object to send authorized requests and receive
      responses.

  Returns:
    Tuple(Dict, Dict): list of collectors response for forwarder.
  """
  # Store error message in dictionary if API returns bad status code
  # represent error on console in yaml format.
  collector_errors = {}
  collector_errors[schema.KEY_COLLECTORS] = {}
  list_collectors_response = {}

  list_collectors_response = client.request(method, url)
  status_code = list_collectors_response.status_code
  list_collectors_response = api_utility.check_content_type(
      list_collectors_response.text)

  if not list_collectors_response:
    collector_errors[schema.KEY_COLLECTORS][
        key_constants.KEY_MESSAGE] = "No collectors found for this forwarder."

  if status_code != status.STATUS_OK:

    collector_errors[schema.KEY_COLLECTORS][key_constants.KEY_ERROR] = {
        schema.KEY_RESPONSE_CODE:
            status_code,
        key_constants.KEY_MESSAGE:
            list_collectors_response[key_constants.KEY_ERROR]
            [key_constants.KEY_MESSAGE]
    }

  return list_collectors_response, collector_errors
