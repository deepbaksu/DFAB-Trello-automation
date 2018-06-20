#!/usr/bin/python3
#_*_ coding: utf-8 _*_

import sys
sys.path.append('./lib')
from lib.logger import LOGGER
from lib import config
from lib.utils import get_board_name, get_board_id, get_list_id, get_the_number_of_card, \
                      create_list, get_archive_name, move_all_cards, compute_sprint_n

LOGGER.debug(config.DOTTED_LINE)
LOGGER.info("Start moving done-list cards to archive-list")

for team in config.TEAM_INFO:
    team_info = config.TEAM_INFO[team]
    start_ym = team_info['start_ym']
    sprint_n = compute_sprint_n(start_ym)
    board_name = get_board_name(sprint_n)
    organ_name = config.TEAM_INFO[team]['organ_name']

    bid = get_board_id(organ_name, board_name)

    if bid:
        done_list_id = get_list_id(bid, config.TARGET_LIST)
        n_card = get_the_number_of_card(done_list_id)

        if done_list_id and n_card > 0:
            archive_list_name = get_archive_name()
            archive_list_id, existance = create_list(bid, archive_list_name)
            if existance:
                LOGGER.info("List(" + archive_list_name + ") is already in " + board_name)
            else:
                LOGGER.info("Created archive-list(" + team + ")")
            move_all_cards(bid, done_list_id, archive_list_id)
            LOGGER.info("Moved all cards in done-list")
        elif done_list_id and n_card <= 0:
            LOGGER.error("No card in the done-list")
        else:
            LOGGER.error("No done-list in the board")

    else:
        LOGGER.error("No " + board_name + " in your team(" + team + ")")
