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

from parsers.commands import activate_parser
from parsers.commands import archive
from parsers.commands import deactivate_parser
from parsers.commands import delete_extension
from parsers.commands import delete_parser
from parsers.commands import download
from parsers.commands import generate
from parsers.commands import get_extension
from parsers.commands import get_parser
from parsers.commands import get_validation_report
from parsers.commands import history
from parsers.commands import list  # pylint: disable=redefined-builtin
from parsers.commands import list_errors
from parsers.commands import list_extensions
from parsers.commands import list_parsers
from parsers.commands import run
from parsers.commands import run_parser
from parsers.commands import status
from parsers.commands import submit
from parsers.commands import submit_extension
from parsers.commands import submit_parser


@click.group(name="parsers", help="Manage config based parsers")
def parsers() -> None:
  """Group of commands to interact with Parser APIs."""


parsers.add_command(activate_parser.activate_parser)
parsers.add_command(archive.archive)
parsers.add_command(deactivate_parser.deactivate_parser)
parsers.add_command(delete_extension.delete_extension)
parsers.add_command(delete_parser.delete_parser)
parsers.add_command(download.download)
parsers.add_command(generate.generate)
parsers.add_command(get_extension.get_extension)
parsers.add_command(get_parser.get_parser)
parsers.add_command(get_validation_report.get_validation_report)
parsers.add_command(history.history)
parsers.add_command(list.list_command)
parsers.add_command(list_errors.list_errors)
parsers.add_command(list_parsers.list_parsers)
parsers.add_command(list_extensions.list_extensions)
parsers.add_command(run.run)
parsers.add_command(run_parser.run_parser)
parsers.add_command(status.status_command)
parsers.add_command(submit.submit)
parsers.add_command(submit_extension.submit_extension)
parsers.add_command(submit_parser.submit_parser)
