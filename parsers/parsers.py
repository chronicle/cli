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

from parsers.commands import archive
from parsers.commands import download
from parsers.commands import generate
from parsers.commands import history
from parsers.commands import list  # pylint: disable=redefined-builtin
from parsers.commands import list_errors
from parsers.commands import run
from parsers.commands import status
from parsers.commands import submit


@click.group(name="parsers", help="Manage config based parsers")
def parsers() -> None:
  """Group of commands to interact with Parser APIs."""


parsers.add_command(archive.archive)
parsers.add_command(download.download)
parsers.add_command(generate.generate)
parsers.add_command(history.history)
parsers.add_command(list.list_command)
parsers.add_command(list_errors.list_errors)
parsers.add_command(run.run)
parsers.add_command(status.status_command)
parsers.add_command(submit.submit)
