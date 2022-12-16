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
"""Unit tests for forwarders.py."""

from click.testing import CliRunner

from forwarders.forwarders import forwarders

runner = CliRunner()


def test_forwarders() -> None:
  """Test case for forwarders."""
  result = runner.invoke(forwarders)
  expected_output = """Commands:
  collectors     Collector Management Workflows
  create         Create a Forwarder
  delete         Delete a forwarder using Forwarder ID
  generate_file  Generate forwarder configuration using Forwarder ID
  get            Get forwarder details using Forwarder ID
  list           List all forwarders
  update         Update a forwarder using Forwarder ID"""
  assert expected_output in result.output
