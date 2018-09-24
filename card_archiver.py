import re
from datetime import timedelta, date


class DoneCardsArchiver:
    def __init__(self, team_info, today):
        self.team_info = team_info
        self.today = today
        self._check_valid_init_input()

    def make_target_board_name(self):
        return 'Sprint{} for {}.'.format(str(self._compute_sprint_n()), self.today.strftime('%b'))

    def make_archived_list_name(self):
        return "아카이브(~ " + str((self.today - timedelta(1)).day) + " " + self.today.strftime('%b') + ".)"

    def archive_done_cards(self, trello_resource_service, done_list_name):
        board_id = trello_resource_service.get_board_id(self.team_info['organ_name'], self.make_target_board_name())
        archived_list_id = trello_resource_service.create_archived_list(board_id, self.make_archived_list_name())
        done_list_id = trello_resource_service.get_list_id(board_id, done_list_name)
        trello_resource_service.move_done_cards(board_id, done_list_id, archived_list_id)

    def _compute_sprint_n(self):
        start_y, start_m = self.team_info['start_ym'].split('-')
        year_diff = self.today.year - int(start_y)
        month_diff = self.today.month - int(start_m)
        if self.is_valid_sprint(year_diff, month_diff):
            return year_diff * 12 + month_diff + 1
        raise ValueError('The input date is before the board sprint starts({})'.format(self.team_info['start_ym']))

    def _check_valid_init_input(self):
        if not self.team_info or not self.today:
            raise ValueError('There are no initial input values')
        if 'start_ym' not in self.team_info or 'organ_name' not in self.team_info:
            raise ValueError('Wrong team information(start_ym or organ_name do not exist)')
        if not isinstance(self.today, date):
            raise ValueError('Wrong date format of today(datetime.date)')
        if not bool(re.search(r'^\d{4}-\d{2}$', self.team_info['start_ym'])):
            raise ValueError('Wrong team start_ym format(yyyy-mm)')

    @staticmethod
    def is_valid_sprint(year_diff, month_diff):
        return year_diff > 0 or (year_diff == 0 and month_diff >= 0)
