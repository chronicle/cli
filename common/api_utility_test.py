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
"""Unit tests for api_utility.py."""

from typing import Any
import pytest

from common import api_utility


def test_content_type_is_json() -> None:
  """Test that the API response is JSON."""
  json_api_response = api_utility.check_content_type('{"key": "value"}')
  assert json_api_response == {'key': 'value'}


def test_content_type_is_not_json() -> None:
  """Test that the API response is not JSON."""
  with pytest.raises(TypeError, match='URL is not reachable.'):
    api_utility.check_content_type('{"key": "value"')


def test_print_request_details(capfd: Any) -> None:
  """Test printing request details."""
  api_utility.print_request_details('test.com', 'GET',
                                    {'header': 'test header'},
                                    {'body': 'test response'})
  console_output, _ = capfd.readouterr()
  assert console_output == """==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: test.com
  Method: GET
  Body: {'header': 'test header'}
Response:
  Body: {'body': 'test response'}

"""
