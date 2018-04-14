#!/usr/bin/python3
#_*_ coding: utf-8 _*_

import sys
sys.path.insert(0, './lib')

from utils import *
from logger import logger

logger.debug(DOTTED_LINE)
logger.info("Start creating new Sprint board for each team")

for info in TEAM_INFO.values():
    organ_name = info['organ_name']
#    organ_name = "test93452024" # for TEST
    start_ym = info['start_ym']
    sprint_n = compute_sprint_n(start_ym)
    last_month_name = YESTERDAY.strftime('%b')
#    last_month_name = "Mar" # for TEST
    copy_board_name = "Sprint" + str(sprint_n-1) + " for " + last_month_name + "."
#    copy_board_name = "Sprint" + str(sprint_n-1) + " for " + last_month_name + "-" # for TEST (To remove, uncomment upper line)
#    print(copy_board_name) # for TEST
    bid = get_tboard_id(organ_name, copy_board_name)

    if bid:
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



