#!/usr/bin/python
import datetime

from card_archiver import DoneCardsArchiver
from lib.config import TEAM_INFO, DONE_LIST_NAME, TRELLO_API_URL
from lib.query import QUERY
from service import TrelloResourceService

for team_info in TEAM_INFO.values():
    archiver = DoneCardsArchiver(team_info, datetime.date.today())
    archiver.archive_done_cards(TrelloResourceService(TRELLO_API_URL, QUERY), DONE_LIST_NAME)
