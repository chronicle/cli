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
"""Utility for file related operations."""
import csv
import json
import os
from typing import Any, AnyStr, Dict, List

FILE_FORMAT_CSV = "CSV"
FILE_FORMAT_JSON = "JSON"
FILE_FORMAT_TXT = "TXT"


def read_file(file_path: str) -> bytes:
  """Read file and return its content.

  Args:
    file_path: Path of file

  Returns:
    File Content
  """
  with open(file_path, "rb") as file:
    return file.read()


def remove_file(file_path: str) -> None:
  """Removes the file if the path exists.

  Args:
    file_path (str): Path of the file to be removed.
  """
  if os.path.exists(file_path):
    os.remove(file_path)


def export_json(file_path: AnyStr, json_data: Dict[str, Any]) -> None:
  """Write JSON data into file.

  Args:
    file_path (AnyStr): Path of file to export output of command.
    json_data (Dict): JSON data.
  """
  with open(file_path, "w") as file:
    file.write(json.dumps(json_data, indent=2))


def export_csv(export_path: AnyStr, column_headers: List[str],
               rows: List[List[str]]) -> None:
  """Writes list of rows into csv file.

  Args:
    export_path (AnyStr): Path of file to export output of list command.
    column_headers (List[str]): List of all column name.
    rows (List[List[str]]): Array with row values.
  """
  with open(export_path, "w") as file:
    file_writer = csv.writer(file, delimiter=",")
    file_writer.writerow(column_headers)
    file_writer.writerows(rows)


def export_txt(file_path: AnyStr, data: str) -> None:
  """Write text data into file.

  Args:
    file_path (AnyStr): Path of file to export output of command.
    data (str): Text data.
  """
  with open(file_path, "w") as file:
    file.write(data)
