# Chronicle CLI

## Preparing build

### Setting up a Python development environment

https://cloud.google.com/python/docs/setup

Go to root directory and execute following command:\
```python3 -m pip install --editable .```

### Run the chronicle_cli

```$ chronicle_cli --help```

## Unit test case execution

Execute the following command from root directory:\
```$ python3 -m pytest feeds/tests --cov=feeds/ --cov-report term-missing -vv```

### Documentation

Design Doc: go/chronicle-cli-design-doc

User Guide: go/chronicle-cli-user-guide
