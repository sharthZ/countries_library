# -*- coding: utf-8 -*-
import shelve
import difflib
from os import path
from six import string_types

DB_PATH = path.join(path.split(path.abspath(__file__))[0],
                    'database', 'countries_db')


def isstr(s):
    return isinstance(s, string_types)


class _Normalizer:
    def __init__(self, db_path):
        self._countries_db = shelve.open(db_path, 'w')

    def cleanup(self):
        self._countries_db.close()

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
                   priority in (1, 2))
        if is_args:
            self._countries_db[key.lower()] = str(priority) + value
            return True
        return False

    def del_country_name(self, key):
        """ Delete key-value pair. Args:
                key - name, which you want to remove from DB (str)
        """
        if isstr(key) and key.lower() in self._countries_db.keys():
            del self._countries_db[key.lower()]

    def match_country_name(self, posname, acc=0.7):
        is_not_args = (~isstr(posname) or ~isinstance(acc, float) or
                       0.0 <= acc <= 1.0 or not posname)
        if is_not_args:
            return None
        posname = posname.lower()
        symbols = [
            ',', '.', '/', '!', '?', '<', '>', '[', ']', '|', '(', ')', '+',
            '=', '_', '*', '&', '%', ';', '№', '~', '@', '#', '$', '{', '}',
            '-', '`', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        ]
        for symb in symbols:
            posname = posname.replace(symb, ' ')
        if not posname:
            return None
        # First, we search for the whole string and
        # the value to coincide with the priority '1'
        # Check for length - to exclude options
        # when only the beginning or other part of the line has coincided
        posname_tmp = difflib.get_close_matches(posname, countries_db.keys(), 
                                                n=1, cutoff=acc)
        if posname_tmp != [] and countries_db[posname_tmp[0]][0] == '1' and \
                abs(len(posname) - len(posname_tmp[0])) <= 1:
            return countries_db[posname_tmp[0]][1:]
        # Ищем совпадение всей строки и значения с приоритетом '2'
        posname_tmp = difflib.get_close_matches(posname, countries_db.keys(), n=1, cutoff=dif_acc)
        if posname_tmp != [] and countries_db[posname_tmp[0]][0] == '2' and \
                abs(len(posname) - len(posname_tmp[0])) <= 1:
            return countries_db[posname_tmp[0]][1:]
        # Ищем совпадение всей строки без пробелов и значения с приоритетом '1'
        posname_tmp = posname.replace(' ', '')
        posname_tmp = difflib.get_close_matches(posname_tmp, countries_db.keys(), n=1, cutoff=dif_acc)
        if posname_tmp != [] and countries_db[posname_tmp[0]][0] == '1' and \
                abs(len(posname.replace(' ', '')) - len(posname_tmp[0].replace(' ', ''))) <= 1:
            return countries_db[posname_tmp[0]][1:]
        # Ищем совпадение всей строки без пробелов и значения с приоритетом '2'
        posname_tmp = posname.replace(' ', '')
        posname_tmp = difflib.get_close_matches(posname_tmp, countries_db.keys(), n=1, cutoff=dif_acc)
        if posname_tmp != [] and countries_db[posname_tmp[0]][0] == '2' and \
                abs(len(posname.replace(' ', '')) - len(posname_tmp[0].replace(' ', ''))) <= 1:
            return countries_db[posname_tmp[0]][1:]

        # Делим входную строку на слова, разделитель - пробел
        parts = posname.split(" ")
        for part in parts:
            # Ищем равное по количеству букв совпадение части строки и значения с приоритетом '1'
            part_tmp = difflib.get_close_matches(part, countries_db.keys(), n=1, cutoff=dif_acc)
            if part_tmp != [] and countries_db[part_tmp[0]][0] == '1' and len(part) == len(part_tmp[0]):
                return countries_db[part_tmp[0]][1:]
        for part in parts:
            # Ищем неравное по количеству букв совпадение части строки и значения с приоритетом '1'
            part_tmp = difflib.get_close_matches(part, countries_db.keys(), n=1, cutoff=dif_acc)
            if part_tmp != [] and countries_db[part_tmp[0]][0] == '1':
                return countries_db[part_tmp[0]][1:]
        for part in parts:
            # Ищем равное по количеству букв совпадение части строки и значения с приоритетом '2'
            part_tmp = difflib.get_close_matches(part, countries_db.keys(), n=1, cutoff=dif_acc)
            if part_tmp != [] and countries_db[part_tmp[0]][0] == '2' and len(part) == len(part_tmp[0]):
                return countries_db[part_tmp[0]][1:]
        for part in parts:
            # Ищем неравное по количеству букв совпадение части строки и значения с приоритетом '2'
            part_tmp = difflib.get_close_matches(part, countries_db.keys(), n=1, cutoff=dif_acc)
            if part_tmp != [] and countries_db[part_tmp[0]][0] == '2':
                return countries_db[part_tmp[0]][1:]
        return None


