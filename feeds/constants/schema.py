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
"""Feed schema constants to be used across the project."""

KEY_FEED_SOURCE_TYPE_SCHEMAS = "feedSourceTypeSchemas"
KEY_FEED_SOURCE_TYPE = "feedSourceType"
KEY_LOG_TYPE_SCHEMAS = "logTypeSchemas"
KEY_LOG_TYPE_SCHEMA = "log_type_schema"
KEY_LOG_TYPES = "logTypes"
KEY_NAME = "name"
KEY_DISPLAY_NAME = "displayName"
KEY_DETAILED_FEED_SCHEMAS = "detailsFieldSchemas"
KEY_ENUMFIELD_SCHEMAS = "enumFieldSchemas"
KEY_FIELD_PATH = "fieldPath"
KEY_STATUS = "status"
KEY_FIELD_VALUE = "value"
KEY_DETAILS = "details"
KEY_FEED_STATE = "feedState"
KEY_FEEDS = "feeds"
KEY_DESCRIPTION = "description"
KEY_DISPLAY_SOURCE_TYPE = "display_source_type"
KEY_READ_ONLY = "readOnly"
KEY_IS_REQUIRED = "isRequired"
KEY_FIELD_TYPE = "type"
KEY_DETAILS_FEED_SCHEMA_ALT = "detailsFieldSchemaAlternatives"
KEY_DETAILS_FEED_SCHEMA_SET = "detailsFieldSchemaSets"
ENUM_FIELD_TYPE = "ENUM"
STR_SECRET_FIELD_TYPE = "STRING_SECRET"
STR_MULTILINE_FIELD_TYPE = "STRING_MULTILINE"
MAP_STR_FIELD_TYPE = "MAP_STRING_STRING"
MULTILINE_SECRET_FIELD_TYPE = "STRING_MULTILINE_SECRET"
KV_LIST_FIELD_TYPE = "KEY_VALUE_LIST"
STR_LIST_FIELD_TYPE = "STRING_LIST"
BOOL_FIELD_TYPE = "BOOL"
JSON_CONTENT_TYPE = "application/json"
KEY_CONTENT_TYPE = "content-type"
KEY_DISPLAY_LOG_TYPE = "display_log_type"
KEY_DETAILS_NAMESPACE = "details.namespace"
KEY_DETAILS_LABELS = "details.labels"
FEED_COLUMN_HEADER = [
    "ID", "Display Name", "Source type", "Log type", "State", "Feed Settings",
    "Namespace", "Labels"
]
