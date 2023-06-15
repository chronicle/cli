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
"""CLI options."""

import click

from common import chronicle_auth

REGION_LIST = [
    "US",
    "ASIA-SOUTHEAST1",
    "EUROPE",
    "EUROPE-WEST2",
    "AUSTRALIA-SOUTHEAST1",
]

verbose_option = click.option(
    "--verbose", is_flag=True, help="Prints verbose output to the console."
)

credential_file_option = click.option(
    "-c",
    "--credential_file",
    help=(
        "Path of Service Account JSON. Default:"
        f" {chronicle_auth.default_cred_file_path}"
    ),
)

region_option = click.option(
    "--region",
    type=click.Choice(
        REGION_LIST,
        case_sensitive=False,
    ),
    default="US",
    help="Select region",
)

url_option = click.option("--url", help="Base URL to be used for API calls")

env_option = click.option(
    "--env",
    type=click.Choice(["prod", "test"], case_sensitive=False),
    default="prod",
    help="""Optionally specify
                        the environment for API calls""",
)

export_option = click.option(
    "--export", help="Export output to specified file path"
)
