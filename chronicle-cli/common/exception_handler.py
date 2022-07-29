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
"""Exception Handling Utility."""

import functools
import click


def catch_exception(func=None):
  """Decorator to handle exceptions.

  Args:
    func: Original unwrapped function

  Returns:
    Result of calling function or prints exception in case of error.
  """
  if not func:
    return functools.partial(catch_exception)

  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    """Wrapper function.

    Args:
      *args: User defined arguments
      **kwargs: Keyword user defined arguments

    Returns:
      Output of calling the function
    """
    try:
      return func(*args, **kwargs)
    except KeyError as e:
      click.echo(f"Failed to find key {str(e)} in the response.")
    except Exception as e:  # pylint: disable=broad-except
      click.echo(f"Failed with exception: {str(e)}")

  return wrapper
