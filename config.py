#_*_ coding: utf-8 _*_

from datetime import datetime, timedelta

## PRIVATE
querystring = { 
                "key"   : "4f57bd041e9a489772600bacb64dbae7",
                "token" : "5bb25369f0d44ec73ae8d8d5ec4e0b7849d70c5b162f9ea08f3bb71cb4f9bef0" 
              }
##
today = datetime.today()
yesterday = today - timedelta(1)
month_name = today.strftime('%b')
the_day_before = yesterday.day
team_info = {
              'alpha' : { 'start_ym' : '2018-01',
                          'organ_name' : 'dfabteamalpha' },
              'bravo' : { 'start_ym' : '2018-03',
                          'organ_name' : 'dfabteambravo' }
              }
target_list = '완료'
board_lists = ['아이디어', '오늘 할 일', '완료', '일시정지']

log_filename = './dfabTrello.log'
log_format = '[%(levelname)s | %(filename)s:%(lineno)s] %(asctime)s >> %(message)s'
logger_name = 'dfabLogger'
dotted_line = '================================================='
