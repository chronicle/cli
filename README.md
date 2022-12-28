# Chronicle CLI

Command line tool to interact with Chronicle's APIs.

Chronicle CLI allows customers to manage various operations that can be
performed on Chronicle. This script provides a command line tool to interact
with Feed, Parser, Forwarder and BigQuery APIs. It will gradually expand to
cover other APIs.

## Setup

Follow these instructions: https://cloud.google.com/python/setup

You may skip installing the Cloud Client Libraries and the Cloud SDK, they are
unnecessary for interacting with Chronicle.

After creating and activating the virtual environment `venv`, clone the repository using following command:

```shell
git clone https://github.com/chronicle/cli.git
```

After cloning, switch directory to `cli` and install Python library dependencies by running this command:

```shell
cd cli
pip install -r requirements.txt
```

It is assumed that you're using Python 3.7 or above.

### Setting up a Python development environment

https://cloud.google.com/python/docs/setup

Go to root directory and execute following command:\
```shell
python3 -m pip install --editable .
```

## Credentials

Running the samples requires a JSON credentials file. By default, all the
samples try to use the file `.chronicle_credentials.json` from inside a hidden
directory `.chronicle_cli` in the user's home directory. If this file is not
found, you need to specify it explicitly by adding the following argument to the
sample's command-line:

```shell
--credential_file <path>
```

## Run the chronicle_cli

```shell
chronicle_cli --help
```

## Unit test case execution

Execute the following command from root directory:\
```shell
python3 -m pytest --cov=./ --cov-report term-missing -vv
```


## Documentation

https://cloud.google.com/chronicle/docs/preview/cli-user-guide/cli-user-guide
