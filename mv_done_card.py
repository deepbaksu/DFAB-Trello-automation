#_*_ coding: utf-8 _*_

from config import *
from utils import *
from logger import logger

logger.debug(dotted_line)
logger.info("Start moving done-list cards to archive-list")

for team in team_info.keys():
    tboard_name = get_tboard_name(team, month_name)
#    tboard_name = "Sprint1 for Mar-" # for TEST

    organ_name = team_info[team]['organ_name']
#    organ_name = "test93452024" # for TEST
    tboard_id = get_tboard_id(organ_name, tboard_name, querystring)

    if tboard_id:
        done_list_id, n_card = search_done_list(tboard_id, querystring)

        if done_list_id and n_card > 0:
            archive_list_id = create_archive_list(tboard_id, month_name, the_day_before, querystring)
            logger.info("Created archive-list(" + team + ")")
            move_all_cards(done_list_id, tboard_id, archive_list_id, querystring)
            logger.info("Moved all cards in done-list")

        elif done_list_id and n_card <= 0:
            logger.error("No card in the done-list")
        else:
            logger.error("No done-list in the board" )

    else:
        logger.error("No " + tboard_name + " in your team(" + team + ")")
