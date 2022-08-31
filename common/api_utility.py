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
"""Utility functions."""

import json
from typing import Any, AnyStr, Dict, Optional

import click

from common import templates


def check_content_type(api_response: AnyStr) -> Any:
  """Return JSON based content for the response data.

  Args:
    api_response (AnyStr): API response

  Returns:
    JSON: Response data.

  Raises:
    TypeError: If response data is not JSON.
  """
  try:
    return json.loads(api_response)
  except json.JSONDecodeError:
    raise TypeError("URL is not reachable.") from None


def print_request_details(url: AnyStr, method: AnyStr,
                          request_body: Optional[Dict[str, Any]],
                          response_body: Dict[str, Any]) -> None:
  """Prints HTTP request details to the console.

  Args:
    url (AnyStr): Request url
    method (AnyStr): Request method
    request_body (Optional[Dict[str,Any]]): Request body
    response_body (Dict[str,Any]): Response body
  """
  click.echo(
      templates.request_details_template.substitute(
          request_url=url,
          method=method,
          request_body=request_body,
          response_body=response_body,
      ))
