import unittest
from datetime import date

import mock

from board_creator import SprintBoardCreator


class TestSprintBoardCreator(unittest.TestCase):
    def setUp(self):
        self.team_info = {
            'start_ym': '2018-01',
            'organ_name': 'testteam'
        }
        self.today = date(2018, 10, 1)
        self.resource_service = mock.Mock()
        self.board_creator = SprintBoardCreator(self.team_info, self.today, self.resource_service)
        self.prev_board_id = 'prevBoardId'
        self.new_board_id = 'newBoardId'
        # Todo: check_valid_input

    def test_create_board(self):
        self.resource_service.create_sprint_board.return_value = self.new_board_id
        self.assertEqual(self.board_creator.create_board(), self.new_board_id)
        self.resource_service.create_sprint_board.assert_called_with(self.team_info['organ_name'], 'Sprint10 for Oct.')

    def test_move_essential_lists(self):
        list_names = ['list1', 'list2', 'list3']
        list_ids = ['listId1', 'listId2', 'listId3']

        self.resource_service.get_board_id.return_value = self.prev_board_id
        self.resource_service.get_lists_ids.return_value = list_ids
        self.board_creator.move_essential_lists(self.new_board_id, list_names)
        self.resource_service.get_lists_ids.assert_called_with(self.prev_board_id, list_names)
        self.resource_service.move_list.assert_has_calls(
            [mock.call(self.new_board_id, list_id) for list_id in reversed(list_ids)])

    def test_update_labels(self):
        labels_data = ['labels_data']

        self.resource_service.get_board_id.return_value = self.prev_board_id
        self.resource_service.get_board_labels.return_value = labels_data
        self.board_creator.update_labels(self.new_board_id)
        self.resource_service.get_board_labels.assert_called_with(self.prev_board_id)
        self.resource_service.update_board_labels.assert_called_with(self.new_board_id, labels_data)

    def test_update_members(self):
        admin_users = ['adminMember1', 'adminMember2']
        members_data = [{'id': 'memberId1', 'username': 'normalMember'},
                        {'id': 'memberId2', 'username': admin_users[0]}]

        self.resource_service.get_board_id.return_value = self.prev_board_id
        self.resource_service.get_board_members.return_value = members_data
        self.board_creator.update_members(self.new_board_id, admin_users)
        self.resource_service.get_board_members.assert_called_with(self.prev_board_id)
        self.resource_service.update_board_member.assert_has_calls([
            mock.call(self.new_board_id, members_data[0]['id'], 'normal'),
            mock.call(self.new_board_id, members_data[1]['id'], 'admin')
        ])
