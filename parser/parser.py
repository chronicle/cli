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
"""Grouping Parser CLI commands."""

import click

from parser.commands import archive
from parser.commands import download
from parser.commands import generate
from parser.commands import history
from parser.commands import list  # pylint: disable=redefined-builtin
from parser.commands import list_errors
from parser.commands import run
from parser.commands import status
from parser.commands import submit


@click.group(name="parser", help="Manage config based parsers")
def parser() -> None:
  """Group of commands to interact with Parser APIs."""


parser.add_command(archive.archive)
parser.add_command(download.download)
parser.add_command(generate.generate)
parser.add_command(history.history)
parser.add_command(list.list_command)
parser.add_command(list_errors.list_errors)
parser.add_command(run.run)
parser.add_command(status.status_command)
parser.add_command(submit.submit)
