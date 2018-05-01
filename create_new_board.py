#!/usr/bin/python3
#_*_ coding: utf-8 _*_

import sys
sys.path.insert(0, './lib')

from utils import *
from logger import logger

logger.debug(DOTTED_LINE)
logger.info("Start creating new Sprint board for each team")

#for infos in TEAM_INFO.values():
for team in TEAM_INFO.keys():
    infor = TEAM_INFO[team]

    if TEST:
        organ_name = "test93452024" # for TEST
    else:
        organ_name = infor['organ_name']

    start_ym = infor['start_ym']
    sprint_n = compute_sprint_n(start_ym)

    if TEST:
        copy_board_name = "Sprint" + str(sprint_n-1) + " for " + "Apr" + "~" # for TEST
        print(copy_board_name) # for TEST
    else:
        copy_board_name = get_tboard_name(team, last_month=True)

    bid = get_tboard_id(organ_name, copy_board_name)

    if bid:
        # move done cards in last month board
        done_list_id, n_card = search_done_list(bid)

        if done_list_id and n_card > 0:
            archive_list_id = create_archive_list(bid)
            logger.info("Created archive-list(" + team + ") in " + copy_board_name)
            move_all_cards(done_list_id, bid, archive_list_id)
            logger.info("Moved all cards in done-list")
        elif done_list_id and n_card <= 0:
            logger.error("No card in the done-list")
        else:
            logger.error("No done-list in the board" )

        # create new board
        new_bid, new_board_name = create_board(sprint_n, organ_name)
        logger.info("Created new Sprint board(" + new_board_name + ") in " + organ_name)
        labels = get_board_labels(bid)

        if labels:
            update_board_labels(new_bid, labels)
            logger.info("Updated labels")

        list_ids = get_list_ids(bid, BOARD_LISTS)

        if list_ids:
            move_lists(list_ids, new_bid)
            logger.info("Moved lists")
        else:
            logger.error("No lists to move")
    else:
        logger.error("No prior board in " + organ_name)



