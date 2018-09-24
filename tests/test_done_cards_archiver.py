import sys

sys.path.append('./')
import unittest
import datetime
import mock
from card_archiver import DoneCardsArchiver


class TestDoneCardsArchiver(unittest.TestCase):
    def setUp(self):
        self.team_info = {
            'start_ym': '2018-01',
            'organ_name': 'testteam'
        }
        self.today = datetime.date(2018, 9, 16)
        self.archiver = DoneCardsArchiver(self.team_info, self.today)

    def test_failed_not_exist_team_info(self):
        self.assertRaises(ValueError, DoneCardsArchiver, None, self.today)

    def test_failed_not_exist_team_info(self):
        self.assertRaises(ValueError, DoneCardsArchiver, self.team_info, None)

    def test_failed_wrong_team_info(self):
        self.assertRaises(ValueError, DoneCardsArchiver, {'start_ym': '2018-02'}, self.today)

    def test_failed_wrong_today_format(self):
        self.assertRaises(ValueError, DoneCardsArchiver, self.team_info, '2018-09-16')

    def test_failed_wrong_team_start_ym_format(self):
        self.assertRaises(ValueError, DoneCardsArchiver, {
            'start_ym': '18-01',
            'organ_name': 'testteam'
        }, self.today)

    def test_make_target_board_name(self):
        self.assertEqual(self.archiver.make_target_board_name(), 'Sprint9 for Sep.')

    def test_failed_make_target_board_name(self):
        self.archiver.today = datetime.date(2017, 12, 16)
        self.assertRaises(ValueError, self.archiver.make_target_board_name)

    def test_make_archived_list_name(self):
        self.assertEqual(self.archiver.make_archived_list_name(), '아카이브(~ 15 Sep.)')

    def test_archive_done_cards(self):
        board_id = 'boardId'
        archived_list_id = 'archivedListId'
        done_list_id = 'doneListId'
        resource_service = mock.Mock()
        resource_service.get_board_id.return_value = board_id
        resource_service.create_archived_list.return_value = archived_list_id
        resource_service.get_list_id.return_value = done_list_id

        self.archiver.archive_done_cards(resource_service, '완료')

        resource_service.get_board_id.assert_called_with(self.team_info['organ_name'], 'Sprint9 for Sep.')
        resource_service.create_archived_list.assert_called_with(board_id, '아카이브(~ 15 Sep.)')
        resource_service.move_done_cards(board_id, done_list_id, archived_list_id)
