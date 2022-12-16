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

header_template = string.Template("""
========================================
${display_name}
========================================""")

preview_template = string.Template("""\
Preview changes:

  - Press Up/b or Down/z keys to paginate.
  - To switch case-sensitivity, press '-i' and press enter. By default, search
    is case-sensitive.
  - To search for specific field, press '/' key, enter text and press enter.
  - Press 'q' to quit and confirm preview changes.
  - Press `h` for all the available options to navigate the list.
=============================================================================
""")

preview_template_win = string.Template("""\
Preview changes:

  - Press ENTER key (scrolls one line at a time) or SPACEBAR key (display next screen).
  - Press 'q' to quit and confirm preview changes.
=============================================================================
""")

retry_template = string.Template("""
Looks like there was a failed create/update attempt for ${display_name}.
Would you like to retry?
""")
