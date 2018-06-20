#!/usr/bin/python3
#_*_ coding: utf-8 _*_

from lib.logger import logger
from lib import config
from lib.utils import get_tboard_name, get_tboard_id, search_done_list, \
                      create_archive_list, move_all_cards

logger.debug(config.DOTTED_LINE)
logger.info("Start moving done-list cards to archive-list")

for team in config.TEAM_INFO:
    if config.TEST:
        tboard_name = "Sprint1 for Mar-" # for TEST
    else:
        tboard_name = get_tboard_name(team)

    if config.TEST:
        organ_name = "test93452024" # for TEST
    else:
        organ_name = config.TEAM_INFO[team]['organ_name']

    tboard_id = get_tboard_id(organ_name, tboard_name)

    if tboard_id:
        done_list_id, n_card = search_done_list(tboard_id)

        if done_list_id and n_card > 0:
            archive_list_id = create_archive_list(tboard_id)
            logger.info("Created archive-list(" + team + ")")
            move_all_cards(done_list_id, tboard_id, archive_list_id)
            logger.info("Moved all cards in done-list")
        elif done_list_id and n_card <= 0:
            logger.error("No card in the done-list")
        else:
            logger.error("No done-list in the board")

    else:
        logger.error("No " + tboard_name + " in your team(" + team + ")")
