from urllib import parse
import datetime
import re

import requests


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

        Args:
            response (str): The response text.

        Returns:
            A list of response values.

        """
        results = {}
        columns = []
        pattern = r'^property\[([^]]+)\]\[(\d+)\]\s+=\s+?(.*)$'
        for match in re.finditer(pattern, response, re.MULTILINE):
            name = match.group(1)
            value = match.group(3)
            if name == 'column':
                columns.append(value)
                continue
            index = int(match.group(2))
            result = results.setdefault(index, {})
            result[name] = try_parse(value)
        if columns:
            for result in results.values():
                for key in list(result):
                    if key not in columns:
                        result.pop(key)
        return [
            results[key]
            for key in sorted(results.keys())]

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
        return response[0]
