import os
from unittest import mock

import pytest

import rrpproxypy


@pytest.fixture(scope='module')
def username():
    """
    Username for the RRP client.

    """
    return os.environ['RRP_USERNAME']


@pytest.fixture(scope='module')
def password():
    """
    Password for the RRP client.

    """
    return os.environ['RRP_PASSWORD']


@pytest.fixture(scope='module')
def client(
        username,
        password):
    """
    Set up an RRPproxy client for testing.

    """
    client = rrpproxypy.RRPproxy(
        username=username,
        password=password,
        test=True)
    return client


def test_convert_currency(
        client):
    """
    Test the convert currency command.

    """
    response = client.convert_currency(
        100,
        'USD',
        'EUR')
    assert response == {
        'code': '200',
        'description': 'Command completed successfully',
        'properties': {
            'amount': '100',
            'converted amount': mock.ANY,
            'from': 'USD',
            'rate': mock.ANY,
            'to': 'EUR',
        },
        'queuetime': '0',
        'runtime': mock.ANY,
    }


def test_domain_price(
        client):
    """
    Test the domain price command.

    """
    response = client.domain_price(
        'example.com',
        type='ADDDOMAIN')
    assert response == {
        'code': '200',
        'description': 'Command completed successfully',
        'properties': {
            'annual': mock.ANY,
            'application': '0.0000',
            'currency': 'USD',
            'domain': 'example.com',
            'exchangerate': '',
            'nonrefundable': '0.0000',
            'period': '1',
            'periodtype': 'YEAR',
            'premium': '0',
            'price': mock.ANY,
            'restore': mock.ANY,
            'setup': '0.0000',
            'trade': '0.0000',
            'transfer': mock.ANY,
            'type': 'ADD',
            'usedprice': 'standard',
            'vat': '0.0000',
            'vatnonrefundable': '0.0000',
            'vatpercent': '0.00',
            'zone': 'com',
            'zonecurrency': ''},
        'queuetime': '0',
        'runtime': mock.ANY}


def test_get_zone_info(
        client):
    """
    Test the get zone info command.

    """
    response = client.get_zone_info(
        'com')
    assert response['properties']['zone'] == 'com'


def test_query_domain_list(
        client):
    """
    Test the query domain list command.

    """
    response = client.query_domain_list()
    assert response['properties']['column'] == [
        'domain',
        'domain idn',
        'roid',
        'domain created date',
        'domain created by',
        'domain updated date',
        'domain updated by',
        'domain registration expiration date',
        'domain renewal date',
        'domain zone',
        'renewalmode',
        'transfermode',
        'domaintags',
        'domaincomment',
    ]


def test_query_exchange_rates(
        client):
    """
    Test the query exchange rate command.

    """
    response = client.query_exchange_rates()
    assert response['properties']['currency from'] == ['EUR'] * len(
        response['properties']['currency from'])


def test_status_domain(
        client):
    """
    Test the status domain command.

    A domain is needed in order to test the command so one is fetched using
    StatusDomain. If no domains are registered this test will fail.

    """
    try:
        domain = client.query_domain_list()['properties']['domain'][0]
    except IndexError:
        pytest.xfail('Could not query a domain. No domains registered?')
    response = client.status_domain(
        domain)
    assert response == {
        'code': '200',
        'description': 'Command completed successfully',
        'properties': {
            'auth': mock.ANY,
            'created by': mock.ANY,
            'created date': mock.ANY,
            'domain': domain,
            'domain idn': domain,
            'paiduntil date': mock.ANY,
            'registrar': mock.ANY,
            'registration expiration date': mock.ANY,
            'renewal date': mock.ANY,
            'renewalmode': mock.ANY,
            'roid': mock.ANY,
            'status': mock.ANY,
            'transfer lock': mock.ANY,
            'transfermode': mock.ANY,
            'updated by': mock.ANY,
            'updated date': mock.ANY,
            'zone': mock.ANY,
        },
        'queuetime': '0',
        'runtime': mock.ANY,
    }
