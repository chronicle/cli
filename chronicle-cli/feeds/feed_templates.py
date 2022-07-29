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

request_details_template = string.Template("""\
==========================================
========== HTTP Request Details ==========
==========================================
Request:
  URL: ${request_url}
  Method: ${method}
  Body: ${request_body}
Response:
  Body: ${response_body}
""")

feed_template = string.Template("""\

Feed Details:
  ID: ${feed_id}
  Source type: ${source_type}
  Log type: ${log_type}
  State: ${feed_state}
  ${feed_details}""")

properties_template = string.Template("""\
====================================
========== Set Properties ==========
====================================""")

log_type_template = string.Template("""\
List of Log types:

(i) How to select log type?
  - Press Up/b or Down/z keys to paginate.
  - To switch case-sensitivity, press '-i' and press enter. By default, search
    is case-sensitive.
  - To search for specific log type, press '/' key, enter text and press enter.
  - Note down the choice number for the log type that you want to select.
  - Press 'q' to quit and enter that choice number.
  - Press `h` for all the available options to navigate the list.
=============================================================================
""")

log_type_template_win = string.Template("""\
List of Log types:

(i) How to select log type?
  - Press ENTER key (scrolls one line at a time) or SPACEBAR key (display next screen).
  - Note down the choice number for the log type that you want to select.
  - Press 'q' to quit and enter that choice number.
=============================================================================
""")

input_parameters_template = string.Template("""\n\n\
======================================
=========== Input Parameters =========
======================================
(*) - Required fields.
Password/secret inputs are hidden.""")

retry_template = string.Template("""
Looks like there was a failed feed create/update attempt with source type: ${source_type} and log type: ${log_type}.
Would you like to retry?
""")
