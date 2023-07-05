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
"""Templates for printing output to console."""

import string

parser_details_template = string.Template("""\

Parser Details:
  Config ID: ${config_id}
  Log type: ${log_type}
  State: ${state}
  SHA256: ${sha256}
  Author: ${author}
  Submit Time: ${submit_time}
  State Last Changed Time: ${state_last_changed_time}
  Last Live Time: ${last_live_time}""")

errors_details_template = string.Template("""\

Error Details:
  Error ID: ${error_id}
  Config ID: ${config_id}
  Log type: ${log_type}
  Error Time: ${error_time}
  Error Category: ${category}
  Error Message: ${error_msg}
  ${logs}""")

submitted_parser_details_template = string.Template("""\

Submitted Parser Details:
  Config ID: ${config_id}
  Log type: ${log_type}
  State: ${state}
  SHA256: ${sha256}
  Author: ${author}
  Submit Time: ${submit_time}
  State Last Changed Time: ${state_last_changed_time}
  """)

parser_history_template = string.Template("""\

Parser History:
  Config ID: ${config_id}
  Log type: ${log_type}
  State: ${state}
  SHA256: ${sha256}
  Author: ${author}
  Submit Time: ${submit_time}
  State Last Changed Time: ${state_last_changed_time}\
${last_live_time}${validationErrors}""")

parserextension_details_template = string.Template("""\

ParserExtension Details:
  ParserExtension ID: ${parserextension_id}
  Log type: ${log_type}
  State: ${state}
  Validation Report ID: ${validation_report_id}
  Create Time: ${create_time}
  State Last Changed Time: ${state_last_changed_time}
  Last Live Time: ${last_live_time}""")

parserv2_details_template = string.Template("""\

Parser Details:
  Parser ID: ${parser_id}
  Log type: ${log_type}
  State: ${state}
  Type: ${type}
  Author: ${author}
  Validation Report ID: ${validation_report_id}
  Create Time: ${create_time}""")
