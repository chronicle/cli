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
"""Starting point for the Chronicle CLI."""

import os
import subprocess

import click
from click._compat import WIN

from common import chronicle_auth
from feeds.feeds import feeds
from forwarders.forwarders import forwarders
from parsers.parsers import parsers
from tools.bigquery import bigquery


@click.group(
    name="cli",
    context_settings=dict(help_option_names=["-h", "--help"]),
    help="Chronicle CLI is a CLI tool for managing Chronicle user workflows for e.g. Feed Management workflows."
)
def cli() -> None:
  """Chronicle CLI commands."""
  if not os.path.exists(chronicle_auth.CHRONICLE_CLI_ROOT_DIR):
    click.echo(
        "'~/.chronicle_cli' directory is not present.\nCreating directory...")
    os.mkdir(chronicle_auth.CHRONICLE_CLI_ROOT_DIR)
    if WIN:
      subprocess.call(["attrib", "+H", chronicle_auth.CHRONICLE_CLI_ROOT_DIR])
    click.echo(
        f"Directory '{chronicle_auth.CHRONICLE_CLI_ROOT_DIR}' created successfully."
    )


cli.add_command(feeds)
cli.add_command(forwarders)
cli.add_command(parsers)
cli.add_command(bigquery)

if __name__ == "__main__":
  cli()
