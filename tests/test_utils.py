import unittest
from datetime import date

from common import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.today = date(2018, 9, 27)
        self.str_ym = '2018-02'

    def test_make_target_board_name(self):
        self.assertEqual(utils.make_target_board_name(self.str_ym, self.today), 'Sprint8 for Sep.')

    def test_failed_wrong_date_format_when_making_target_board_name(self):
        self.assertRaises(TypeError, utils.make_target_board_name, self.str_ym, '2018-09-27')

    def test_make_archived_list_name(self):
        self.assertEqual(utils.make_archived_list_name(self.today), '아카이브(~ 26 Sep.)')
        self.assertEqual(utils.make_archived_list_name(date(2018, 10, 1)), '아카이브(~ 30 Sep.)')

    def test_failed_wrong_date_format_when_making_archived_list_name(self):
        self.assertRaises(TypeError, utils.make_archived_list_name, '2018-09-27')

    def test_compute_sprint_n(self):
        self.assertEqual(utils.compute_sprint_n(self.str_ym, self.today), 8)

    def test_failed_wrong_str_ym_format(self):
        self.assertRaises(ValueError, utils.compute_sprint_n, '18-02', self.today)

    def test_failed_wrong_date_format_when_compute_sprint_n(self):
        self.assertRaises(TypeError, utils.compute_sprint_n, self.str_ym, '2018-09-27')

    def test_is_valid_sprint(self):
        self.assertTrue(utils.is_valid_sprint(1, 2))
        self.assertTrue(utils.is_valid_sprint(1, -2))
        self.assertTrue(utils.is_valid_sprint(0, 0))
        self.assertFalse(utils.is_valid_sprint(-1, 4))

    def test_failed_wrong_input_in_is_valid_sprint(self):
        self.assertRaises(TypeError, utils.is_valid_sprint, '2', '4')
