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
"""Unit tests for main.py."""
from click.testing import CliRunner
from main import cli

runner = CliRunner()


def test_main() -> None:
  """Test case for main."""
  result = runner.invoke(cli)
  assert """Usage: cli [OPTIONS] COMMAND [ARGS]...

  Chronicle CLI is a CLI tool for managing Chronicle user workflows for e.g.
  Feed Management workflows.

Options:
  -h, --help  Show this message and exit.

Commands:
  feeds   Feed Management Workflows
  parser  Manage config based parsers
""" == result.output
