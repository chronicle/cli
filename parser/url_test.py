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
"""Unit tests for url.py."""

from parser import url


def test_get_url() -> None:
  """Test whether URL for parser commands are generated as expected."""
  # List/Download/Submit commands.
  assert url.get_url(
      region="us", command="list", environment="prod"
  ) == "https://backstory.googleapis.com/v1/tools/cbnParsers"
  assert url.get_url(
      region="europe", command="list", environment="prod"
  ) == "https://europe-backstory.googleapis.com/v1/tools/cbnParsers"
  assert url.get_url(
      region="asia-southeast1", command="list", environment="prod"
  ) == "https://asia-southeast1-backstory.googleapis.com/v1/tools/cbnParsers"
  assert url.get_url(
      region="us", command="list", environment="test"
  ) == "https://test-backstory.sandbox.googleapis.com/v1/tools/cbnParsers"

  # list_errors command.
  assert url.get_url(
      region="us",
      command="list_errors",
      environment="prod",
      log_type="test_log_type",
      start_time="2022-08-01T00:00:00Z",
      end_time="2022-08-01T11:00:00Z"
  ) == "https://backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserErrors?log_type=test_log_type&start_time=2022-08-01T00%3A00%3A00Z&end_time=2022-08-01T11%3A00%3A00Z"
  assert url.get_url(
      region="europe",
      command="list_errors",
      environment="prod",
      log_type="test_log_type",
      start_time="2022-08-01T00:00:00Z",
      end_time="2022-08-01T11:00:00Z"
  ) == "https://europe-backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserErrors?log_type=test_log_type&start_time=2022-08-01T00%3A00%3A00Z&end_time=2022-08-01T11%3A00%3A00Z"
  assert url.get_url(
      region="asia-southeast1",
      command="list_errors",
      environment="prod",
      log_type="test_log_type",
      start_time="2022-08-01T00:00:00Z",
      end_time="2022-08-01T11:00:00Z"
  ) == "https://asia-southeast1-backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserErrors?log_type=test_log_type&start_time=2022-08-01T00%3A00%3A00Z&end_time=2022-08-01T11%3A00%3A00Z"
  assert url.get_url(
      region="us",
      command="list_errors",
      environment="test",
      log_type="test_log_type",
      start_time="2022-08-01T00:00:00Z",
      end_time="2022-08-01T11:00:00Z"
  ) == "https://test-backstory.sandbox.googleapis.com/v1/tools/cbnParsers:listCbnParserErrors?log_type=test_log_type&start_time=2022-08-01T00%3A00%3A00Z&end_time=2022-08-01T11%3A00%3A00Z"

  # Run command.
  assert url.get_url(
      region="us", command="run", environment="prod"
  ) == "https://backstory.googleapis.com/v1/tools:validateCbnParser"
  assert url.get_url(
      region="europe", command="run", environment="prod"
  ) == "https://europe-backstory.googleapis.com/v1/tools:validateCbnParser"
  assert url.get_url(
      region="asia-southeast1", command="run", environment="prod"
  ) == "https://asia-southeast1-backstory.googleapis.com/v1/tools:validateCbnParser"
  assert url.get_url(
      region="us", command="run", environment="test"
  ) == "https://test-backstory.sandbox.googleapis.com/v1/tools:validateCbnParser"

  # History command.
  assert url.get_url(
      region="us",
      command="history",
      environment="prod",
      log_type="SAMPLE_LOGTYPE"
  ) == "https://backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserHistory?log_type=SAMPLE_LOGTYPE"
  assert url.get_url(
      region="europe",
      command="history",
      environment="prod",
      log_type="SAMPLE_LOGTYPE"
  ) == "https://europe-backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserHistory?log_type=SAMPLE_LOGTYPE"
  assert url.get_url(
      region="asia-southeast1",
      command="history",
      environment="prod",
      log_type="SAMPLE_LOGTYPE"
  ) == "https://asia-southeast1-backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserHistory?log_type=SAMPLE_LOGTYPE"
  assert url.get_url(
      region="us",
      command="history",
      environment="test",
      log_type="SAMPLE_LOGTYPE"
  ) == "https://test-backstory.sandbox.googleapis.com/v1/tools/cbnParsers:listCbnParserHistory?log_type=SAMPLE_LOGTYPE"
