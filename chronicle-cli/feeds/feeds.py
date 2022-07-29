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
"""Grouping Feed CLI commands."""

import os

import click

from common import chronicle_auth
from feeds.commands import create
from feeds.commands import delete
from feeds.commands import disable
from feeds.commands import enable
from feeds.commands import get
from feeds.commands import list  # pylint: disable=redefined-builtin
from feeds.commands import update


@click.group(name="feeds", help="Feed Management Workflows")
def feeds() -> None:
  """Feeds group commands."""
  feed_dir = os.path.join(chronicle_auth.CHRONICLE_CLI_ROOT_DIR, "feeds")
  if not os.path.exists(feed_dir):
    os.mkdir(feed_dir)


feeds.add_command(get.get)
feeds.add_command(list.list_command)
feeds.add_command(create.create)
feeds.add_command(update.update)
feeds.add_command(delete.delete)
feeds.add_command(enable.enable)
feeds.add_command(disable.disable)
