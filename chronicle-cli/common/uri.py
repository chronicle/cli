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
"""Helper functions to make Chronicle API URLs."""

import click

REGION_EUROPE = "europe"
REGION_ASIA_SOUTHEAST1 = "asia-southeast1"
BASE_URL = "https://backstory.googleapis.com/v1"
BASE_URL_EUROPE = "https://europe-backstory.googleapis.com/v1"
BASE_URL_ASIA_SOUTHEAST1 = "https://asia-southeast1-backstory.googleapis.com/v1"

region_option = click.option(
    "--region",
    type=click.Choice(["US", "ASIA-SOUTHEAST1", "EUROPE"],
                      case_sensitive=False),
    default="US",
    help="Select region")

url_option = click.option("--url", help="Base URL to be used for API calls")


def get_base_url(region: str, custom_url: str) -> str:
  """Get base URL according to selected region.

  Args:
    region (str): Region (US, EUROPE, ASIA_SOUTHEAST1)
    custom_url (str): Base URL to be used for API calls

  Returns:
    str: Base URL
  """
  if custom_url:
    return custom_url
  region = region.lower()
  if region == REGION_EUROPE:
    return BASE_URL_EUROPE
  if region == REGION_ASIA_SOUTHEAST1:
    return BASE_URL_ASIA_SOUTHEAST1
  return BASE_URL
