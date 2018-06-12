# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas.motl@ip-tools.org>
#
# HTTP client for accessing the Minesoft PatBase REST API.
# See also: https://www.patbase.com/rest/
#
import attr
import json
import maya
import logging
import requests

from patbase.exceptions import PatBaseRequestError, PatBaseLoginError, PatBaseQueryError, PatBaseResultError
from patbase.util import StopWatch

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
            raise PatBaseRequestError('Empty response from PatBase API')

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

        # Query parameters
        params = {'method': 'login', 'userid': self.username, 'password': self.password}

        # Send request
        response = self.session.get(self.url, params=params)

        # Read response
        data = self.process_response(response)

        # Check response
        if 'LOGIN_TO_API' in data and data['LOGIN_TO_API'] == 'OK':
            logger.info('PatBase API login succeeded')
        else:
            raise PatBaseLoginError('PatBase API login failed, please check your credentials. The error was: {}'.format(data))

        # Signal authenticated state
        self.authenticated = True

    def query(self, expression):

        # Start stopwatch
        stopwatch = StopWatch()

        # Make sure we are authenticated with the API
        self.ensure_login()

        # Report what we will be doing
        logger.info('PatBase API query using expression "{}"'.format(expression))

        # Query parameters
        params = {'method': 'query', 'query': expression}

        # Send request
        response = self.session.get(self.url, params=params)

        # Read response
        data = self.process_response(response)

        # Check response
        if 'Results' in data and 'QueryKey' in data:
            date = response.headers.get('Date')
            duration = stopwatch.elapsed()
            if date:
                date = maya.parse(date).rfc3339()
            outcome = PatBaseQuery(
                expression=expression,
                results=data['Results'],
                date=date,
                duration=duration,
                querykey=data['QueryKey'],
            )
            logger.info('PatBase API query succeeded with: {}'.format(outcome))
            return outcome
        else:
            raise PatBaseQueryError('PatBase API query failed, please check your expression. The error was: {}'.format(data))

    def searchresults(self, query, offset=None, limit=None, sort=None):

        # Make sure we are authenticated with the API
        self.ensure_login()

        # Report what we will be doing
        logger.info('PatBase API searchresults using query: {}'.format(query))

        # Query parameters
        params = {'method': 'searchresults', 'querykey': query.querykey}
        if offset is not None:
            params['from'] = offset
            if limit is not None:
                params['to'] = offset + limit

        # TODO: Add knowledge about mapping
        if sort is not None:
            params['sortorder'] = sort

        # Send request
        response = self.session.get(self.url, params=params)

        # Read response
        data = self.process_response(response)

        # Check response
        if 'Families' in data:
            outcome = PatBaseResult(query=query, records=data['Families'])
            logger.info('PatBase API searchresults succeeded with: {}'.format(outcome))
            return outcome
        else:
            raise PatBaseResultError(
                'PatBase API searchresults failed. The error was: {}'.format(data))


@attr.s
class PatBaseQuery(object):

    # Search expression string
    expression = attr.ib()

    # Total result count
    results = attr.ib()

    # Timestamp of query response
    date = attr.ib()

    # Duration of query operation
    duration = attr.ib()

    # QueryKey token for retrieving results
    querykey = attr.ib()


@attr.s
class PatBaseResult(object):

    # PatBaseQuery instance
    query = attr.ib()

    # List of result items
    records = attr.ib(default=attr.Factory(list), repr=False)

    def asdict(self):
        return attr.asdict(self)