class CountryNormalizer():
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def __enter__(self):
        self.package_obj = _Normalizer(self.db_path)
        return self.package_obj

    def __exit__(self):
        self.package_obj.cleanup()






def normalize_country_name(posname, dif_acc=0.7):
    """ Приведение названия страны к общепринятому виду. Аргументы: posname (possible name) - нормализуемое название 
    (строка), dif_acc - параметр точности (вещественное число от 0 до 1, по умолчанию 0.7). 
    Возвращаемое значение: общее название страны (строка), если не найдено - 'None' (строка) """

    if type(posname) is not str or type(dif_acc) is not float or dif_acc <= 0.0 or dif_acc >= 1.0 or posname == "":
        return 'Invalid arguments'
    try:
        with shelve.open(DB_PATH, 'w') as countries_db:
            posname = posname.lower()
            # Очищаем входную строку от знаков препинания (кроме пробелов) и цифр.
            # Данный способ безопаснее, чем регулярные выражения и применение некоторых стандартных функций,
            # всвязи с национальными символами в названиях стран. Если пользователь умудрится использовать
            # иные символы, то он либо опечатался, либо издевается. Опечатки исправляются далее.
            symbols = [',', '.', '/', '!', '?', '<', '>', '[', ']', '|', '(', ')', '+', '=', '_', '*', '&', '%',
                       ';', '№', '~', '@', '#', '$', '{', '}', '-', '`', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            for symb in symbols:
                posname = posname.replace(symb, ' ')
            if posname == "":
                return 'Invalid arguments'

            # Сначала ищем совпадение всей строки и значения с приоритетом '1'
            # Проверка на длину - чтобы исключить варианты, когда совпало только начало или другая часть строки
            posname_tmp = difflib.get_close_matches(posname, countries_db.keys(), n=1, cutoff=dif_acc)
            if posname_tmp != [] and countries_db[posname_tmp[0]][0] == '1' and \
                    abs(len(posname) - len(posname_tmp[0])) <= 1:
                return countries_db[posname_tmp[0]][1:]
            # Ищем совпадение всей строки и значения с приоритетом '2'
            posname_tmp = difflib.get_close_matches(posname, countries_db.keys(), n=1, cutoff=dif_acc)
            if posname_tmp != [] and countries_db[posname_tmp[0]][0] == '2' and \
                    abs(len(posname) - len(posname_tmp[0])) <= 1:
                return countries_db[posname_tmp[0]][1:]
            # Ищем совпадение всей строки без пробелов и значения с приоритетом '1'
            posname_tmp = posname.replace(' ', '')
            posname_tmp = difflib.get_close_matches(posname_tmp, countries_db.keys(), n=1, cutoff=dif_acc)
            if posname_tmp != [] and countries_db[posname_tmp[0]][0] == '1' and \
                    abs(len(posname.replace(' ', '')) - len(posname_tmp[0].replace(' ', ''))) <= 1:
                return countries_db[posname_tmp[0]][1:]
            # Ищем совпадение всей строки без пробелов и значения с приоритетом '2'
            posname_tmp = posname.replace(' ', '')
            posname_tmp = difflib.get_close_matches(posname_tmp, countries_db.keys(), n=1, cutoff=dif_acc)
            if posname_tmp != [] and countries_db[posname_tmp[0]][0] == '2' and \
                    abs(len(posname.replace(' ', '')) - len(posname_tmp[0].replace(' ', ''))) <= 1:
                return countries_db[posname_tmp[0]][1:]

            # Делим входную строку на слова, разделитель - пробел
            parts = posname.split(" ")
            for part in parts:
                # Ищем равное по количеству букв совпадение части строки и значения с приоритетом '1'
                part_tmp = difflib.get_close_matches(part, countries_db.keys(), n=1, cutoff=dif_acc)
                if part_tmp != [] and countries_db[part_tmp[0]][0] == '1' and len(part) == len(part_tmp[0]):
                    return countries_db[part_tmp[0]][1:]
            for part in parts:
                # Ищем неравное по количеству букв совпадение части строки и значения с приоритетом '1'
                part_tmp = difflib.get_close_matches(part, countries_db.keys(), n=1, cutoff=dif_acc)
                if part_tmp != [] and countries_db[part_tmp[0]][0] == '1':
                    return countries_db[part_tmp[0]][1:]
            for part in parts:
                # Ищем равное по количеству букв совпадение части строки и значения с приоритетом '2'
                part_tmp = difflib.get_close_matches(part, countries_db.keys(), n=1, cutoff=dif_acc)
                if part_tmp != [] and countries_db[part_tmp[0]][0] == '2' and len(part) == len(part_tmp[0]):
                    return countries_db[part_tmp[0]][1:]
            for part in parts:
                # Ищем неравное по количеству букв совпадение части строки и значения с приоритетом '2'
                part_tmp = difflib.get_close_matches(part, countries_db.keys(), n=1, cutoff=dif_acc)
                if part_tmp != [] and countries_db[part_tmp[0]][0] == '2':
                    return countries_db[part_tmp[0]][1:]
            return 'None'
