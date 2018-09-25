import re
from datetime import timedelta, date


def make_target_board_name(str_ym, today):
    if not isinstance(today, date):
        raise TypeError('Wrong date format of today(datetime.date)')
    return 'Sprint{} for {}.'.format(str(compute_sprint_n(str_ym, today)), today.strftime('%b'))


def make_archived_list_name(today):
    if not isinstance(today, date):
        raise TypeError('Wrong date format of today(datetime.date)')

    yesterday = today - timedelta(1)
    return '아카이브(~ {} {}.)'.format(str(yesterday.day), yesterday.strftime('%b'))


def compute_sprint_n(str_ym, today):
    if not bool(re.search(r'^\d{4}-\d{2}$', str_ym)):
        raise ValueError('Wrong team start_ym format(yyyy-mm)')

    if not isinstance(today, date):
        raise TypeError('Wrong date format of today(datetime.date)')

    start_y, start_m = str_ym.split('-')
    year_diff = today.year - int(start_y)
    month_diff = today.month - int(start_m)

    if is_valid_sprint(year_diff, month_diff):
        return year_diff * 12 + month_diff + 1
    raise TypeError('The input date is before the board sprint starts({})'.format(str_ym))


def is_valid_sprint(year_diff, month_diff):
    return year_diff > 0 or (year_diff == 0 and month_diff >= 0)
