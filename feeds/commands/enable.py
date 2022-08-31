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
"""Enable feed."""

from typing import AnyStr

import click

from common import api_utility
from common import exception_handler
from common import options
from common.constants import key_constants
from common.constants import status
from feeds import feed_schema_utility
from feeds import feed_utility


@click.command(help="Enable feed with a given feed id.")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def enable(credential_file: AnyStr, verbose: bool, region: str,
           url: AnyStr) -> None:
  """Enable feed using Feed ID.

  Args:
    credential_file (str): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    url (str): Base URL to be used for API calls.

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  url = feed_utility.lower_or_none(url)
  feed_schema = feed_schema_utility.FeedSchema(credential_file, region, url)
  feed_id = click.prompt("Enter Feed ID", default="", show_default=False)
  if not feed_id:
    click.echo("Feed ID not provided. Please enter Feed ID.")
    return

  full_url = f"{feed_utility.get_feed_url(region, url)}/{feed_id}:enable"
  method = "POST"
  enable_feed_response = feed_schema.client.request(method, full_url, {})
  response = api_utility.check_content_type(enable_feed_response.text)

  status_code = enable_feed_response.status_code

  if status_code == status.STATUS_OK:
    click.echo(f"Feed with ID: {feed_id} enabled successfully.")
  elif status_code == status.STATUS_NOT_FOUND:
    click.echo("Invalid Feed ID. Please enter valid Feed ID.")
  elif status_code == status.STATUS_BAD_REQUEST:
    click.echo("Feed does not exist.")
  else:
    click.echo(
        f"Error while enabling feed.\nResponse Code: {status_code}\nError: "
        f"{response[key_constants.KEY_ERROR][key_constants.KEY_MESSAGE]}")

  if verbose:
    api_utility.print_request_details(full_url, method, None, response)
