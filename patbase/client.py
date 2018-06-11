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

from patbase.exceptions import PatBaseInvalidRequest, PatBaseLoginFailed

logger = logging.getLogger(__name__)

@attr.s
class PatBaseClient(object):

    username = attr.ib()
    password = attr.ib()

    url = attr.ib(default='https://www.patbase.com/rest/api.php')
    authenticated = attr.ib(default=False)
    tls_verify = attr.ib(default=True)

    #session = attr.ib(default=requests.Session())
    session = attr.ib(default=None)

    methods = ['login', 'query', 'searchresults']
    query_max_results = 100000

    def login(self):

        # Signal unauthenticated state
        self.authenticated = False

        # A HTTP session object keeping track of cookies
        self.session = requests.Session()

        # Send login request and read response body
        params = {'method': 'login', 'userid': self.username, 'password': self.password}
        response = self.session.get(self.url, params=params)
        content = response.content

        # The server seems to send an UTF-8 byte order mark, compensate for that.
        # https://en.wikipedia.org/wiki/Byte_order_mark#UTF-8
        try:
            content = response.content.decode('utf-8-sig')
        except:
            pass

        # Sanity checks
        if content == '':
            raise PatBaseInvalidRequest('Empty response from PatBase API login request')

        # Decode JSON response
        data = json.loads(content)

        # Check response
        if 'LOGIN_TO_API' in data and data['LOGIN_TO_API'] == 'OK':
            logger.info('Login to PatBase succeeded with user {}'.format(self.username))
        else:
            raise PatBaseLoginFailed('Login to PatBase failed, please check your credentials. The error was: {}'.format(data))

        # Signal authenticated state
        self.authenticated = True

    def logout(self):
        # Signal unauthenticated state
        self.authenticated = False

    def ensure_login(self):
        if not self.authenticated:
            self.login()

    def query(self, expression):
        pass

    def searchresults(self, querykey):
        pass
