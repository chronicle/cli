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
"""Helper functions to access Chronicle APIs using OAuth 2.0."""

import os
import pathlib
from typing import AnyStr, Any

from google.auth.transport import requests
from google.oauth2 import service_account

CHRONICLE_CLI_ROOT_DIR = os.path.join(
    str(pathlib.Path.home()), ".chronicle_cli")
default_cred_file_path = os.path.join(CHRONICLE_CLI_ROOT_DIR,
                                      "chronicle_credentials.json")
AUTHORIZATION_SCOPES = ["https://www.googleapis.com/auth/chronicle-backstory"]


def initialize_http_session(credential_file_path: AnyStr) -> Any:
  """Initializes an authorized HTTP session, based on the given credential.

  Args:
    credential_file_path: Absolute or relative path to a JSON file containing
      private OAuth 2.0 credentials of a Google Cloud Platform service account.
      Default path is ".chronicle_credentials.json" in the .chronicle_cli
      directory inside user's home directory.

  Returns:
    HTTP session object to send authorized requests and receive responses.
  """
  credentials = service_account.Credentials.from_service_account_file(
      filename=os.path.abspath(credential_file_path or default_cred_file_path),
      scopes=AUTHORIZATION_SCOPES)
  return requests.AuthorizedSession(credentials)
