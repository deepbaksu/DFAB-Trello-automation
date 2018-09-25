import re
from datetime import date

from common import utils


class DoneCardsArchiver:
    def __init__(self, team_info, today):
        self.team_info = team_info
        self.today = today
        self._check_valid_init_input()

    def archive_done_cards(self, resource_service, list_name, board_date):
        board_id = resource_service.get_board_id(self.team_info['organ_name'],
                                                 utils.make_target_board_name(self.team_info['start_ym'], board_date))
        archived_list_id = resource_service.create_archived_list(board_id,
                                                                 utils.make_archived_list_name(self.today))
        done_list_id = resource_service.get_list_id(board_id, list_name)

        resource_service.move_done_cards(board_id, done_list_id, archived_list_id)

    def _check_valid_init_input(self):
        if not self.team_info or not self.today:
            raise ValueError('There are no initial input values')
        if 'start_ym' not in self.team_info or 'organ_name' not in self.team_info:
            raise ValueError('Wrong team information(start_ym or organ_name do not exist)')
        if not isinstance(self.today, date):
            raise TypeError('Wrong date format of today(datetime.date)')
        if not bool(re.search(r'^\d{4}-\d{2}$', self.team_info['start_ym'])):
            raise ValueError('Wrong team start_ym format(yyyy-mm)')
