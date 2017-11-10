# -*- coding: utf-8 -*-
import shelve
import difflib as df
from os import path
from six import string_types
from collections import Counter

DB_PATH = path.join(path.split(path.abspath(__file__))[0],
                    'database', 'countries_db')
PRIORITIES = (1, 2)


def isstr(s):
    return isinstance(s, string_types)


class _Normalizer:
    def __init__(self, db_path):
        self._db = shelve.open(db_path, 'w')

    def cleanup(self):
        self._db.close()

    def add_country_name(self, key, value, priority=2):
        """ Add key-value pair for country.
            Args:
                key - name, which you want to add to DB (str),
                value - official country name (str),
                priority - priority for normalization (default 2):
                    1 - high (official name, translate, abbreviation),
                    2 - low (capital, state, region, etc.)
            Return:
                True - if key-value pair successfully added,
                False - otherwise
        """
        is_args = (isstr(key) and isstr(value) and type(priority) is int and
                   priority in PRIORITIES)
        if is_args:
            self._db[key.lower()] = str(priority) + value
            return True
        return False

    def del_country_name(self, key):
        """ Delete key-value pair. Args:
                key - name, which you want to remove from DB (str)
        """
        if isstr(key) and key.lower() in self._db.keys():
            del self._db[key.lower()]

    def match_country_name(self, name, acc=0.7):
        """ Match closest country name.
            Args:
                name - name, which to search (str)
                acc - accuracy (default 0.7), float in [0, 1], higher = better
            Return:
                str - if search with specified accuracy was successful,
                None - otherwise
        """

        def match(s_in, n=1, f=True):
            for wo in (False, True):
                s = s_in if ~wo else s_in.replace(' ', '')
                r = df.get_close_matches(s, self._db.keys(),
                                         n=n, cutoff=acc)
                if len(r) < 1:
                    continue
                for p in PRIORITIES:
                    if self._db[r[0]][0] == str(p):
                        return self._db[r[0]][1 if f else 0:]

        is_args = (isstr(name) and isinstance(acc, float) and
                   0.0 <= acc <= 1.0 and name != '')
        if not is_args:
            return None
        name = name.lower()
        symbols = [
            ',', '.', '/', '!', '?', '<', '>', '[', ']', '|', '(', ')', '+',
            '=', '_', '*', '&', '%', ';', '№', '~', '@', '#', '$', '{', '}',
            '-', '`', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        ]
        for symb in symbols:
            name = name.replace(symb, ' ')
        if not name:
            return None
        res_name = match(name)
        if res_name is not None:
            return res_name
        parts = name.split(' ')
        res_list = list(filter(None, [match(p, 3, False) for p in parts]))
        res_list.sort()
        if len(res_list) > 0:
            return Counter(res_list).most_common(1)[0][0][1:]


class CountryNormalizer():
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def open(self):
        self.package_obj = _Normalizer(self.db_path)
        return self.package_obj

    def __enter__(self):
        return self.open()

    def close(self):
        self.package_obj.cleanup()

    def __exit__(self, *args, **kwargs):
        self.close()
