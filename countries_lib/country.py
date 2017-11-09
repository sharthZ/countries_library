# -*- coding: utf-8 -*-
import shelve
import difflib as df
from os import path
from six import string_types
from collections import Counter

DB_PATH = path.join(path.split(path.abspath(__file__))[0],
                    'database', 'countries_db')
PRIORITES = (1, 2)


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
                priority - priority for normalization:
                    '1' - high (official name, translate, abbreviation),
                    '2' - low (capital, state, region, etc.)
            Return:
                True - if key-value pair successfully added,
                False - otherwise
        """
        is_args = (isstr(key) and isstr(value) and type(priority) is int and
                   priority in PRIORITES)
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
        def match(s_in, acc, n=1):
            for is_wo in (False, True):
                s = s_in if ~is_wo else s_in.replace(' ', '')
                r = df.get_close_matches(s, self._db.keys(),
                                         n=n, cutoff=acc)
                for p in PRIORITES:
                    len_r = len(r[0]) if ~is_wo else len(r[0].replace(' ', ''))
                    if r != [] and self._db[r[0]][0] == p and \
                            abs(len(s) - len_r) <= 1:
                        return self._db[r[0]][1:]

        is_not_args = (~isstr(name) or ~isinstance(acc, float) or
                       0.0 <= acc <= 1.0 or not name)
        if is_not_args:
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
        res_name = match(name, acc)
        if res_name:
            return res_name
        parts = name.split(' ')
        res_cnt = Counter(filter(None, [match(p, acc, 3) for p in parts]))
        return res_cnt.most_common(1)[0][0]


class CountryNormalizer():
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def __enter__(self):
        self.package_obj = _Normalizer(self.db_path)
        return self.package_obj

    def __exit__(self):
        self.package_obj.cleanup()
