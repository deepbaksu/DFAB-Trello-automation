import sys

sys.path.append('./')
import unittest
from datetime import date, timedelta
import mock
from card_archiver import DoneCardsArchiver


class TestDoneCardsArchiver(unittest.TestCase):
    def setUp(self):
        self.team_info = {
            'start_ym': '2018-01',
            'organ_name': 'testteam'
        }
        self.today = date(2018, 9, 16)
        self.archiver = DoneCardsArchiver(self.team_info, self.today)

    def test_failed_not_exist_team_info(self):
        self.assertRaises(ValueError, DoneCardsArchiver, None, self.today)

    def test_failed_not_exist_today_date(self):
        self.assertRaises(ValueError, DoneCardsArchiver, self.team_info, None)

    def test_failed_wrong_team_info(self):
        self.assertRaises(ValueError, DoneCardsArchiver, {'start_ym': '2018-02'}, self.today)

    def test_failed_wrong_today_format(self):
        self.assertRaises(TypeError, DoneCardsArchiver, self.team_info, '2018-09-16')

    def test_failed_wrong_team_start_ym_format(self):
        self.assertRaises(ValueError, DoneCardsArchiver, {
            'start_ym': '18-01',
            'organ_name': 'testteam'
        }, self.today)

    def test_archive_done_cards(self):
        resource_ids = {'board_id': 'boardId',
                        'archived_list_id': 'archivedListId',
                        'done_list_id': 'doneListId'}

        resource_service = self._mock_resource_service(resource_ids)

        self.archiver.archive_done_cards(resource_service, '완료', self.today)

        self._service_assert_called_with(resource_service, 'Sprint9 for Sep.', '아카이브(~ 15 Sep.)', resource_ids)

    def test_archive_done_cards_in_previous_board(self):
        resource_ids = {'board_id': 'boardId',
                        'archived_list_id': 'archivedListId',
                        'done_list_id': 'doneListId'}

        resource_service = self._mock_resource_service(resource_ids)

        self.archiver.today = date(2018, 10, 1)
        self.archiver.archive_done_cards(resource_service, '완료', self.today - timedelta(1))

        self._service_assert_called_with(resource_service, 'Sprint9 for Sep.', '아카이브(~ 30 Sep.)', resource_ids)

    def _mock_resource_service(self, resource_ids):
        resource_service = mock.Mock()
        resource_service.get_board_id.return_value = resource_ids['board_id']
        resource_service.create_archived_list.return_value = resource_ids['archived_list_id']
        resource_service.get_list_id.return_value = resource_ids['done_list_id']

        return resource_service

    def _service_assert_called_with(self, service, board_name, list_name, resource_ids):
        service.get_board_id.assert_called_with(self.team_info['organ_name'], board_name)
        service.create_archived_list.assert_called_with(resource_ids['board_id'], list_name)
        service.move_done_cards.assert_called_with(resource_ids['board_id'],
                                                   resource_ids['done_list_id'],
                                                   resource_ids['archived_list_id'])
