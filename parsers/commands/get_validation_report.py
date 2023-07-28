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
"""Run a parser(with extension) against given logs."""

import click
import stringcase

from common import api_utility
from common import chronicle_auth
from common import exception_handler
from common import options
from common.constants import http_method
from common.constants import key_constants as common_constants
from common.constants import status
from parsers import parser_templates
from parsers import url
from parsers.constants import key_constants as parser_constants


@click.command(name="get_validation_report",
               help="[New]Get validation report for a parser/extension")
@click.option(
    "--parser_id",
    help="ID of the parser",
)
@click.option(
    "--parserextension_id",
    help="ID of the parserextension",
)
@click.argument("project_id", required=True, default="")
@click.argument("customer_id", required=True, default="")
@click.argument("log_type", required=True, default="")
@click.argument("validation_report_id", required=True, default="")
@options.env_option
@options.region_option
@options.verbose_option
@options.credential_file_option
@options.v2_option
@exception_handler.catch_exception()
def get_validation_report(
    v2: bool,
    credential_file: str,
    verbose: bool,
    region: str,
    env: str,
    project_id: str,
    customer_id: str,
    log_type: str,
    validation_report_id: str,
    parser_id: str,
    parserextension_id: str) -> None:
  """Get validation report for a parser/parserextension.

  Args:
    v2 (bool): Option for enabling v2 commands.
    credential_file (AnyStr): Path of Service Account JSON.
    verbose (bool): Option for printing verbose output to console.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    env (str): Option for selection environment. Available options - prod, test.
    project_id (str): The GCP Project ID.
    customer_id (str): The Customer ID.
    log_type (str): The Log Type.
    validation_report_id (str): The Validation Report ID.
    parser_id (str): The ID of the parser to get the validation report.
    parserextension_id (str): The ID of the parserextension to get the
      validation report.

  Raises:
    OSError: Failed to read the given file, e.g. not found, no read access
      (https://docs.python.org/library/exceptions.html#os-exceptions).
    ValueError: Invalid file contents.
    KeyError: Required key is not present in dictionary.
    TypeError: If response data is not JSON.
  """
  if not v2:
    click.echo("--v2 flag not provided. "
               "Please provide the flag to run the new commands")
    return

  if not project_id:
    click.echo("Project ID not provided. Please enter Project ID")
    return

  if not customer_id:
    click.echo("Customer ID not provided. Please enter Customer ID")
    return

  if not log_type:
    click.echo("Log Type not provided. Please enter Log Type")
    return

  if not validation_report_id:
    click.echo("Validation Report ID not provided. "
               "Please enter Validation Report ID")
    return

  if not parser_id and not parserextension_id:
    click.echo("Parser ID or ParserExtension ID not provided. "
               "Parser ID or ParserExtension ID not provided")
    return

  if parser_id and parserextension_id:
    click.echo("Parser ID and ParserExtension ID provided. "
               "Please enter Parser or ParserExtension ID")
    return

  message = command = ""
  if parser_id:
    message = "Parser"
    command = "get_parser_validation_report"
  elif parserextension_id:
    message = "ParserExtension"
    command = "get_parserextension_validation_report"

  click.echo(f"Fetching Validation report for {message}...")

  resources = {
      parser_constants.KEY_PROJECT: project_id,
      parser_constants.KEY_LOCATION: region.lower(),
      parser_constants.KEY_INSTANCE: customer_id,
      parser_constants.KEY_LOG_TYPE: log_type,
      parser_constants.KEY_VALIDATION_REPORT: validation_report_id,
  }
  if parser_id:
    resources[parser_constants.KEY_PARSER] = parser_id
  if parserextension_id:
    resources[parser_constants.KEY_PARSER_EXTENSION] = parserextension_id

  get_validation_report_url = url.get_dataplane_url(
      region,
      command,
      env,
      resources,
  )
  client = chronicle_auth.initialize_dataplane_http_session(credential_file)
  method = http_method.GET
  response = client.request(
      method,
      get_validation_report_url,
      timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parsed_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    click.echo(
        f"Error while fetching validation report for {message}.\n"
        f"Response Code: {response.status_code}\n"
        f"Error: "
        f"{parsed_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )
    return

  if parser_constants.KEY_NAME not in parsed_response:
    click.echo(f"No Validation report found for {message}.")
    return

  validation_report = ""

  try:
    verdict = parsed_response[parser_constants.KEY_VERDICT]

    # Handle validation stats
    stats = parsed_response.get(parser_constants.KEY_STATS, {})
    log_entry_count = stats.get(
        parser_constants.KEY_LOG_ENTRY_COUNT, "0")
    successfully_normalized_log_count = stats.get(
        parser_constants.KEY_SUCCESSFULLY_NORMALIZED_LOG_COUNT, "0")
    failed_log_count = stats.get(
        parser_constants.KEY_FAILED_LOG_COUNT, "0")
    invalid_log_count = stats.get(
        parser_constants.KEY_INVALID_LOG_COUNT, "0")
    on_error_count = stats.get(
        parser_constants.KEY_ON_ERROR_COUNT, "0")
    event_count = stats.get(parser_constants.KEY_EVENT_COUNT, "0")
    generic_event_count = stats.get(
        parser_constants.KEY_GENERIC_EVENT_COUNT, "0")
    max_parse_duration = stats.get(
        parser_constants.KEY_MAX_PARSE_DURATION, "0")
    avg_parse_duration = stats.get(
        parser_constants.KEY_AVG_PARSE_DURATION, "0")
    normalization_percentage = stats.get(
        parser_constants.KEY_NORMALIZATION_PERCENTAGE, "0")
    generic_event_percentage = stats.get(
        parser_constants.KEY_GENERIC_EVENT_PERCENTAGE, "0")

    # Handle event category count map
    event_category_counts = stats.get(
        parser_constants.KEY_EVENT_CATEGORY_COUNTS, {})
    event_category_counts_tmpl = "{key}: {value}"
    event_category_counts_str = ""
    for k, v in event_category_counts.items():
      event_category_counts_str += event_category_counts_tmpl.format(
          key=stringcase.capitalcase(k), value=v)
    if not event_category_counts_str:
      event_category_counts_str = "-"
    # Handle event category count map
    drop_tag_counts = stats.get(
        parser_constants.KEY_DROP_TAG_COUNTS, {})
    drop_tag_counts_tmpl = "{key}: {value}"
    drop_tag_counts_str = ""
    for k, v in drop_tag_counts.items():
      drop_tag_counts_str += drop_tag_counts_tmpl.format(
          key=stringcase.capitalcase(k), value=v)
    if not drop_tag_counts_str:
      drop_tag_counts_str = "-"

    # Handle error
    errors = "-"
    if parser_constants.KEY_ERROR in parsed_response:
      errors = list_parsing_errors(
          credential_file,
          region,
          env,
          project_id,
          customer_id,
          log_type,
          validation_report_id,
          parser_id,
          parserextension_id,
      )

    # Populate the validation report
    validation_report = parser_templates.validation_report_template.substitute(
        verdict=verdict,
        log_entry_count=log_entry_count,
        successfully_normalized_log_count=successfully_normalized_log_count,
        failed_log_count=failed_log_count,
        invalid_log_count=invalid_log_count,
        on_error_count=on_error_count,
        event_count=event_count,
        generic_event_count=generic_event_count,
        event_category_count=event_category_counts_str,
        drop_tag_count=drop_tag_counts_str,
        max_parse_duration=max_parse_duration,
        avg_parse_duration=avg_parse_duration,
        normalization_percentage=normalization_percentage,
        generic_event_percentage=generic_event_percentage,
        errors=errors,
    )
  except KeyError as e:
    validation_report += f"\nKey {str(e)} not found in the response."
  except Exception as e:  # pylint: disable=broad-except
    validation_report += f"\nFailed with exception: {str(e)}"

  click.echo(validation_report)

  if verbose:
    api_utility.print_request_details(
        get_validation_report_url, method, None, parsed_response)


def list_parsing_errors(
    credential_file: str,
    region: str,
    env: str,
    project_id: str,
    customer_id: str,
    log_type: str,
    validation_report_id: str,
    parser_id: str,
    parserextension_id: str) -> str:
  """Get validation report for a parser/parserextension.

  Args:
    credential_file (AnyStr): Path of Service Account JSON.
    region (str): Option for selecting regions. Available options - US, EUROPE,
      ASIA_SOUTHEAST1.
    env (str): Option for selection environment. Available options - prod, test.
    project_id (str): The GCP Project ID.
    customer_id (str): The Customer ID.
    log_type (str): The Log Type.
    validation_report_id (str): The Validation Report ID.
    parser_id (str): The ID of the parser to get the validation report.
    parserextension_id (str): The ID of the parserextension to get the
      validation report.

  Raises:
    KeyError: Required key is not present in dictionary.

  Returns:
    The parsing errors. The value is rendered using a template. For example:

    Log: sample log
    Error: sample error
  """
  message = command = ""
  if parser_id:
    message = "Parser"
    command = "list_parser_parsing_errors"
  elif parserextension_id:
    message = "ParserExtension"
    command = "list_parserextension_parsing_errors"

  resources = {
      parser_constants.KEY_PROJECT: project_id,
      parser_constants.KEY_LOCATION: region.lower(),
      parser_constants.KEY_INSTANCE: customer_id,
      parser_constants.KEY_LOG_TYPE: log_type,
      parser_constants.KEY_VALIDATION_REPORT: validation_report_id,
  }
  if parser_id:
    resources[parser_constants.KEY_PARSER] = parser_id
  if parserextension_id:
    resources[parser_constants.KEY_PARSER_EXTENSION] = parserextension_id

  list_parsing_errors_url = url.get_dataplane_url(
      region,
      command,
      env,
      resources,
  )

  client = chronicle_auth.initialize_dataplane_http_session(credential_file)
  method = "GET"
  response = client.request(method, list_parsing_errors_url,
                            timeout=url.HTTP_REQUEST_TIMEOUT_IN_SECS)
  parsed_response = api_utility.check_content_type(response.text)

  if response.status_code != status.STATUS_OK:
    raise ValueError(
        f"Error while fetching parsing errors for {message}.\n"
        f"Response Code: {response.status_code}\n"
        f"Error: "
        f"{parsed_response[common_constants.KEY_ERROR][common_constants.KEY_MESSAGE]}"
    )

  if parser_constants.KEY_PARSING_ERRORS not in parsed_response:
    return "-"

  errors = ""
  for parsing_error in parsed_response[parser_constants.KEY_PARSING_ERRORS]:
    log = parsing_error.get(parser_constants.KEY_LOG_DATA, "-")
    error = parsing_error[parser_constants.KEY_ERROR]
    errors += parser_templates.parsing_errors_details_template.substitute(
        log=log,
        error=error,
    )
  if not errors:
    return "-"

  return errors
