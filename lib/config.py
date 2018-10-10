#_*_ coding: utf-8 _*_

"""Configuration"""
import os
from datetime import datetime, timedelta

## date
TODAY = datetime.today()
YESTERDAY = TODAY - timedelta(1)
THE_DAY_BEFORE = YESTERDAY.day
MONTH_NAME = TODAY.strftime('%b')
LAST_MONTH = TODAY.replace(day=1) - timedelta(days=1)
LAST_MONTH_NAME = LAST_MONTH.strftime('%b')

##
TEAM_INFO = {
    'alpha' : {'start_ym' : '2018-01',
               'organ_name' : 'dfabteamalpha'},
    'bravo' : {'start_ym' : '2018-03',
               'organ_name' : 'dfabteambravo'}
}
DONE_LIST_NAME = '완료'
BOARD_LISTS = ['아이디어', '오늘 할 일', '완료', '일시정지']

ADMIN_USERS = ['jinwoopark8', 'minjikim59', 'martinhwang']

## logger
LOG_FILENAME = os.getcwd() + '/dfabTrello.log'
LOG_FORMAT = '[%(levelname)s | %(filename)s:%(lineno)s] %(asctime)s >> %(message)s'
LOGGER_NAME = 'dfabLogger'
DOTTED_LINE = '================================================='

TRELLO_API_URL = "https://api.trello.com/1"
