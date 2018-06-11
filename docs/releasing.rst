#######################
Releasing this software
#######################

Setup prerequisites
===================
::

    pip install -e .[release]


Cut a release
=============
::

    make release bump=minor


Build package
=============
::

    # Build sdist package
    python setup.py sdist


Upload to PyPI
==============
::

    # Test upload
    twine upload --repository testpypi dist/*

    # Real upload
    twine upload dist/minesoft-patbase-client-0.1.0.tar.gz

See also: https://pypi.python.org/pypi/twine
