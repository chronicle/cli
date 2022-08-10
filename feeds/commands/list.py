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
"""List feeds."""

import os
from typing import AnyStr

import click

from common import exception_handler
from common import uri
from feeds import feed_schema_utility
from feeds import feed_templates
from feeds import feed_utility
from feeds.constants import schema
from feeds.constants import status


@click.command(name="list", help="List all feeds")
@uri.url_option
@uri.region_option
@click.option("--export", help="Export output to specified file path")
@click.option(
    "--file-format",
    type=click.Choice(["TXT", "CSV", "JSON"], case_sensitive=False),
    default="CSV",
    help="Format of the file to be exported")
@feed_utility.verbose_option
@feed_utility.credential_file_option
@exception_handler.catch_exception()
def list_command(credential_file: AnyStr, verbose: bool, file_format: AnyStr,
                 export: AnyStr, region: str, url: str) -> None:
  """List all feeds.

  Args:
    credential_file (AnyStr): Path of Service Account JSON
    verbose (bool): Option for printing verbose output to console.
    file_format (AnyStr): Format of the content to be exported
    export (AnyStr): Path of file to export output of list command
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1
    url (str): Base URL to be used for API calls

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  url = feed_utility.lower_or_none(url)
  list_feed_errors = []
  feed_schema = feed_schema_utility.FeedSchema(credential_file, region, url)
  full_url = feed_utility.get_feed_url(region, url)
  method = "GET"
  list_feeds_response = feed_schema.client.request(method, full_url)
  status_code = list_feeds_response.status_code
  feeds_response = feed_utility.check_content_type(list_feeds_response.text)

  if status_code != status.STATUS_OK:
    error_message = feeds_response[schema.KEY_ERROR][schema.KEY_MESSAGE]
    click.echo(
        f"\nError while fetching list of feeds.\nResponse Code: {status_code}"
        f"\nError: {error_message}")
    return

  if not feeds_response:
    click.echo("No feeds found.")
    return

  feed_rows = []

  feeds = feeds_response[schema.KEY_FEEDS]
  for feed in feeds:
    try:
      detail_schema = feed_schema.get_detailed_schema(
          feed[schema.KEY_DETAILS][schema.KEY_FEED_SOURCE_TYPE],
          feed[schema.KEY_DETAILS][schema.KEY_LOG_TYPE])
      if detail_schema.error:
        list_feed_errors.append({
            "name": feed[schema.KEY_NAME][6:],
            "error": detail_schema.error
        })
        continue

      flattened_response = feed_utility.flatten_dict(feed)
      field_response = feed_utility.get_feed_details(
          flattened_response, detail_schema.log_type_schema)

      feed_template_str = feed_templates.feed_template.substitute(
          # To fetch the id, we are trimming feeds/prefix here.
          feed_id=f"{feed[schema.KEY_NAME][6:]}",
          source_type=f"{detail_schema.display_source_type}",
          log_type=f"{detail_schema.log_type_schema[schema.KEY_DISPLAY_NAME]}",
          feed_state=f"{feed[schema.KEY_FEED_STATE]}",
          feed_details=f"{field_response}")

      if export:
        feed_rows.append([
            feed[schema.KEY_NAME][6:], detail_schema.display_source_type,
            detail_schema.log_type_schema[schema.KEY_DISPLAY_NAME],
            feed[schema.KEY_FEED_STATE],
            (field_response.replace("\n", "")[14:]).strip() if file_format
            == feed_utility.FEED_FILE_FORMAT_CSV else field_response
        ])
    except KeyError as e:
      list_feed_errors.append({
          "name": feed[schema.KEY_NAME][6:],
          "error": f"Key {str(e)} not found."
      })
      continue
    except Exception as e:  # pylint: disable=broad-except
      list_feed_errors.append({
          "name": feed[schema.KEY_NAME][6:],
          "error": f"Failed with exception: {str(e)}"
      })
      continue
    click.echo(feed_template_str)
    click.echo("=" * 60)

  if list_feed_errors:
    click.echo("\nFollowing Feed(s) failed with error:")
    for error_feed in list_feed_errors:
      click.echo(f"{error_feed['name']} - {error_feed['error']}")

  if export:
    export_path = os.path.abspath(export) + f".{file_format.lower()}"
    if file_format == feed_utility.FEED_FILE_FORMAT_CSV:
      feed_utility.export_csv(export_path, feed_rows)
    elif file_format == feed_utility.FEED_FILE_FORMAT_JSON:
      feed_utility.export_json(export_path, feeds)
    else:
      feed_utility.export_txt(export_path, feed_rows)
    click.echo(f"\nFeed list details exported successfully to: {export_path}")

  if verbose:
    feed_utility.print_request_details(full_url, method, None,
                                       feeds_response)
