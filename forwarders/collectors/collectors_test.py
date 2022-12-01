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
"""Unit tests for collectors.py."""

from click.testing import CliRunner

from forwarders.collectors.collectors import collectors

runner = CliRunner()


def test_collectors() -> None:
  """Test case for collectors."""
  result = runner.invoke(collectors)
  expected_output = """Commands:
  create  Create a collector
  delete  Delete a collector using collector ID.
  get     Get a collector using collector ID.
  list    List all collectors.
  update  Update a collector using collector ID."""
  assert  expected_output in result.output
