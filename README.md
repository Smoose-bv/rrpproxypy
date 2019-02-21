# RRPproxypy

RRPproxypy is a Python interface to the RRPproxy HTTP API.

[![PyPI version](https://badge.fury.io/py/rrpproxypy.svg)](https://badge.fury.io/py/rrpproxypy)
[![Documentation Status](https://readthedocs.org/projects/rrpproxypy/badge/?version=latest)](https://rrpproxypy.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/Smoose-bv/rrpproxypy.svg?branch=master)](https://travis-ci.org/Smoose-bv/rrpproxypy)

## Usage

Create a RRPproxy interface with the credentials and use it to
call the API.

```python
import rrpproxypy

rrp = rrpproxypy.RRPproxy(
    'username',
    'password')
rrp.status_domain('example.com')
```

## Development

When doing development the development dependencies need to be installed.
They can be installed using Pipenv:

```sh
pipenv install --dev
```

## Running tests

To enforce some form of coding style the project is linted using flake8.
Run flake8 using Pipenv:

```sh
pipenv run flake8
```

Running the unittests is a bit more difficult. An account for RRPproxy is
required having access to their test environment (OTE).
The credentials need to be set using the environment variables `RRP_USERNAME`
and `RRP_PASSWORD` (using a `.env` file is possible).
The tests can then be ran using Pipenv:

```sh
pipenv run pytest
```
