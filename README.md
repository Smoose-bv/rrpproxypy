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
