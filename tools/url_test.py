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

from tools import url


def test_get_url() -> None:
  """Test whether URL for big query commands are generated as expected."""
  # provide bigquery access commands.
  assert url.get_url(
      region="us", command="provide_bq_access", environment="prod"
  ) == "https://backstory.googleapis.com/v1/tools/bigqueryAccess:update"
  assert url.get_url(
      region="europe", command="provide_bq_access", environment="prod"
  ) == "https://europe-backstory.googleapis.com/v1/tools/bigqueryAccess:update"
  assert url.get_url(
      region="asia-southeast1", command="provide_bq_access", environment="prod"
  ) == "https://asia-southeast1-backstory.googleapis.com/v1/tools/bigqueryAccess:update"
  assert url.get_url(
      region="us", command="provide_bq_access", environment="test"
  ) == "https://test-backstory.sandbox.googleapis.com/v1/tools/bigqueryAccess:update"
  assert url.get_url(
      region="us",
      command="provide_bq_access",
      environment="prod",
      input="sample_test"
  ) == "https://backstory.googleapis.com/v1/tools/bigqueryAccess:update?input=sample_test"
