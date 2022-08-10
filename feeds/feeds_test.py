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
"""Unit tests for feeds.py."""

from click.testing import CliRunner

from feeds.feeds import feeds


runner = CliRunner()


def test_feeds() -> None:
  """Test case for feeds."""
  result = runner.invoke(feeds)
  expected_output = """Commands:
  create   Create a feed
  delete   Delete a feed
  disable  Disable feed with a given feed id.
  enable   Enable feed with a given feed id.
  get      Get feed details using Feed ID
  list     List all feeds
  update   Update feed details using Feed ID"""
  assert expected_output in result.output
