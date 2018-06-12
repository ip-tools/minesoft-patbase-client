# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas.motl@ip-tools.org>
import json
import logging
from docopt import docopt
from patbase import __version__
from patbase.client import PatBaseClient
from patbase.util import boot_logging, normalize_options, PersistentConfiguration

"""
Python command line client for accessing the Minesoft PatBase REST API.

See also:
- https://www.patbase.com/rest/
- https://www.patbase.com/rest/PatBaseRestAPI.pdf
"""

logger = logging.getLogger(__name__)

APP_NAME = 'patbase'

def run():
    """
    Usage:
        {program} login --username=<username> --password=<password>
        {program} search <expression> [--username=<username> --password=<password>]
        {program} info
        {program} --version
        {program} (-h | --help)

    Examples:

        # Display published application by publication number in XML format
        {program} login --username=test@example.org --password=secret

        # Search for documents matching "Space Shuttle" in all fulltext fields and display JSON response
        {program} search 'FT=(Space Shuttle)'

    """

    # Use generic commandline options schema and amend with current program name
    commandline_schema = (run.__doc__).format(program=APP_NAME)

    # Read commandline options
    options = normalize_options(docopt(commandline_schema, version=APP_NAME + ' ' + __version__))

    # Start logging subsystem
    boot_logging(options)

    # The configuration file for storing API credentials
    config = PersistentConfiguration(appname='minesoft-patbase-client')

    if options['login']:

        # Create API client
        client = PatBaseClient(username=options['username'], password=options['password'])
        client.login()

        # Save credentials for subsequent operations
        logger.info('Saving login credentials to {}'.format(config.configfile))
        config['api_credentials'] = {
            'username': options['username'],
            'password': options['password'],
        }

    elif options['search']:

        # Optionally load credentials from configuration file
        username, password = options['username'], options['password']
        if not username or not password:
            api_credentials = config['api_credentials']
            username, password = api_credentials['username'], api_credentials['password']

        # Create API client
        client = PatBaseClient(username=username, password=password)
        query = client.query(options['expression'])
        result = client.searchresults(query, offset=0, limit=20)
        print(json.dumps(result.asdict()))
