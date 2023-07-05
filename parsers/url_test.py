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
"""Unit tests for url.py."""

from parsers import url

TEST_PROJECT = "test_prohject"
TEST_INSTANCE = "test_customer"
TEST_LOGTYPE = "test_log_type"
TEST_PARSER_ID = "test_parser_id"
TEST_AUGMENTATION_ID = "test_augmentation_id"


def test_get_url() -> None:
  """Test whether URL for parser commands are generated as expected."""
  # List/Download/Submit commands.
  assert url.get_url(
      region="us", command="list", environment="prod"
  ) == "https://backstory.googleapis.com/v1/tools/cbnParsers"
  assert url.get_url(
      region="europe", command="list", environment="prod"
  ) == "https://europe-backstory.googleapis.com/v1/tools/cbnParsers"
  assert url.get_url(
      region="asia-southeast1", command="list", environment="prod"
  ) == "https://asia-southeast1-backstory.googleapis.com/v1/tools/cbnParsers"
  assert url.get_url(
      region="us", command="list", environment="test"
  ) == "https://test-backstory.sandbox.googleapis.com/v1/tools/cbnParsers"

  # list_errors command.
  assert url.get_url(
      region="us",
      command="list_errors",
      environment="prod",
      log_type="test_log_type",
      start_time="2022-08-01T00:00:00Z",
      end_time="2022-08-01T11:00:00Z"
  ) == "https://backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserErrors?log_type=test_log_type&start_time=2022-08-01T00%3A00%3A00Z&end_time=2022-08-01T11%3A00%3A00Z"
  assert url.get_url(
      region="europe",
      command="list_errors",
      environment="prod",
      log_type="test_log_type",
      start_time="2022-08-01T00:00:00Z",
      end_time="2022-08-01T11:00:00Z"
  ) == "https://europe-backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserErrors?log_type=test_log_type&start_time=2022-08-01T00%3A00%3A00Z&end_time=2022-08-01T11%3A00%3A00Z"
  assert url.get_url(
      region="asia-southeast1",
      command="list_errors",
      environment="prod",
      log_type="test_log_type",
      start_time="2022-08-01T00:00:00Z",
      end_time="2022-08-01T11:00:00Z"
  ) == "https://asia-southeast1-backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserErrors?log_type=test_log_type&start_time=2022-08-01T00%3A00%3A00Z&end_time=2022-08-01T11%3A00%3A00Z"
  assert url.get_url(
      region="us",
      command="list_errors",
      environment="test",
      log_type="test_log_type",
      start_time="2022-08-01T00:00:00Z",
      end_time="2022-08-01T11:00:00Z"
  ) == "https://test-backstory.sandbox.googleapis.com/v1/tools/cbnParsers:listCbnParserErrors?log_type=test_log_type&start_time=2022-08-01T00%3A00%3A00Z&end_time=2022-08-01T11%3A00%3A00Z"

  # Run command.
  assert url.get_url(
      region="us", command="run", environment="prod"
  ) == "https://backstory.googleapis.com/v1/tools:validateCbnParser"
  assert url.get_url(
      region="europe", command="run", environment="prod"
  ) == "https://europe-backstory.googleapis.com/v1/tools:validateCbnParser"
  assert url.get_url(
      region="asia-southeast1", command="run", environment="prod"
  ) == "https://asia-southeast1-backstory.googleapis.com/v1/tools:validateCbnParser"
  assert url.get_url(
      region="us", command="run", environment="test"
  ) == "https://test-backstory.sandbox.googleapis.com/v1/tools:validateCbnParser"

  # History command.
  assert url.get_url(
      region="us",
      command="history",
      environment="prod",
      log_type="SAMPLE_LOGTYPE"
  ) == "https://backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserHistory?log_type=SAMPLE_LOGTYPE"
  assert url.get_url(
      region="europe",
      command="history",
      environment="prod",
      log_type="SAMPLE_LOGTYPE"
  ) == "https://europe-backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserHistory?log_type=SAMPLE_LOGTYPE"
  assert url.get_url(
      region="asia-southeast1",
      command="history",
      environment="prod",
      log_type="SAMPLE_LOGTYPE"
  ) == "https://asia-southeast1-backstory.googleapis.com/v1/tools/cbnParsers:listCbnParserHistory?log_type=SAMPLE_LOGTYPE"
  assert url.get_url(
      region="us",
      command="history",
      environment="test",
      log_type="SAMPLE_LOGTYPE"
  ) == "https://test-backstory.sandbox.googleapis.com/v1/tools/cbnParsers:listCbnParserHistory?log_type=SAMPLE_LOGTYPE"


