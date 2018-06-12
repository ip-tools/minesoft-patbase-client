# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas.motl@ip-tools.org>
#
# HTTP client for accessing the Minesoft PatBase REST API.
# See also: https://www.patbase.com/rest/
#
import attr
import json
import logging
import requests

from patbase.exceptions import PatBaseInvalidRequest, PatBaseLoginFailed, PatBaseQueryFailed

logger = logging.getLogger(__name__)


@attr.s
class PatBaseClientBase(object):

    def logout(self):
        # Signal unauthenticated state
        self.authenticated = False

    def ensure_login(self):
        if not self.authenticated:
            self.login()

    def process_response(self, response, on_empty='raise'):

        # Read response content
        payload = response.content

        # The server seems to send an UTF-8 byte order mark, compensate for that.
        # https://en.wikipedia.org/wiki/Byte_order_mark#UTF-8
        try:
            payload = payload.decode('utf-8-sig')
        except:
            pass

        # Sanity checks
        if payload == '' and on_empty == 'raise':
            raise PatBaseInvalidRequest('Empty response from PatBase API')

        # Decode JSON payload
        data = json.loads(payload)

        return data


@attr.s
class PatBaseClient(PatBaseClientBase):

    # The API credentials for authenticating with the service
    username = attr.ib()
    password = attr.ib()

    # The URL to the HTTP API endpoint
    url = attr.ib(default='https://www.patbase.com/rest/api.php')

    # The maximum number of results returned is 100,000
    query_max_results = attr.ib(default=100000)

    # Whether the client instance was able to authenticate properly
    authenticated = attr.ib(default=False)

    # Whether to enable/disable X.509 certificate verification when performing the TLS handshake
    tls_verify = attr.ib(default=True)

    # The HTTP client session instance from the "requests" module
    session = attr.ib(default=None)

    def login(self):

        # Signal unauthenticated state
        self.authenticated = False

        # Create HTTP session object which will keep track of cookies
        self.session = requests.Session()

        # Send request
        params = {'method': 'login', 'userid': self.username, 'password': self.password}
        response = self.session.get(self.url, params=params)

        # Read response
        data = self.process_response(response)

        # Check response
        if 'LOGIN_TO_API' in data and data['LOGIN_TO_API'] == 'OK':
            logger.info('PatBase API login succeeded with user "{}"'.format(self.username))
        else:
            raise PatBaseLoginFailed('PatBase API login failed, please check your credentials. The error was: {}'.format(data))

        # Signal authenticated state
        self.authenticated = True

    def query(self, expression):

        # Make sure we are authenticated with the API
        self.ensure_login()

        # Report what we will be doing
        logger.info('PatBase API query using expression "{}"'.format(expression))

        # Send request
        params = {'method': 'query', 'query': expression}
        response = self.session.get(self.url, params=params)

        # Read response
        data = self.process_response(response)

        # Check response
        if 'Results' in data and 'QueryKey' in data:
            outcome = PatBaseResult(expression=expression, result_count=data['Results'], query_key=data['QueryKey'])
            logger.info('PatBase API query succeeded with: {}'.format(outcome))
            return outcome
        else:
            raise PatBaseQueryFailed('PatBase API query failed, please check your expression. The error was: {}'.format(data))


@attr.s
class PatBaseResult(object):
    expression = attr.ib()
    result_count = attr.ib()
    query_key = attr.ib()
