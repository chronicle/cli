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
"""Grouping Forwarders CLI commands."""

import os

import click

from common import chronicle_auth
from forwarders.collectors.collectors import collectors
from forwarders.commands import create
from forwarders.commands import delete
from forwarders.commands import generate_files
from forwarders.commands import get
from forwarders.commands import list  # pylint: disable=redefined-builtin
from forwarders.commands import update


@click.group(name="forwarders", help="Forwarder Management Workflows")
def forwarders() -> None:
  """Forwarders group commands."""
  forwarder_dir = os.path.join(chronicle_auth.CHRONICLE_CLI_ROOT_DIR,
                               "forwarders")
  if not os.path.exists(forwarder_dir):
    os.mkdir(forwarder_dir)


forwarders.add_command(collectors)
forwarders.add_command(get.get)
forwarders.add_command(list.list_command)
forwarders.add_command(create.create)
forwarders.add_command(update.update)
forwarders.add_command(delete.delete)
forwarders.add_command(generate_files.generate_files)
