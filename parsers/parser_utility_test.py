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
"""Unit tests for parser_utility."""

from parsers import parser_utility
from parsers.constants import key_constants


def test_decode_log() -> None:
  """Test decode log."""
  input_log = 'dGVzdF9sb2c='
  assert parser_utility.decode_log(input_log) == 'test_log'


def test_process_resource_name_for_parser() -> None:
  """Test process resource name for parser."""
  parent = 'projects/test_project/locations/test_location/instances/test_instance/logTypes/test_log_type/parsers/test_parser_id'
  component = parser_utility.process_resource_name(parent)
  assert component == {
      key_constants.KEY_PROJECTS: 'test_project',
      key_constants.KEY_LOCATIONS: 'test_location',
      key_constants.KEY_INSTANCES: 'test_instance',
      key_constants.KEY_LOGTYPES: 'test_log_type',
      key_constants.KEY_PARSERS: 'test_parser_id'
  }


def test_process_resource_name_for_parserextension() -> None:
  """Test process resource name for parserextension."""
  parent = 'projects/test_project/locations/test_location/instances/test_instance/logTypes/test_log_type/parserExtensions/test_parserextension_id'
  component = parser_utility.process_resource_name(parent)
  assert component == {
      key_constants.KEY_PROJECTS: 'test_project',
      key_constants.KEY_LOCATIONS: 'test_location',
      key_constants.KEY_INSTANCES: 'test_instance',
      key_constants.KEY_LOGTYPES: 'test_log_type',
      key_constants.KEY_PARSER_EXTENSIONS: 'test_parserextension_id'
  }
