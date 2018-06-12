# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas.motl@ip-tools.org>
import os
import sys
import json
import timeit
import logging
from appdirs import user_data_dir


def to_list(obj):
    """Convert an object to a list if it is not already one"""
    # stolen from cornice.util
    if not isinstance(obj, (list, tuple)):
        obj = [obj, ]
    return obj


def read_list(data, separator=u','):
    if data is None:
        return []
    result = list(map(lambda x: x.strip(), data.split(separator)))
    if len(result) == 1 and not result[0]:
        result = []
    return result


def boot_logging(options=None):
    log_level = logging.INFO
    if options and options.get('debug'):
        log_level = logging.DEBUG
    setup_logging(level=log_level)


def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-20s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)


def normalize_options(options):
    normalized = {}
    for key, value in options.items():
        key = key.strip('--<>')
        normalized[key] = value
    return normalized


def read_numbersfile(filename):
    numbers = open(filename, 'r').readlines()
    numbers = map(str.strip, numbers)
    numbers = filter(lambda number: not number.startswith('#'), numbers)
    return numbers


class SmartException(Exception):

    def __init__(self, message, **kwargs):

        # Call the base class constructor with the parameters it needs
        super(SmartException, self).__init__(message)

        # Stuff more things into the exception object
        self.more_info = kwargs


class PersistentConfiguration(dict):

    def __init__(self, appname=None, configfile=None):
        self.store = {}
        if configfile:
            self.configfile = configfile
        else:
            self.configpath = user_data_dir(appname=appname, appauthor=False)
            if not os.path.exists(self.configpath):
                os.makedirs(self.configpath)
            self.configfile = os.path.join(self.configpath, 'config.json')
        self.setup()

    def setup(self):
        # json_store is not compatible with Python 3
        #self.store = json_store.open(self.configfile)
        if os.path.exists(self.configfile):
            with open(self.configfile, 'r') as f:
                self.store = json.load(f)

    def has_key(self, key):
        return self.store.has_key(key)

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value
        self.sync()

    def sync(self):
        # json_store is not compatible with Python 3
        #self.store.sync()
        with open(self.configfile, 'w') as f:
            json.dump(self.store, f, indent=4)


class StopWatch:

    def __init__(self):
        self.start()

    def start(self):
        self.starttime = self.now()

    def now(self):
        return timeit.default_timer()

    def elapsed(self):
        duration = round(self.now() - self.starttime, 2)
        return duration
