from datetime import timedelta

from common import utils


class SprintBoardCreator:
    def __init__(self, team_info, today, resource_service):
        self.team_info = team_info
        self.today = today
        self.resource_service = resource_service

    def create_board(self):
        board_name = utils.make_target_board_name(self.team_info['start_ym'], self.today)
        return self.resource_service.create_sprint_board(self.team_info['organ_name'], board_name)

    def move_essential_lists(self, board_id, list_names):
        lists_ids = self.resource_service.get_lists_ids(self._get_prev_board_id(), list_names)
        for list_id in reversed(lists_ids):
            self.resource_service.move_list(board_id, list_id)

    def update_labels(self, new_board_id):
        self.resource_service.update_board_labels(new_board_id,
                                                  self.resource_service.get_board_labels(self._get_prev_board_id()))

    def update_members(self, new_board_id, admin_users):
        members_data = self.resource_service.get_board_members(self._get_prev_board_id())
        for member in members_data:
            self.resource_service.update_board_member(new_board_id, member['id'],
                                                      self._get_member_type(member['username'], admin_users))

    def _get_prev_board_id(self):
        prev_board_name = utils.make_target_board_name(self.team_info['start_ym'], self.today - timedelta(1))
        return self.resource_service.get_board_id(self.team_info['organ_name'], prev_board_name)

    def _get_member_type(self, user_name, admin_users):
        return 'admin' if user_name in admin_users else 'normal'
