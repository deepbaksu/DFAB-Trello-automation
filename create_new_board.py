#!/usr/bin/python3
#_*_ coding: utf-8 _*_

import sys
sys.path.insert(0, './lib')
from logger import logger

import config
from utils import compute_sprint_n, get_tboard_name, get_tboard_id, search_done_list, get_list_ids, create_archive_list, \
                  move_all_cards, create_board, get_board_labels, update_board_labels, update_board_members, move_lists, get_members

logger.debug(config.DOTTED_LINE)
logger.info("Start creating new Sprint board for each team")

for team in config.TEAM_INFO.keys():
    info = config.TEAM_INFO[team]

    if config.TEST:
        organ_name = "test93452024" # for TEST
    else:
        organ_name = info['organ_name']

    start_ym = info['start_ym']
    sprint_n = compute_sprint_n(start_ym)

    if config.TEST:
        copy_board_name = "Sprint" + str(sprint_n-1) + " for " + "Apr" + "~" # for TEST
        copy_board_name = "Sprint" + str(1) + " for " + "Mar" + "-" # for TEST
        print(copy_board_name) # for TEST
    else:
        copy_board_name = get_tboard_name(team, last_month=True)

    bid = get_tboard_id(organ_name, copy_board_name)

    if bid:
        # move done cards in last month board
        done_list_id, n_card = search_done_list(bid)

        if done_list_id and n_card > 0:
            archive_list_id = create_archive_list(bid, last_month=True)
            logger.info("Created archive-list(" + team + ") in " + copy_board_name)
            move_all_cards(done_list_id, bid, archive_list_id)
            logger.info("Moved all cards in done-list")
        elif done_list_id and n_card <= 0:
            logger.error("No card in done-list")
        else:
            logger.error("No done-list in the board")

        # create new board
        new_bid, new_board_name, existance = create_board(sprint_n, organ_name)
        if existance:
            logger.info("New Sprint board(" + new_board_name + ") is already in " + organ_name)
        else:
            logger.info("Created new Sprint board(" + new_board_name + ") in " + organ_name)

        # update board labels
        labels = get_board_labels(bid)
        if labels:
            update_board_labels(new_bid, labels)
            logger.info("Updated labels")
        else:
            logger.error("No labels in the board")

        # update board members
        mem_ids, admin_id = get_members(bid)
        if mem_ids:
            update_board_members(new_bid, mem_ids, admin_id)
            logger.info("Updated members")
        else:
            logger.error("No members in the board")

        # move lists to new board
        list_ids = get_list_ids(bid, config.BOARD_LISTS)
        if list_ids:
            move_lists(list_ids, new_bid)
            logger.info("Moved lists")
        else:
            logger.error("No lists to move")
    else:
        logger.error("No prior board in " + organ_name)
