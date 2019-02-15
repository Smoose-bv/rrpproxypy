import os

def add_arguments(
        parser,
        default_username=None,
        default_password=None):
    """
    Add RRP arguments to an argument parser.

    Command line arguments are added for the RRP username
    (`--rrpproxy-username`) and password (`--rrpproxy-password`).
    Both default to environment variables (`RRPPROXY_USERNAME` and
    `RRPPROXY_PASSWORD`). Another default can be supplied which serves
    as a fallback for the environment variables.

    Args:
        parser (ArgumentParser): The parser to add the arguments to.

    Keyword Args:
        default_username (str): The default RRP username.
        default_password (str): The default RRP password.

    """
    parser.add_argument(
        '--rrpproxy-username',
        default=os.environ.get('RRPPROXY_USERNAME', default_username),
        help='The RRPproxy username.')
    parser.add_argument(
        '--rrpproxy-password',
        default=os.environ.get('RRPPROXY_PASSWORD', default_password),
        help='The RRPproxy password.')
    parser.add_argument(
        '--rrpproxy-test',
        action='store_true',
        help='Use the RRP OTE (test environment).')
