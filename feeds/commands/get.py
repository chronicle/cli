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
"""Get feed details."""

from typing import AnyStr

import click

from common import api_utility
from common import exception_handler
from common import options
from common.constants import key_constants
from common.constants import status
from feeds import feed_schema_utility
from feeds import feed_templates
from feeds import feed_utility
from feeds.constants import schema


@click.command(help="Get feed details using Feed ID")
@options.url_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def get(credential_file: AnyStr, verbose: bool, region: str,
        url: AnyStr) -> None:
  """Get feed details using Feed ID.

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

  full_url = f"{feed_utility.get_feed_url(region, url)}/{feed_id}"
  method = "GET"
  get_feed_response = feed_schema.client.request(method, full_url)
  response = api_utility.check_content_type(get_feed_response.text)

  status_code = get_feed_response.status_code

  if status_code == status.STATUS_OK:
    detail_schema = feed_schema.get_detailed_schema(
        response[schema.KEY_DETAILS][schema.KEY_FEED_SOURCE_TYPE],
        response[schema.KEY_DETAILS][key_constants.KEY_LOG_TYPE])
    if detail_schema.error:
      click.echo(detail_schema.error)
      return

    flattened_response = feed_utility.flatten_dict(response)
    field_response = feed_utility.get_feed_details(
        flattened_response, detail_schema.log_type_schema)
    namespace = feed_utility.get_namespace(response.get(schema.KEY_DETAILS, {}))
    labels = feed_utility.get_labels(response.get(schema.KEY_DETAILS, {}))
    click.echo(
        feed_templates.feed_template.substitute(
            feed_id=feed_id,
            source_type=detail_schema.display_source_type,
            log_type=detail_schema.log_type_schema[schema.KEY_DISPLAY_NAME],
            feed_state=response[schema.KEY_FEED_STATE],
            feed_details=field_response,
            namespace=namespace,
            labels=labels))

  elif status_code == status.STATUS_NOT_FOUND:
    click.echo("Invalid Feed ID. Please enter valid Feed ID.")
  elif status_code == status.STATUS_BAD_REQUEST:
    click.echo("Feed does not exist.")
  else:
    click.echo(
        f"Error while fetching feed.\nResponse Code: {status_code}\nError: "
        f"{response[key_constants.KEY_ERROR][key_constants.KEY_MESSAGE]}")

  if verbose:
    api_utility.print_request_details(full_url, method, None, response)
