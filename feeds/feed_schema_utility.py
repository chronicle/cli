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
"""Feed schema utility functions and classes."""

import dataclasses
import datetime
import getpass
import json
from typing import Any, AnyStr, Dict, List, Optional, Tuple

import click

from common import api_utility
from common import chronicle_auth
from common import uri
from common.constants import key_constants
from common.constants import status
from feeds import feed_utility
from feeds.constants import schema

API_VERSION = "v1"


@dataclasses.dataclass
class DetailedSchema:
  """Detailed schema dataclass."""
  display_source_type: Optional[str]
  log_type_schema: Optional[Dict[str, Any]]
  error: Optional[str]


class FeedSchema:
  """Class to fetch and process feed schema."""

  def __init__(self, credential_file_path: AnyStr, region: str,
               custom_url: AnyStr) -> None:
    """Fetch feed schema.

    Args:
      credential_file_path (str): Path of credential file.
      region (str): Region (US, EUROPE, ASIA_SOUTHEAST1).
      custom_url (str): Base URL to be used for API calls.
    """
    self.client = chronicle_auth.initialize_http_session(credential_file_path)
    self.current_time = datetime.datetime.utcnow()
    self.pre_body = {}
    self.region = region
    self.custom_url = custom_url
    self.schema_response = self.get_latest_schema()

  def get_latest_schema(self) -> Dict[str, Any]:
    """Get feed schema from API.

    Returns:
      Dict[str, str]: Feed schema response.

    Raises:
      Exception: Raised when status code is not 200.
    """
    feed_schema_response = self.client.request(
        "GET", get_feed_schema_url(self.region, self.custom_url))
    status_code = feed_schema_response.status_code
    response = api_utility.check_content_type(feed_schema_response.text)
    if status_code != status.STATUS_OK:
      error_message = response[key_constants.KEY_ERROR][
          key_constants.KEY_MESSAGE]
      raise Exception(error_message)
    return response

  def get_detailed_schema(self, user_source_type: AnyStr,
                          user_log_type: AnyStr) -> Any:
    """Get detailed schema for specific source and log type.

    Args:
      user_source_type (str): Source type.
      user_log_type (str): Log type.

    Returns:
      dataclass: Consists of -
        1. Display nane of Source type
        2. Schema of Log type
        3. Error message.
    """
    all_schema = self.schema_response[schema.KEY_FEED_SOURCE_TYPE_SCHEMAS]
    for source_type in all_schema:
      if user_source_type == source_type[schema.KEY_FEED_SOURCE_TYPE]:
        for logtype_schema in source_type[schema.KEY_LOG_TYPE_SCHEMAS]:
          if user_log_type == logtype_schema[key_constants.KEY_LOG_TYPE]:
            return DetailedSchema(source_type[schema.KEY_DISPLAY_NAME],
                                  logtype_schema, None)

    return DetailedSchema(None, None, "Schema Not Found.")

  def get_log_source_map(self) -> Dict[str, Any]:
    """Generate source type and log type mapping from feed schema.

    Returns:
      Dict: Map of source type and its display name and corresponding log
      types.
        Example)
        {
          'AMAZON_S3': {
              'displayName': 'Amazon S3',
              'logTypes': [('ONEPASSWORD', '1Password'),...]
            },
          'API': {
            'displayName': 'Third party API',
            'logTypes': [('ANOMALI_IOC', 'Anomali'),...]
            }
          ...
        }
    """
    source_log_mapping = {}
    response = self.schema_response[schema.KEY_FEED_SOURCE_TYPE_SCHEMAS]

    for source_type in response:
      if source_type[schema.KEY_DISPLAY_NAME] == "SFTP" or source_type.get(
          schema.KEY_READ_ONLY):
        continue
      source_log_mapping[source_type[schema.KEY_FEED_SOURCE_TYPE]] = {
          schema.KEY_DISPLAY_NAME: source_type[schema.KEY_DISPLAY_NAME]
      }

      log_types = []
      for each_log_type in source_type[schema.KEY_LOG_TYPE_SCHEMAS]:
        if not each_log_type.get(schema.KEY_READ_ONLY):
          log_types.append((each_log_type[key_constants.KEY_LOG_TYPE],
                            each_log_type[schema.KEY_DISPLAY_NAME]))

      source_log_mapping[source_type[schema.KEY_FEED_SOURCE_TYPE]][
          schema.KEY_LOG_TYPES] = log_types

    return source_log_mapping

  def process_input_detailed_schema(self, detailed_schema: List[Dict[str, Any]],
                                    flattened_response: Dict[str, Any]) -> None:
    """Prompt inputs for given schema and generate request body.

    Args:
      detailed_schema (List): List of schema dictionaries for fields
      flattened_response (Dict): Flattened response of existing feed.
    """
    for each in detailed_schema:
      enum_choices = []
      for each_choice in each.get(schema.KEY_ENUMFIELD_SCHEMAS, []):
        enum_choices.append((each_choice[schema.KEY_DISPLAY_NAME],
                             each_choice[schema.KEY_FIELD_VALUE]))

      existing_value = flattened_response.get(each[schema.KEY_FIELD_PATH], "")

      field_value = process_field_input(each, enum_choices, existing_value)
      self.pre_body.update({f"{each[schema.KEY_FIELD_PATH]}": field_value})

      # Add data entered by user for not existing field in flattened_response.
      # The data will be added only if the field is not the secret or password.
      if each[schema.KEY_FIELD_TYPE] not in [
          schema.STR_SECRET_FIELD_TYPE, schema.MULTILINE_SECRET_FIELD_TYPE
      ]:
        flattened_response[each[schema.KEY_FIELD_PATH]] = field_value

  def prepare_request_body(
      self,
      detailed_schema: Any,
      selected_source_type: AnyStr,
      selected_log_type: AnyStr,
      flattened_response: Dict[str, Any],
      feed_display_name: Optional[str] = None) -> Tuple[AnyStr, Dict[str, Any]]:
    """Prepare request body for create command.

    Args:
      detailed_schema: Feed schema for selected source and log type.
      selected_source_type (str): Source type.
      selected_log_type (str): Log type.
      flattened_response (Dict): Flattened response of existing feed.
      feed_display_name (str): Feed display name.

    Returns:
      AnyStr: Request body.
      flattened_response (Dict): Flattened response of existing feed.
    """
    schema_set_choices = []
    # Evaluating Feed Schema Alternative options.
    for each_alternative in detailed_schema.get(
        schema.KEY_DETAILS_FEED_SCHEMA_ALT, []):
      click.echo("\nChoose from following available options:")
      if each_alternative.get(schema.KEY_DETAILS_FEED_SCHEMA_SET):
        for option_num, each_schema_set in enumerate(
            each_alternative.get(schema.KEY_DETAILS_FEED_SCHEMA_SET, []),
            start=1):
          schema_set_choices.append(each_schema_set[schema.KEY_DISPLAY_NAME])
          click.echo(
              f"{option_num}. {each_schema_set[schema.KEY_DISPLAY_NAME]}")

        schema_set_index = int(
            click.prompt(
                "\nEnter your choice",
                type=click.types.IntRange(1, len(schema_set_choices)),
                show_default=False))

        detailed_schema_set = each_alternative.get(
            schema.KEY_DETAILS_FEED_SCHEMA_SET)[schema_set_index - 1]

        # Prompt for input fields according to option selected by user and
        # update request body.
        # For example: 'OAuth password grant' in Salesforce log type
        self.process_input_detailed_schema(
            detailed_schema_set[schema.KEY_DETAILED_FEED_SCHEMAS],
            flattened_response)

    # Prompt for other input fields and update request body.
    self.process_input_detailed_schema(
        detailed_schema[schema.KEY_DETAILED_FEED_SCHEMAS], flattened_response)

    self.process_namespace_input(flattened_response)
    self.process_labels_input(flattened_response)

    request_body = feed_utility.deflatten_dict(self.pre_body)

    request_body[schema.KEY_DETAILS].update({
        schema.KEY_FEED_SOURCE_TYPE: selected_source_type,
        key_constants.KEY_LOG_TYPE: selected_log_type,
    })
    request_body[schema.KEY_DISPLAY_NAME] = feed_display_name
    return json.dumps(request_body), flattened_response

  def process_namespace_input(self, flattened_response: Dict[str, Any]) -> None:
    """Prompt input for namespace field.

    Args:
      flattened_response (Dict): Flattened response of existing feed.
    """
    existing_value = flattened_response.get("details.namespace", "")

    namespace = click.prompt(
        "\nNamespace (The asset namespace to apply to "
        "all logs ingested through this feed.)",
        default=existing_value,
        show_default=bool(existing_value),
        prompt_suffix="\n=> ",
    )
    flattened_response[schema.KEY_DETAILS_NAMESPACE] = namespace
    self.pre_body[schema.KEY_DETAILS_NAMESPACE] = namespace

  def process_labels_input(self, flattened_response: Dict[str, Any]) -> None:
    """Prompt input for lables field.

    Args:
      flattened_response (Dict): Flattened response of existing feed.
    """
    click.echo("\nLabels (The ingestion metadata labels in 'key:value' format"
               " to apply to all logs ingested through this feed, "
               "as well as the resulting normalized data.)\n"
               "Enter/Paste your content. On a new line, press Ctrl-D (Linux)"
               " / Ctrl-Z (Windows) to save it:")

    contents = []
    while True:
      try:
        line = input()
      except EOFError:
        break
      contents.append(line)

    labels = []
    for kv in contents:
      key, value = kv.split(":")
      labels.append({"key": key, "value": value})
    flattened_response[schema.KEY_DETAILS_LABELS] = labels
    self.pre_body[schema.KEY_DETAILS_LABELS] = labels


