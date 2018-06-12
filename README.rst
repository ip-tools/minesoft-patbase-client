.. image:: https://img.shields.io/badge/Python-2.7,%203.6-green.svg
    :target: https://pypi.org/project/minesoft-patbase-client/

.. image:: https://img.shields.io/pypi/v/minesoft-patbase-client.svg
    :target: https://pypi.org/project/minesoft-patbase-client/

.. image:: https://img.shields.io/github/tag/ip-tools/minesoft-patbase-client.svg
    :target: https://github.com/ip-tools/minesoft-patbase-client

|

################################
Minesoft PatBase REST API client
################################


*****
About
*****
``minesoft-patbase-client`` is a client library for accessing the Minesoft PatBase REST API.
It is written in Python.

Currently, it implements wrappers for the following API methods:

- Login
- Query
- SearchResults

For more details about the whole list of API methods,
please consult the canonical `PatBase REST API documentation`_.

.. _PatBase REST API documentation: http://www.patbase.com/rest/PatBaseRestAPI.pdf


**********************
About PatBase REST API
**********************
The Minesoft PatBase API allows software applications to interface seamlessly
with PatBase, Minesoft’s global patent database. Containing approximately
100 million patent documents from over 100 patent issuing authorities,
PatBase is used by large corporations, international IP law firms and tech
transfer companies for search, review, analysis and monitoring of patent information.

The Minesoft PatBase API is a modern REST API with advanced functionality to
create individual software solutions, for powerful data retrieval and for
integrating with federated search engines as well as in-house corporate applications.

For more details, see also the blog article `Minesoft API to access big patent data`_.

.. _Minesoft API to access big patent data: https://minesoft.com/2015/02/20/minesoft-develops-api-to-open-up-access-to-big-patent-data/


***************
Getting started
***************

Install
=======
If you know your way around Python, installing this software is really easy::

    pip install minesoft-patbase-client

Please refer to the `virtualenv`_ page about further guidelines how to install and use this software.

.. _virtualenv: https://github.com/ip-tools/minesoft-patbase-client/blob/master/docs/virtualenv.rst


Usage
=====
::

    # Login to PatBase API and remember credentials for subsequent requests
    patbase login --username=test@example.org --password=secret

    # Submit fulltext search expression and display results in JSON format
    patbase search 'FT=(Space Shuttle)' | jq .


*******************
Project information
*******************
``minesoft-patbase-client`` is released under the terms of the GNU AGPL 3.0 license.
The code lives on `GitHub <https://github.com/ip-tools/minesoft-patbase-client>`_ and
the Python package is published to `PyPI <https://pypi.org/project/minesoft-patbase-client/>`_.
You might also want to have a look at the `documentation <https://docs.ip-tools.org/minesoft-patbase-client/>`_.

The software has been tested on Python 2.7 and Python 3.6.

Contributing
============
If you'd like to contribute you're most welcome!
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue.

Thanks in advance for your efforts, we really appreciate any help or feedback.

License
=======
This software is copyright © 2018 The PatZilla authors. All rights reserved.

It is and will always be **free and open source software**.

Use of the source code included here is governed by the
`GNU Affero General Public License <GNU-AGPL-3.0_>`_ and the
`European Union Public License <EUPL-1.2_>`_.

.. _GNU-AGPL-3.0: https://docs.ip-tools.org/ip-navigator/_static/license/GNU-AGPL-3.0.txt
.. _EUPL-1.2: https://docs.ip-tools.org/ip-navigator/_static/license/EUPL-1.2.txt


----

Have fun!
