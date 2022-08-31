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
"""Unit tests for feed_utility.py."""

from typing import Dict
from feeds import feed_utility
from feeds.tests.fixtures import *  # pylint: disable=wildcard-import


def test_flatten_dict() -> None:
  """Test flattening of dict."""
  input_dict = {"a": {"b": "c"}, 1: {"a": [1]}, "p": {"q": {"r": "s"}}}
  expected_output = {"a.b": "c", "1.a": [1], "p.q.r": "s"}
  assert feed_utility.flatten_dict(input_dict) == expected_output


def test_defflatten_dict() -> None:
  """Test deflattening of dict."""
  input_dict = {"a.b": "c", "1.a": [1], "p.q.r": "s"}
  expected_output = {"a": {"b": "c"}, "1": {"a": [1]}, "p": {"q": {"r": "s"}}}
  assert feed_utility.deflatten_dict(input_dict) == expected_output


def test_swap_with_underscore() -> None:
  """Test converting of camelcase key name to snakecase key name."""
  assert feed_utility.swap_with_underscore(
      "workdaySettings") == "workday_settings"


def test_get_feed_details(get_flattened_response: Dict[str, str],
                          get_detailed_schema: Dict[str, str]) -> None:
  """Test printing of key-value pair after correlation with schema.

  Args:
    get_flattened_response (dict): Test input data
    get_detailed_schema (dict): Test input data
  """
  expected_output = ("  Feed Settings:\n    API Hostname: abc.workday.com\n    "
                     "Tenant: ID\n")
  assert feed_utility.get_feed_details(
      get_flattened_response,
      get_detailed_schema.log_type_schema) == expected_output


def test_snake_to_camel() -> None:
  """Test conversion of snakecase string to camelcase string."""
  assert feed_utility.snake_to_camel("feed_schema") == "feedSchema"


def test_lower_or_none() -> None:
  """Test conversion of string to lowercase string."""
  assert feed_utility.lower_or_none("TEST") == "test"


def test_lower_or_none_none() -> None:
  """Test return of string as None if string is None."""
  assert feed_utility.lower_or_none(None) is None


def test_get_labels() -> None:
  """Test printing of key-value pair of labels field."""
  expected_output = ("  Labels:\n    k: v\n")
  assert feed_utility.get_labels({"labels": [{
      "key": "k",
      "value": "v"
  }]}) == expected_output


def test_namespace() -> None:
  """"Test printing of namespace field."""
  expected_output = ("  Namespace: sample_namespace\n")
  assert feed_utility.get_namespace({"namespace": "sample_namespace"
                                    }) == expected_output
