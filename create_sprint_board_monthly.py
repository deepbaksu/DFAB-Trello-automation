# _*_ coding: utf-8 _*_
from datetime import date, timedelta

from board_creator import SprintBoardCreator
from card_archiver import DoneCardsArchiver
from lib.config import TEAM_INFO, DONE_LIST_NAME, TRELLO_API_URL, ADMIN_USERS, BOARD_LISTS
from lib.query import QUERY
from service import TrelloResourceService

today = date.today()
yesterday = today - timedelta(1)
resource_service = TrelloResourceService(TRELLO_API_URL, QUERY)

for team_info in TEAM_INFO.values():
    cards_archiver = DoneCardsArchiver(team_info, today)
    board_creator = SprintBoardCreator(team_info, today, resource_service)

    cards_archiver.archive_done_cards(resource_service, DONE_LIST_NAME, yesterday)
    new_board_id = board_creator.create_board()
    board_creator.move_essential_lists(new_board_id, BOARD_LISTS)
    board_creator.update_labels(new_board_id)
    board_creator.update_members(new_board_id, ADMIN_USERS)