def process_field_input(field: Dict[str, Any],
                        choices: List[Any],
                        existing_value: Optional[str] = None) -> Any:
  """Generate prompts according to field type.

  Args:
    field (Dict): Schema for each field.
    choices (List): Enum choices.
    existing_value (str): Existing value of field for update command.

  Returns:
    Field value for request body.
  """
  prompt_text = (f"\n{field[schema.KEY_DISPLAY_NAME]} "
                 f"({field[schema.KEY_DESCRIPTION]})")
  is_required_value = None if field.get("isRequired") else ""
  default_value = existing_value or is_required_value
  show_default_value = bool(existing_value)

  if field.get(schema.KEY_IS_REQUIRED):
    prompt_text = (f"\n(*) {field[schema.KEY_DISPLAY_NAME]} "
                   f"({field[schema.KEY_DESCRIPTION]})")

  if field.get(schema.KEY_FIELD_TYPE) == schema.ENUM_FIELD_TYPE:
    click.echo(f"{prompt_text}\nChoose:")
    for choice_index, choice in enumerate(choices):
      click.echo(f"{choice_index + 1}. {choice[0]}")

    selected_choice = click.prompt(
        "",
        prompt_suffix="\n=> ",
        show_default=show_default_value,
        type=click.types.IntRange(1, len(choices)),
        default=(None if field.get(schema.KEY_IS_REQUIRED) else 1))

    field_value = choices[selected_choice - 1][1]
    click.echo("\nYou have selected " +
               click.style(f"{choices[selected_choice - 1][0]}", bold=True))

  elif field[schema.KEY_FIELD_TYPE] == schema.STR_SECRET_FIELD_TYPE:
    field_value = click.prompt(
        prompt_text,
        show_default=show_default_value,
        default=default_value,
        prompt_suffix="\n=> ",
        hide_input=True)

  elif field.get(schema.KEY_FIELD_TYPE) in [
      schema.STR_MULTILINE_FIELD_TYPE, schema.MAP_STR_FIELD_TYPE,
      schema.MULTILINE_SECRET_FIELD_TYPE, schema.KV_LIST_FIELD_TYPE
  ]:
    click.echo(f"{prompt_text}\n"
               "Enter/Paste your content. On a new line, press Ctrl-D (Linux)"
               " / [Ctrl-Z + Enter] (Windows) to save it:")

    contents = []
    while True:
      try:
        if field.get(
            schema.KEY_FIELD_TYPE) == schema.MULTILINE_SECRET_FIELD_TYPE:
          line = getpass.getpass(prompt="")
        else:
          line = input()
      except EOFError:
        break
      contents.append(line)
    field_value = "\n".join(contents)

    if field.get(schema.KEY_FIELD_TYPE) == schema.KV_LIST_FIELD_TYPE:
      field_value = []
      for kv in contents:
        key, value = kv.split(":")
        field_value.append({"key": key, "value": value})
    elif field.get(schema.KEY_FIELD_TYPE) == schema.MAP_STR_FIELD_TYPE:
      field_value = {}
      for kv in contents:
        key, value = kv.split(":")
        field_value.update({key: value})

  elif field.get(schema.KEY_FIELD_TYPE) == schema.STR_LIST_FIELD_TYPE:
    field_value = click.prompt(
        prompt_text,
        show_default=show_default_value,
        default=default_value,
        prompt_suffix="\n=> ")

    field_value = field_value.split(",")

  elif field[schema.KEY_FIELD_TYPE] == schema.BOOL_FIELD_TYPE:
    field_value = click.confirm(
        prompt_text,
        default=default_value if default_value else False,
        prompt_suffix="\n=> ")

  else:
    field_value = click.prompt(
        prompt_text,
        default=default_value,
        prompt_suffix="\n=> ",
        show_default=show_default_value)

  return field_value


def get_feed_schema_url(region: str, custom_url: str) -> str:
  """Get feed schema URL according to selected region.

  Args:
    region (str): Region (US, EUROPE, ASIA_SOUTHEAST1).
    custom_url (str): Base URL to be used for API calls.

  Returns:
    str: Feed schema URL.
  """
  return uri.get_base_url(region, custom_url) + f"/{API_VERSION}/feedSchema"