def test_get_dataplane_url() -> None:
  """Test whether Dataplane URL for parser commands are generated as expected."""
  # List command.
  assert url.get_dataplane_url(
      region="us", command="list_parsers", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": "-",
      }
  ) == f"https://us-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/-/parsers"
  assert url.get_dataplane_url(
      region="eu", command="list_parsers", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "eu",
          "instance": TEST_INSTANCE,
          "log_type": "-",
      }
  ) == f"https://eu-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/eu/instances/{TEST_INSTANCE}/logTypes/-/parsers"
  assert url.get_dataplane_url(
      region="asia-southeast1", command="list_parsers", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "asia-southeast1",
          "instance": TEST_INSTANCE,
          "log_type": "-",
      }
  ) == f"https://asia-southeast1-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/asia-southeast1/instances/{TEST_INSTANCE}/logTypes/-/parsers"
  assert url.get_dataplane_url(
      region="europe-west2", command="list_parsers", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "europe-west2",
          "instance": TEST_INSTANCE,
          "log_type": "-",
      }
  ) == f"https://europe-west2-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/europe-west2/instances/{TEST_INSTANCE}/logTypes/-/parsers"
  assert url.get_dataplane_url(
      region="us", command="list_parsers", environment="test",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": "-",
      }
  ) == f"https://test-chronicle.sandbox.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/-/parsers"
  assert url.get_dataplane_url(
      region="us", command="list_extensions", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": "-",
      }
  ) == f"https://us-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/-/parserExtensions"
  assert url.get_dataplane_url(
      region="eu", command="list_extensions", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "eu",
          "instance": TEST_INSTANCE,
          "log_type": "-",
      }
  ) == f"https://eu-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/eu/instances/{TEST_INSTANCE}/logTypes/-/parserExtensions"
  assert url.get_dataplane_url(
      region="asia-southeast1", command="list_extensions", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "asia-southeast1",
          "instance": TEST_INSTANCE,
          "log_type": "-",
      }
  ) == f"https://asia-southeast1-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/asia-southeast1/instances/{TEST_INSTANCE}/logTypes/-/parserExtensions"
  assert url.get_dataplane_url(
      region="europe-west2", command="list_extensions", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "europe-west2",
          "instance": TEST_INSTANCE,
          "log_type": "-",
      }
  ) == f"https://europe-west2-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/europe-west2/instances/{TEST_INSTANCE}/logTypes/-/parserExtensions"
  assert url.get_dataplane_url(
      region="us", command="list_extensions", environment="test",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": "-",
      }
  ) == f"https://test-chronicle.sandbox.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/-/parserExtensions"

  # Submit command.
  assert url.get_dataplane_url(
      region="us", command="submit_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://us-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers"
  assert url.get_dataplane_url(
      region="eu", command="submit_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "eu",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://eu-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/eu/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers"
  assert url.get_dataplane_url(
      region="asia-southeast1", command="submit_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "asia-southeast1",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://asia-southeast1-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/asia-southeast1/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers"
  assert url.get_dataplane_url(
      region="europe-west2", command="submit_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "europe-west2",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://europe-west2-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/europe-west2/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers"
  assert url.get_dataplane_url(
      region="us", command="submit_parser", environment="test",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://test-chronicle.sandbox.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers"
  assert url.get_dataplane_url(
      region="us", command="submit_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://us-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions"
  assert url.get_dataplane_url(
      region="eu", command="submit_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "eu",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://eu-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/eu/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions"
  assert url.get_dataplane_url(
      region="asia-southeast1", command="submit_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "asia-southeast1",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://asia-southeast1-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/asia-southeast1/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions"
  assert url.get_dataplane_url(
      region="europe-west2", command="submit_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "europe-west2",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://europe-west2-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/europe-west2/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions"
  assert url.get_dataplane_url(
      region="us", command="submit_extension", environment="test",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://test-chronicle.sandbox.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions"

  # Get command.
  assert url.get_dataplane_url(
      region="us", command="get_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://us-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}"
  assert url.get_dataplane_url(
      region="eu", command="get_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "eu",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://eu-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/eu/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}"
  assert url.get_dataplane_url(
      region="asia-southeast1", command="get_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "asia-southeast1",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://asia-southeast1-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/asia-southeast1/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}"
  assert url.get_dataplane_url(
      region="europe-west2", command="get_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "europe-west2",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://europe-west2-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/europe-west2/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}"
  assert url.get_dataplane_url(
      region="us", command="get_parser", environment="test",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://test-chronicle.sandbox.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}"
  assert url.get_dataplane_url(
      region="us", command="get_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser_extension": TEST_AUGMENTATION_ID,
      }
  ) == f"https://us-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions/{TEST_AUGMENTATION_ID}"
  assert url.get_dataplane_url(
      region="eu", command="get_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "eu",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser_extension": TEST_AUGMENTATION_ID,
      }
  ) == f"https://eu-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/eu/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions/{TEST_AUGMENTATION_ID}"
  assert url.get_dataplane_url(
      region="asia-southeast1", command="get_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "asia-southeast1",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser_extension": TEST_AUGMENTATION_ID,
      }
  ) == f"https://asia-southeast1-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/asia-southeast1/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions/{TEST_AUGMENTATION_ID}"
  assert url.get_dataplane_url(
      region="europe-west2", command="get_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "europe-west2",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser_extension": TEST_AUGMENTATION_ID,
      }
  ) == f"https://europe-west2-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/europe-west2/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions/{TEST_AUGMENTATION_ID}"
  assert url.get_dataplane_url(
      region="us", command="get_extension", environment="test",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser_extension": TEST_AUGMENTATION_ID,
      }
  ) == f"https://test-chronicle.sandbox.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions/{TEST_AUGMENTATION_ID}"

  # Delete command.
  assert url.get_dataplane_url(
      region="us", command="delete_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://us-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}"
  assert url.get_dataplane_url(
      region="eu", command="delete_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "eu",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://eu-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/eu/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}"
  assert url.get_dataplane_url(
      region="asia-southeast1", command="delete_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "asia-southeast1",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://asia-southeast1-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/asia-southeast1/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}"
  assert url.get_dataplane_url(
      region="europe-west2", command="delete_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "europe-west2",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://europe-west2-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/europe-west2/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}"
  assert url.get_dataplane_url(
      region="us", command="delete_parser", environment="test",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://test-chronicle.sandbox.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}"
  assert url.get_dataplane_url(
      region="us", command="delete_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser_extension": TEST_AUGMENTATION_ID,
      }
  ) == f"https://us-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions/{TEST_AUGMENTATION_ID}"
  assert url.get_dataplane_url(
      region="eu", command="delete_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "eu",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser_extension": TEST_AUGMENTATION_ID,
      }
  ) == f"https://eu-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/eu/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions/{TEST_AUGMENTATION_ID}"
  assert url.get_dataplane_url(
      region="asia-southeast1", command="delete_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "asia-southeast1",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser_extension": TEST_AUGMENTATION_ID,
      }
  ) == f"https://asia-southeast1-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/asia-southeast1/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions/{TEST_AUGMENTATION_ID}"
  assert url.get_dataplane_url(
      region="europe-west2", command="delete_extension", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "europe-west2",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser_extension": TEST_AUGMENTATION_ID,
      }
  ) == f"https://europe-west2-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/europe-west2/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions/{TEST_AUGMENTATION_ID}"
  assert url.get_dataplane_url(
      region="us", command="delete_extension", environment="test",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser_extension": TEST_AUGMENTATION_ID,
      }
  ) == f"https://test-chronicle.sandbox.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parserExtensions/{TEST_AUGMENTATION_ID}"

  # Activate parser
  assert url.get_dataplane_url(
      region="us", command="activate_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://us-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}:activate"
  assert url.get_dataplane_url(
      region="eu", command="activate_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "eu",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://eu-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/eu/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}:activate"
  assert url.get_dataplane_url(
      region="asia-southeast1", command="activate_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "asia-southeast1",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://asia-southeast1-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/asia-southeast1/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}:activate"
  assert url.get_dataplane_url(
      region="europe-west2", command="activate_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "europe-west2",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://europe-west2-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/europe-west2/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}:activate"
  assert url.get_dataplane_url(
      region="us", command="activate_parser", environment="test",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://test-chronicle.sandbox.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}:activate"

  # Deactivate parser
  assert url.get_dataplane_url(
      region="us", command="deactivate_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://us-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}:deactivate"
  assert url.get_dataplane_url(
      region="eu", command="deactivate_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "eu",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://eu-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/eu/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}:deactivate"
  assert url.get_dataplane_url(
      region="asia-southeast1", command="deactivate_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "asia-southeast1",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://asia-southeast1-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/asia-southeast1/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}:deactivate"
  assert url.get_dataplane_url(
      region="europe-west2", command="deactivate_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "europe-west2",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://europe-west2-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/europe-west2/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}:deactivate"
  assert url.get_dataplane_url(
      region="us", command="deactivate_parser", environment="test",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
          "parser": TEST_PARSER_ID,
      }
  ) == f"https://test-chronicle.sandbox.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}/parsers/{TEST_PARSER_ID}:deactivate"

  # Run parser
  assert url.get_dataplane_url(
      region="us", command="run_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://us-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}:runParser"
  assert url.get_dataplane_url(
      region="eu", command="run_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "eu",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://eu-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/eu/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}:runParser"
  assert url.get_dataplane_url(
      region="asia-southeast1", command="run_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "asia-southeast1",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://asia-southeast1-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/asia-southeast1/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}:runParser"
  assert url.get_dataplane_url(
      region="europe-west2", command="run_parser", environment="prod",
      resources={
          "project": TEST_PROJECT,
          "location": "europe-west2",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://europe-west2-chronicle.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/europe-west2/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}:runParser"
  assert url.get_dataplane_url(
      region="us", command="run_parser", environment="test",
      resources={
          "project": TEST_PROJECT,
          "location": "us",
          "instance": TEST_INSTANCE,
          "log_type": TEST_LOGTYPE,
      }
  ) == f"https://test-chronicle.sandbox.googleapis.com/v1alpha/projects/{TEST_PROJECT}/locations/us/instances/{TEST_INSTANCE}/logTypes/{TEST_LOGTYPE}:runParser"
