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
"""Give permission to an email to view Big Query tables and run queries."""

from typing import AnyStr

import click

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import options
from common.constants import key_constants as common_constants
from common.constants import status
from tools import bigquery_templates
from tools import url
from tools.constants import key_constants as bigquery_constants


@click.command(
    name="provide_access",
    help="Give permission to an email to access Big Query.")
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@exception_handler.catch_exception()
def provide_access(credential_file: AnyStr, verbose: bool, region: str,
                   env: str) -> None:
  """Give permission to an email to access Big Query.

  Args:
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    env (str): Option for selection environment. Available options - prod, test.

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  email = click.prompt("Enter email", show_default=False, default="")

  if not email:
    click.echo("Email not provided. Please enter email.")
    return

  click.echo("Providing Bigquery access...")

  provide_access_url = url.get_url(region, "provide_bq_access", env)
  client = chronicle_auth.initialize_http_session(credential_file)
  method = "PATCH"
  data = {bigquery_constants.KEY_EMAIL_ID: email}
  response = client.request(
      method,
      provide_access_url,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS,
      data=data)

  parsed_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    error_response = bigquery_templates.errors_response_template.substitute(
        error_code=f"{response.status_code}",
        error_msg=f"{parsed_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    click.echo(error_response)
    return

  success_response = bigquery_templates.success_response_template.substitute(
      email=f"{parsed_response[bigquery_constants.KEY_EMAIL_ID]}")
  click.echo(success_response)

  if verbose:
    api_utility.print_request_details(provide_access_url, method, None,
                                      parsed_response)
