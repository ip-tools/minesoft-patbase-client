import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'attrs>=17.3.0,<18.0.0',
    'docopt==0.6.2',
    'appdirs>=1.4.3,<2.0.0',
    'requests>=2.18.4',
    'jsonpointer>=1.12,<2.0.0',
    'maya==0.5.0',
]

test_requires = [
]

setup(name='minesoft-patbase-client',
      version='0.1.0',
      description='minesoft-patbase-client is a client library for accessing the Minesoft PatBase REST API',
      long_description=README,
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: Text Processing",
        "Topic :: Utilities",
      ],
      author='Andreas Motl',
      author_email='andreas.motl@ip-tools.org',
      url='https://github.com/ip-tools/minesoft-patbase-client',
      keywords='patent information minesoft patbase rest api client bulk data download import interface '
               'research search opendata xml json',
      packages=find_packages(),
      include_package_data=True,
      package_data={
      },
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      tests_require=test_requires,
      extras_require={
          'release': [
              'bumpversion==0.5.3',
              'twine==1.9.1',
              'keyring==10.4.0',
          ],
          'documentation': [
              'Sphinx==1.6.4',
              'sphinx_rtd_theme==0.2.5b1',
          ],
      },
      dependency_links=[
      ],

      entry_points={
        'console_scripts': [
            'patbase = patbase.command:run',
        ],
      },

    )
