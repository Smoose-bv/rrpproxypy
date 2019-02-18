from urllib import parse
import configparser
import datetime
import re

import requests

from rrpproxypy import exceptions


def try_parse(value):
    """
    Try to parse the given value.

    Args:
        value (str): The value to parse.

    Returns:
        The parsed value.

    """
    try:
        return datetime.datetime.strptime(
            value,
            '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return value


class RRPproxy:
    def __init__(
            self,
            username,
            password,
            test=False):
        """
        Args:
            username (str): The RRP username.
            password (str): The RRP password.

        Keyword Args:
            test (bool): Whether or not to use the test environment.

        """
        if test:
            self.url = 'https://api-ote.rrpproxy.net/'
        else:
            self.url = 'https://api.rrpproxy.net/'
        self.username = username
        self.password = password

    def _response_to_dict(self, response):
        """
        Convert a response to a dict.

        Properties are automatically converted to lists whenever there are
        multiple indexes for the same property.

        Args:
            response (str): The response text.

        Returns:
            dict: The response as a dict.

        """
        # Cut off the EOF line.
        response = response[:response.find('EOF', -10)]
        parser = configparser.ConfigParser(
            interpolation=None)
        parser.read_string(response)
        response = dict(parser.items('RESPONSE'))
        for key in sorted(response):
            if key.startswith('property['):
                value = response.pop(key)
                name_end_index = key.find(']', 9)
                name = key[9:name_end_index]
                # XXX: The index in the response is ignored. If this somehow
                # matters some post processing of these properties needs to
                # occur. (Can't do it in-place as `sorted` is not a natural
                # sort.) Anyway, code to get the index is commented below.
                #
                # index_start_index = key.find('[', name_end_index) + 1
                # index_end_index = key.find(']', index_start_index)
                # index = int(key[index_start_index:index_end_index])
                properties = response.setdefault('properties', {})
                try:
                    properties[name].append(value)
                except KeyError:
                    properties[name] = value
                except AttributeError:
                    properties[name] = [properties[name], value]
        return response

    def domain_price(
            self,
            domain,
            **params):
        """
        Get the price for an action on a domain.

        Args:
            domain (str): The domain name.
            **params: Additional params.

        Returns:
            dict: The response.

        Raises:
            Failure: When the request has failed.

        Note:
            See the wiki for more info:
            https://wiki.rrpproxy.net/api/api-command/DomainPrice

        """
        response = self.request(
            'DomainPrice',
            domain=domain,
            **params
        )
        if int(response['code']) == 200:
            return response
        else:
            raise exceptions.Failure(response['description'])

    def get_zone_info(
            self,
            zone,
            **params):
        """
        Get information about a zone (TLD).

        Args:
            zone (str): The zone to query.
            **params: Additional params.

        Returns:
            dict: The response.

        Note:
            See the wiki for more info:
            https://wiki.rrpproxy.net/api/api-command/GetZoneInfo

        """
        response = self.request(
            'GetZoneInfo',
            zone=zone,
            **params)
        return response

    def query_domain_list(self):
        """
        Query a list of domains.

        Returns:
            A list of domains.

        """
        response = self.request(
            'QueryDomainList',
            orderby='DOMAINREGISTRATIONEXPIRATIONDATE',
            wide=1)
        return response

    def request(
            self,
            command,
            **args):
        """
        Perform a request.

        Args:
            command (str): The API command to call.

        Keyword Args:
            Additional arguments to the API call.

        Returns:
            The parsed response.

        """
        (scheme, netloc, path, params, query, fragment) = parse.urlparse(
            self.url)
        path = '/api/call'

        query = {
            's_login': self.username,
            's_pw': self.password,
            'command': command,
        }
        query.update(args)
        query = parse.urlencode(query)
        url = parse.urlunparse((
            scheme,
            netloc,
            path,
            params,
            query,
            fragment))
        response = requests.get(url)
        response = self._response_to_dict(response.text)
        return response

    def status_domain(self, domain):
        """
        Request the domain status.

        Args:
            domain (str): The domain name to request the status for.

        Returns:
            dict: The domain.

        """
        response = self.request(
            'StatusDomain',
            domain=domain)
        return response
