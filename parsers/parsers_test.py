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
"""Unit tests for parsers.py."""

from click.testing import CliRunner

from parsers.parsers import parsers


runner = CliRunner()


def test_parser() -> None:
  """Test case for parsers."""
  result = runner.invoke(parsers)
  expected_output = """Commands:
  archive      Archives a parser given the config ID.
  download     Download parser code given config ID or log type
  generate     Generate sample logs for a given log type
  history      History retrieves all parser submissions given a log type
  list         List all parsers of a given customer
  list_errors  List errors of a log type between specific timestamps
  run          Run the parser against given logs
  status       Get status of a submitted parser
  submit       Submit a new parser"""
  assert expected_output in result.output
