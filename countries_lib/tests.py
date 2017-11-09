# -*- coding: utf-8 -*-
import unittest
from country import CountryNormalizer


class MatchCountryNameTestCase(unittest.TestCase):

    def run(self, result=None):
        with CountryNormalizer() as country_normalizer:
            self.cn = country_normalizer
            super(MatchCountryNameTestCase, self).run(result)

    def test_simple_name(self):
        self.assertEqual(self.cn.match_country_name('Russia'), 'Russia')

    def test_punctuation_sensitivity(self):
        self.assertEqual(self.cn.match_country_name('Russia!!!:)'), 'Russia')

    def test_upper_register(self):
        self.assertEqual(self.cn.match_country_name('RUSSIA'), 'Russia')

    def test_low_register(self):
        self.assertEqual(self.cn.match_country_name('russia'), 'Russia')

    def test_missed_letter(self):
        self.assertEqual(self.cn.match_country_name('Russi'), 'Russia')

    def test_excess_letter(self):
        self.assertEqual(self.cn.match_country_name('Russiaa'), 'Russia')

    def test_another_letter(self):
        self.assertEqual(self.cn.match_country_name('Rassia'), 'Russia')

    def test_simple_two_words_name(self):
        self.assertEqual(self.cn.match_country_name('Russian Federation'),
                         'Russia')

    def test_excess_word_name(self):
        self.assertEqual(self.cn.match_country_name('The Russia'), 'Russia')

    def test_american_paris_like_construction(self):
        self.assertEqual(self.cn.match_country_name('Paris, USA'),
                         'United States')

    def test_standard_accuracy_result(self):
        self.assertEqual(self.cn.match_country_name('azazaza'), None)

    def test_correct_accuracy_type(self):
        self.assertEqual(self.cn.match_country_name('Russia', 0.9), 'Russia')

    def test_incorrect_accuracy_type(self):
        self.assertEqual(self.cn.match_country_name('Russia', '0.7'), None)
        self.assertEqual(self.cn.match_country_name('Russia', []), None)

    def test_incorrect_accuracy_value(self):
        self.assertEqual(self.cn.match_country_name('Russia', 3.0), None)
        self.assertEqual(self.cn.match_country_name('Russia', -0.5), None)


class AddAndDelCountryNameTestCase(unittest.TestCase):

    def run(self, result=None):
        with CountryNormalizer() as country_normalizer:
            self.cn = country_normalizer
            super(AddAndDelCountryNameTestCase, self).run(result)

    def test_non_existing_object_delete(self):
            self.cn.del_country_name('SpecialForTest')
            self.assertEqual(self.cn.match_country_name('SpecialForTest'),
                             None)

    def test_match(self):
            self.cn.add_country_name('SpecialForTest', 'SpecialForTest')
            self.assertEqual(self.cn.match_country_name('SpecialForTest'),
                             'SpecialForTest')

    def test_existing_object_delete(self):
            self.cn.del_country_name('SpecialForTest')
            self.assertEqual(self.cn.match_country_name('SpecialForTest'),
                             None)

    def test_correct_priority_match(self):
            self.cn.add_country_name('SpecialForTest', 'SpecialForTest', 1)
            self.assertEqual(self.cn.match_country_name('SpecialForTest'),
                             'SpecialForTest')
            self.cn.del_country_name('SpecialForTest')

    def test_incorrect_priority_match(self):
        self.assertEqual(
            self.cn.add_country_name('SpecialForTest', 'SpecialForTest', 3),
            False)
        self.assertEqual(
            self.cn.add_country_name('SpecialForTest', 'SpecialForTest', -5),
            False)
        self.assertEqual(
            self.cn.add_country_name('SpecialForTest', 'SpecialForTest', 1.2),
            False)
        self.assertEqual(
            self.cn.add_country_name('SpecialForTest', 'SpecialForTest', '1'),
            False)
        self.assertEqual(
            self.cn.add_country_name('SpecialForTest', 'SpecialForTest', []),
            False)

    def test_incorrect_match(self):
        self.assertEqual(self.cn.add_country_name(1, 'SpecialForTest'),
                         False)
        self.assertEqual(self.cn.add_country_name('SpecialForTest', 1),
                         False)
        self.assertEqual(self.cn.add_country_name([], 'SpecialForTest'),
                         False)
        self.assertEqual(self.cn.add_country_name('SpecialForTest', []),
                         False)

    def test_incorrect_delete(self):
        self.assertEqual(self.cn.del_country_name(1), None)
        self.assertEqual(self.cn.del_country_name(1.5), None)
        self.assertEqual(self.cn.del_country_name([]), None)


if __name__ == '__main__':
    unittest.main()
