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
"""Schema utility functions and classes."""

import json
import os
from typing import Any, Dict, List, Optional

import click

from forwarders import forwarder_templates
from forwarders.constants import schema

SCHEMAS_DIR = "schemas"
FORWARDER_SCHEMA_FILE = "forwarder_schema.json"
COLLECTOR_SCHEMA_FILE = "collector_schema.json"


def format_display_name(display_name: str) -> str:
  """Returns string to be printed on console to show section names.

  Args:
    display_name: String to format. Example: 'Forwarder Metadata'

  Returns:
    str: Formatted display name. Example: '========== Forwarder Metadata
    =========='
  """
  len_display_name = ((40 - len(display_name)) // 2) - 1
  return f'{"="*len_display_name} {display_name} {"="*len_display_name}'


def get_default_value(field_schema: Dict[str, Any],
                      existing_value: Optional[str] = None) -> Any:
  """Gets default value.

  Args:
    field_schema (Dict[str, Any]): Schema for each field.
    existing_value (str): Existing value of field for backup and update.

  Returns:
    Default value.
  """
  # As per click library implementation, assign None when field is required and
  # "" in case when field in optional.
  required_value = None if field_schema.get(schema.KEY_IS_REQUIRED) else ""
  default_value = existing_value or field_schema.get(
      schema.KEY_DEFAULT_VALUE) or required_value
  return default_value


def process_field_input(field_schema: Dict[str, Any],
                        existing_value: Optional[str] = None) -> Any:
  """Generates prompts based on field type.

  Args:
    field_schema (Dict): Schema for each field.
    existing_value (str): Existing value of field for backup and update.

  Returns:
    Field value for request body.
  """
  prompt_text = f"\n{field_schema.get(schema.KEY_DISPLAY_NAME)}"
  description_text = field_schema.get(schema.KEY_DESCRIPTION)

  if field_schema.get(schema.KEY_IS_REQUIRED):
    prompt_text = f"\n(*) {field_schema.get(schema.KEY_DISPLAY_NAME)}"

  if description_text:
    prompt_text = f"{prompt_text} ({description_text})"

  default_value = get_default_value(field_schema, existing_value)

  show_default_value = True if field_schema.get(
      schema.KEY_DEFAULT_VALUE) or existing_value else False

  if field_schema.get(schema.KEY_FIELD_TYPE) == schema.INT_FIELD_TYPE:
    field_value = click.prompt(
        prompt_text,
        type=int,
        show_default=show_default_value,
        default=default_value if default_value else -1)

  elif field_schema.get(schema.KEY_FIELD_TYPE) == schema.BOOL_FIELD_TYPE:
    field_value = click.confirm(
        prompt_text,
        show_default=True,
        default=default_value if default_value else False)

  elif field_schema.get(schema.KEY_FIELD_TYPE) == schema.ENUM_FIELD_TYPE:
    enum_choices = []

    click.echo(f"{prompt_text}\nChoose:")

    for each_choice in field_schema.get(schema.KEY_ENUM_FIELD_SCHEMAS, []):
      enum_choices.append(
          (each_choice[schema.KEY_DISPLAY_NAME], each_choice[schema.KEY_VALUE]))
    for choice_index, choice in enumerate(enum_choices):
      click.echo(f"{choice_index + 1}. {choice[0]}")
      if default_value == choice[1]:
        default_value = choice_index + 1

    selected_choice = click.prompt(
        "",
        type=click.types.IntRange(1, len(enum_choices)),
        default=(default_value if default_value else None))
    field_value = enum_choices[selected_choice - 1][1]
    click.echo(
        "\nYou have selected " +
        click.style(f"{enum_choices[selected_choice - 1][0]}", bold=True))

  elif field_schema.get(schema.KEY_FIELD_TYPE) == schema.STR_SECRET_FIELD_TYPE:
    field_value = click.prompt(
        prompt_text,
        show_default=show_default_value,
        default=default_value,
        prompt_suffix="\n=> ",
        hide_input=True)
  else:
    field_value = click.prompt(
        prompt_text, show_default=show_default_value, default=default_value)
  return field_value


class Schema:
  """Class to get and process schema.

  Attributes:
    request_body: Format of the request body sent to the API with all necessary
      keys and values.
    schema_type: Type of schema forwarder or collector.
    backup_request_body: Request body of existing forwarder.
    schema: Forwarder or collector schema.
    repeated_message_fields: Repeated fields in schema.
  """

  def __init__(self, schema_type: str, backup_request_body: Dict[str, Any]):
    """Gets schema.

    Args:
      schema_type (str): Type of schema, i.e. forwarder or collector.
      backup_request_body (Dict): Request body of existing forwarder or
        collector.
    """
    self.schema_type = schema_type
    self.backup_request_body = backup_request_body
    self.schema = self.get_schema()
    self.repeated_message_fields = set()

  def get_schema(self) -> Dict[str, Any]:
    """Gets schema from json file.

    Returns:
      Detailed schema for respective schema type.
    """
    try:
      if self.schema_type == schema.KEY_FORWARDER_SCHEMA:
        file_path = os.path.join(
            os.path.dirname(__file__), SCHEMAS_DIR, FORWARDER_SCHEMA_FILE)
      elif self.schema_type == schema.KEY_COLLECTOR_SCHEMA:
        file_path = os.path.join(
            os.path.dirname(__file__), SCHEMAS_DIR, COLLECTOR_SCHEMA_FILE)

      # Read forwarder or collector schema from the specified file path.
      with open(file_path, "r") as f:
        detailed_schema = json.load(f)
    except FileNotFoundError as e:  # pylint: disable=broad-except
      click.echo("Failed with exception:" + str(e))

    return detailed_schema

  def validate_syslog_udp_settings(self, field_schema: Dict[str, Any],
                                   request_body) -> bool:
    """Validate syslog UDP settings to process input detailed schema.

    Args:
      field_schema ([Dict[str, Any]]): Input field schema.
      request_body (Dict[str, Any]): Request body sent to the API with all
        necessary keys and values.

    Returns:
      True if the field path is connection timeout or tls settings and the
      syslog protocol is UDP.
    """

    return request_body.get(
        schema.PROTOCOL_FIELD_PATH) == "UDP" and field_schema.get(
            schema.KEY_FIELD_PATH) in [
                schema.CONNECTION_TIMEOUT_FIELD_PATH,
                schema.TLS_SETTINGS_FIELD_PATH
            ]

  def process_labels_input(self,
                           existing_value: Optional[List[Dict[str, Any]]] = None
                          ) -> Any:
    """Prompt input for labels.

    Args:
      existing_value (List[Dict[str, Any]]): Existing value of labels for backup
        and update.

    Returns:
      List of labels entered by user in required key, value format.
    """
    click.echo("\nLabels (The ingestion metadata labels in 'key:value' format"
               " to apply to all logs ingested through this forwarder, "
               "as well as the resulting normalized data.)\n"
               "Enter/Paste your content. On a new line, press Ctrl-D (Linux)"
               " / [Ctrl-Z + Enter (Windows)] to save it:")

    if existing_value:
      display_labels = []
      for label in existing_value:
        display_labels.append({label["key"]: label["value"]})
      click.echo(display_labels)

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

    # Use existing labels if the user doesn't provide any.
    if not labels and existing_value:
      labels = existing_value

    return labels

  def process_oneof_input(self,
                          field_schema_dict: Dict[str, Any],
                          existing_value: Any = None) -> Any:
    """Process input for oneof field.

    Args:
      field_schema_dict (Dict[str, Any]): Oneof field schema.
      existing_value (Any): Existing value of field.

    Returns:
      Any: List of fields for selected settings.
    """
    click.echo(
        forwarder_templates.header_template.substitute(
            display_name=format_display_name(
                field_schema_dict.get(schema.KEY_DISPLAY_NAME))))

    oneof_choices = []
    existing_choice = None

    click.echo("\nChoose:")

    # List of tuples with field names and types.
    for index, each_choice in enumerate(
        field_schema_dict.get(schema.KEY_ONEOF_FIELD_SCHEMAS, [])):
      # Example - [("File Settings", "fileSettings")]
      oneof_choices.append((each_choice.get(schema.KEY_DISPLAY_NAME),
                            each_choice.get(schema.KEY_FIELD_TYPE)))
      # Check for existing oneof input.
      if existing_value and each_choice.get(
          schema.KEY_FIELD_PATH) in existing_value:
        existing_choice = index + 1

    # Display list of oneof fields.
    for choice_index, choice in enumerate(oneof_choices):
      click.echo(f"{choice_index + 1}. {choice[0]}")

    selected_choice = click.prompt(
        "",
        type=click.types.IntRange(1, len(oneof_choices)),
        default=existing_choice if existing_choice else None)

    setting_type = oneof_choices[selected_choice - 1][1]

    # List of settings fields based on the user's preference.
    list_settings = field_schema_dict.get(
        schema.KEY_ONEOF_FIELD_SCHEMAS)[selected_choice - 1].get(setting_type)

    # Field path based on the user's preference.
    selected_field_path = field_schema_dict.get(
        schema.KEY_ONEOF_FIELD_SCHEMAS)[selected_choice - 1].get(
            schema.KEY_FIELD_PATH)

    return list_settings, selected_field_path

  def validate_oneof_input(self, list_settings: List[Dict[str, Any]],
                           request_body: Any) -> bool:
    """Verify whether the user has set a field for one of the inputs.

    Args:
      list_settings: List of fields for selected settings.
      request_body: API request body.

    Returns:
      bool: Any field that is set returns true unless it is false.
    """
    for field_schema in list_settings:
      field_path = field_schema.get(schema.KEY_FIELD_PATH)

      # Checks if path is exist or not in request_body.
      if request_body.get(field_path):
        return True
    return False

  def prepare_request_body(self) -> Dict[str, Any]:
    """Prepare request body for create command.

    Returns:
      Dict[str, Any]: Request body.
    """
    request_body = {}
    if self.schema_type == schema.KEY_FORWARDER_SCHEMA:
      self.process_input_detailed_schema(
          self.schema.get(schema.KEY_FORWARDER_SCHEMA), request_body,
          self.backup_request_body)
    elif self.schema_type == schema.KEY_COLLECTOR_SCHEMA:
      self.process_input_detailed_schema(
          self.schema.get(schema.KEY_COLLECTOR_SCHEMA), request_body,
          self.backup_request_body)

    return request_body

  def process_input_detailed_schema(self,
                                    detailed_schema: List[Dict[str, Any]],
                                    request_body: Any,
                                    backup_request_body: Any,
                                    each_field_mask_path: str = "") -> None:
    """Prompt inputs for given schema and generate request body.

    Args:
      detailed_schema (LIST[DICT[str, Any]]): List of schema dictionaries for
        fields.
      request_body (Any): API request body.
      backup_request_body (Any): Request body of existing forwarder or
        collector.
      each_field_mask_path (str): String containing field path from parent field
        seperated by ".".
    """
    for each in detailed_schema:

      if self.validate_syslog_udp_settings(each, request_body):
        continue

      field_path = each.get(schema.KEY_FIELD_PATH)

      # Check for existing value of field in "backup_request_body".
      existing_value = backup_request_body[
          field_path] if backup_request_body and backup_request_body.get(
              field_path) else None

      # Check for existing value of oneof field in "backup_request_body".
      # Example - each = { "fieldPath": "settings", "type": "ONEOF",
      # "oneOfFieldSchemas": [{"fieldPath": "file_settings"},
      # {"fieldPath": "kafka_settings"}]},
      # backup_request_body = {"file_settings": {"file_path": "sample"}}.
      if each.get(schema.KEY_FIELD_TYPE
                 ) == schema.ONEOF_FIELD_TYPE and backup_request_body:
        for each_choice in each.get(schema.KEY_ONEOF_FIELD_SCHEMAS, []):
          # Check for existing oneof input.
          if each_choice.get(schema.KEY_FIELD_PATH, "") in backup_request_body:
            existing_value = {
                each_choice[schema.KEY_FIELD_PATH]:
                    backup_request_body[each_choice[schema.KEY_FIELD_PATH]]
            }

      self.process_each_field_type(each, request_body, existing_value,
                                   each_field_mask_path)

  def process_each_field_type(self, each: Dict[str, Any], request_body: Any,
                              existing_value: Any,
                              each_field_mask_path: str) -> None:
    """Prompt inputs for given schema and generate request body.

    Args:
      each (DICT[str, Any]): Dictionary of fields.
      request_body (Any): API request body.
      existing_value (Any): Existing value of feilds.
      each_field_mask_path (str): String containing field path from parent field
        seperated by ".".
    """
    # Processing user input for primitive types.
    if each.get(schema.KEY_FIELD_TYPE) in [
        schema.INT_FIELD_TYPE, schema.STRING_FIELD_TYPE, schema.ENUM_FIELD_TYPE,
        schema.BOOL_FIELD_TYPE, schema.STR_SECRET_FIELD_TYPE
    ]:
      field_value = process_field_input(each, existing_value)

      # In case if the type of field is integer and the user does not provide
      # the value,it would consider that field's value as -1.
      # In case if the type of field is boolean and its value is False,
      # the request body should be updated with the same.
      # Update the request body only when the field value is available,not equal
      # to -1 or if the type of field value is boolean as mentioned above.
      if (field_value and field_value != -1) or isinstance(field_value, bool):
        request_body.update({each[schema.KEY_FIELD_PATH]: field_value})

    # Processing label type input.
    elif each.get(schema.KEY_FIELD_TYPE) == schema.LABEL_FIELD_TYPE:
      click.echo(
          forwarder_templates.header_template.substitute(
              display_name=format_display_name(
                  each.get(schema.KEY_DISPLAY_NAME))))
      labels = self.process_labels_input(existing_value)
      if labels:
        request_body.update({each[schema.KEY_FIELD_PATH]: labels})

    # Processing oneof field type input.
    elif each.get(schema.KEY_FIELD_TYPE) == schema.ONEOF_FIELD_TYPE:
      list_settings, selected_field_path = self.process_oneof_input(
          each, existing_value)

      # Update each_field_mask_path based on the user's preference.
      # Example - selected_field_path = "file_settings",
      # each_field_mask_path = "config". Expected_output: "config.file_settings"
      each_field_mask_path = each_field_mask_path + "." + selected_field_path if each_field_mask_path else selected_field_path
      request_body.update({selected_field_path: {}})
      self.process_input_detailed_schema(
          list_settings, request_body[selected_field_path],
          existing_value.get(selected_field_path) if existing_value else None,
          each_field_mask_path)

      # Verify whether or not user have set any of the fields
      # for a certain setting.
      while not self.validate_oneof_input(list_settings,
                                          request_body[selected_field_path]):
        click.echo(
            click.style(
                f"\nYou haven't given any information regarding {schema.KEY_INGESTION_SETTINGS}.\nPlease set one of the settings to continue.",
                bold=True))
        self.process_input_detailed_schema(
            list_settings, request_body[selected_field_path],
            existing_value.get(selected_field_path) if existing_value else None,
            each_field_mask_path)

    # Processing repeated string field type input.
    elif each.get(schema.KEY_FIELD_TYPE) == schema.REPEATED_STRING_FIELD_TYPE:
      click.echo(
          click.style(
              f"\n[Enter list of values separated by comma]\nExisting value {existing_value}",
              bold=True))
      field_value = process_field_input(each)

      if field_value:
        values = field_value.split(",")
        field_value = [value.strip() for value in values]
      else:
        field_value = existing_value

      request_body.update({each[schema.KEY_FIELD_PATH]: field_value})
    else:
      # Prompt users whether they want to proceed configuring non-primitive
      # field types such as metadata, serverSettings etc.
      if each.get(schema.KEY_IS_REQUIRED):
        selected_choice = True
      else:
        selected_choice = click.confirm(
            "\nDo you want to proceed with"
            f" {each.get(schema.KEY_DISPLAY_NAME)}?")

      if selected_choice:
        click.echo(
            forwarder_templates.header_template.substitute(
                display_name=format_display_name(
                    each.get(schema.KEY_DISPLAY_NAME))))

        if each.get(schema.KEY_IS_REPEATED):
          request_body.update({each[schema.KEY_FIELD_PATH]: []})
          repeated_input = True
          index = 0
          while repeated_input:
            # (index < len(existing_value) will not check for existing values if
            # user had provided only that many values. If we don't keep this,
            # entering any additional repeated non-primitive value would throw
            # index error.
            self.populate_repeated_values(
                each, request_body, existing_value[index] if
                (existing_value is not None) and
                (index < len(existing_value)) else None, each_field_mask_path)
            index += 1
            repeated_input = click.confirm(
                f"\nDo you want to add more {each.get(schema.KEY_DISPLAY_NAME)}?"
            ) if each.get(schema.KEY_IS_REPEATED) else False
          each_field_mask_path = each_field_mask_path + "." + each.get(
              schema.KEY_FIELD_PATH) if each_field_mask_path else each.get(
                  schema.KEY_FIELD_PATH)

          # To prepare update mask for the update command, save current key in
          # "repeated_message_fields" attribute.
          self.repeated_message_fields.add(each_field_mask_path)
        else:
          each_field_mask_path = each_field_mask_path + "." + each.get(
              schema.KEY_FIELD_PATH) if each_field_mask_path else each.get(
                  schema.KEY_FIELD_PATH)
          request_body.update({each[schema.KEY_FIELD_PATH]: {}})
          self.process_input_detailed_schema(
              each.get(each.get(schema.KEY_FIELD_TYPE)),
              request_body[each[schema.KEY_FIELD_PATH]], existing_value,
              each_field_mask_path)

  def populate_repeated_values(self, each_field_schema, request_body,
                               existing_value, each_field_mask_path) -> None:
    """Iterate through non-primitive repeated fields and generate request body.

    Args:
      each_field_schema (DICT[str, Any]): Dictionary of fields. Example - {
        "type": "regex_filters", "regex_filters": [ { "fieldPath":
        "description", "type": "STRING" }, { "fieldPath": "regexp", "type":
        "STRING" } ] }.
      request_body: API request body. Example - {"regex_filters" : []}.
      existing_value: Existing value of feilds. {"description": "sample",
        "regexp": ".*"}.
      each_field_mask_path (str): String containing field path from parent field
        seperated by ".".
    """
    each_non_primitive_dict = {}
    for each in each_field_schema.get(
        each_field_schema.get(schema.KEY_FIELD_TYPE)):
      self.process_each_field_type(
          each, each_non_primitive_dict,
          existing_value.get(each[schema.KEY_FIELD_PATH])
          if existing_value else None, each_field_mask_path)
    request_body[each_field_schema[schema.KEY_FIELD_PATH]].append(
        each_non_primitive_dict)
