import argparse
import os
from unittest import mock

import rrpproxypy

import pytest


@pytest.fixture
def parser():
    """
    An argument parser.

    """
    return argparse.ArgumentParser()


def test_username_arg(parser):
    """
    Test if the username can be set on the command line.

    """
    rrpproxypy.add_arguments(parser)
    args = parser.parse_args([
        '--rrpproxy-username',
        'username'])
    assert args.rrpproxy_username == 'username'


def test_username_arg_default(parser):
    """
    Test if the username can have a default value.

    """
    rrpproxypy.add_arguments(
        parser,
        default_username='username')
    args = parser.parse_args([])
    assert args.rrpproxy_username == 'username'


@mock.patch.dict(os.environ, {'RRPPROXY_USERNAME': 'username'})
def test_username_arg_from_env(parser):
    """
    Test if the username can be set from the environment.

    """
    rrpproxypy.add_arguments(
        parser)
    args = parser.parse_args([])
    assert args.rrpproxy_username == 'username'


def test_password_arg(parser):
    """
    Test if the password can be set on the command line.

    """
    rrpproxypy.add_arguments(parser)
    args = parser.parse_args([
        '--rrpproxy-password',
        'password'])
    assert args.rrpproxy_password == 'password'


def test_password_arg_default(parser):
    """
    Test if the password can have a default value.

    """
    rrpproxypy.add_arguments(
        parser,
        default_password='password')
    args = parser.parse_args([])
    assert args.rrpproxy_password == 'password'


@mock.patch.dict(os.environ, {'RRPPROXY_PASSWORD': 'password'})
def test_password_arg_from_env(parser):
    """
    Test if the password can be set from the environment.

    """
    rrpproxypy.add_arguments(
        parser)
    args = parser.parse_args([])
    assert args.rrpproxy_password == 'password'


def test_test_arg(parser):
    """
    Test if the test flag can be set on the command line.

    """
    rrpproxypy.add_arguments(parser)
    args = parser.parse_args([])
    assert args.rrpproxy_test is False
    args = parser.parse_args([
        '--rrpproxy-test'])
    assert args.rrpproxy_test is True
