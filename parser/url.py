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
"""Return URLs to interact with CBN APIs."""

from typing import Dict
import urllib.parse

from common import uri

API_VERSION = 'v1'
HTTP_REQUEST_TIMEOUT_IN_SECS = 1200
HTTP_REQUEST_HEADERS = {'Content-type': 'application/x-www-form-urlencoded'}
PATH_DICT = {
    'list': 'tools/cbnParsers',
    'run': 'tools:validateCbnParser',
    'history': 'tools/cbnParsers:listCbnParserHistory',
    'generate': 'tools:retrieveSampleLogs',
    'status': 'tools/cbnParsers',
    'list_errors': 'tools/cbnParsers:listCbnParserErrors'
}


def get_url(region: str, command: str, environment: str,
            **query_params: Dict[str, str]) -> str:
  """Get URL for the given command.

  Args:
    region (str): Region (US, EUROPE, ASIA_SOUTHEAST1)
    command (str): Command name
    environment (str): Environment (prod, test)
    **query_params(Dict): Query
      parameters

  Returns:
    str: URL to interact with CBN APIs.
  """
  url = f'{uri.get_base_url(region, "", environment)}/{API_VERSION}/{PATH_DICT[command]}'
  if query_params:
    url += f'?{urllib.parse.urlencode(query_params)}'
  return url
