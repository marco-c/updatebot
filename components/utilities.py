#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import copy
from dateutil.parser import parse


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class NeverUseMeClass:
    def __init__(self, *args, **kwargs):
        pass

    def update_config(self, config):
        pass

    def __getattr__(self, *args, **kwargs):
        raise Exception("No methods on this class should be called")


PUSH_HEALTH_IGNORED_DICTS = ["commitHistory", 'jobCounts', 'status']
PUSH_HEALTH_IGNORED_KEYS = ['next', 'previous', 'revision', 'id', 'result', 'push_timestamp']


# Needed so you can raise an exception in a lambda
def raise_(e):
    raise e


def string_date_to_uniform_string_date(s):
    return parse(s).strftime('%Y-%m-%d %H:%M:%S')


def merge_dictionaries(a, b, ignored_dicts=[], ignored_keys=[]):
    c = copy.deepcopy(b)

    for key, value in a.items():
        if isinstance(value, dict):
            if key in ignored_dicts:
                pass
            else:
                # get node or create one
                node = c.setdefault(key, {})
                c[key] = merge_dictionaries(value, node, ignored_dicts, ignored_keys)
        elif isinstance(value, list):
            if key in c:
                assert isinstance(c[key], list)
                c[key] += value

                # Not everything will sort.
                # This feels like the type of extremey subtle behavior that could
                # find its way into a security vulnerability.
                try:
                    c[key] = sorted(c[key])
                except Exception:
                    pass
            else:
                c[key] = value
        else:
            if key == 'count':
                c[key] = a[key] + b[key]
            elif key in ignored_keys:
                pass
            elif key in c and a[key] == b[key]:
                pass
            else:
                assert key not in c, "We already had the key '%s' in the dictionary. Values: '%s', '%s'" % (key, a[key], b[key])
                c[key] = value

    return c
