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
"""Grouping Collectors CLI commands."""

import os

import click

from common import chronicle_auth
from forwarders.collectors.commands import create
from forwarders.collectors.commands import delete
from forwarders.collectors.commands import get
from forwarders.collectors.commands import list  # pylint: disable=redefined-builtin
from forwarders.collectors.commands import update


@click.group(name="collectors", help="Collector Management Workflows")
def collectors() -> None:
  """Collectors group commands."""
  collector_dir = os.path.join(chronicle_auth.CHRONICLE_CLI_ROOT_DIR,
                               "collectors")
  if not os.path.exists(collector_dir):
    os.mkdir(collector_dir)


collectors.add_command(get.get)
collectors.add_command(list.list_command)
collectors.add_command(create.create)
collectors.add_command(update.update)
collectors.add_command(delete.delete)
