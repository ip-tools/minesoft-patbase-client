# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas.motl@ip-tools.org>
import logging
from docopt import docopt, DocoptExit
from patbase import __version__
#from uspto.pbd.client import UsptoPairBulkDataClient
#from uspto.util.command import run_command
#from uspto.util.common import boot_logging
from patbase.client import PatBaseClient
from patbase.util import boot_logging, normalize_options

"""
Python command line client for accessing the Minesoft PatBase REST API (https://www.patbase.com/rest/).
See also: https://www.patbase.com/rest/PatBaseRestAPI.pdf
"""

logger = logging.getLogger(__name__)

APP_NAME = 'patbase'

def run():
    """
    Usage:
        {program} login --username=<username> --password=<password>
        {program} info
        {program} --version
        {program} (-h | --help)

    Examples:

        # Display published application by publication number in XML format
        {program} login --username=test@example.org --password=secret

        # Search for documents matching "applicant=nasa" and display polished JSON response
        {program} search 'firstNamedApplicant:(nasa)' --filter='appFilingDate:[2000-01-01T00:00:00Z TO 2017-12-31T23:59:59Z]'

        # Search for documents matching "applicant=grohe" filed between 2010 and 2017
        {program} search 'firstNamedApplicant:(*grohe*)' --filter='appFilingDate:[2010-01-01T00:00:00Z TO 2017-12-31T23:59:59Z]'

        # Search for documents matching "applicant=nasa" and download zip archives containing bundles in XML and JSON formats
        {program} search 'firstNamedApplicant:(nasa)' --download --format=xml,json --directory=/tmp

    """

    # Use generic commandline options schema and amend with current program name
    commandline_schema = (run.__doc__).format(program=APP_NAME)

    # Read commandline options
    options = normalize_options(docopt(commandline_schema, version=APP_NAME + ' ' + __version__))

    # Start logging subsystem
    boot_logging(options)

    # An instance of the API client
    client = PatBaseClient(username=options['username'], password=options['password'])
    client.login()
