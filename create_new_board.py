#_*_ coding: utf-8 _*_

"""Move all done cards to archive list in prior sprint board.
   Create new sprint board and move necessary lists from prior board to new board"""
import sys
sys.path.append('./lib')
from lib.logger import LOGGER
from lib.config import DOTTED_LINE, TEAM_INFO, DONE_LIST_NAME, ADMIN_USER_NAME, BOARD_LISTS
from lib.utils import compute_sprint_n, get_board_name, get_board_id, get_list_id, \
                      get_the_number_of_card, create_list, move_all_cards, create_board, \
                      get_labels_data, update_board_label, update_board_member, move_list, \
                      get_members_data, get_archive_name

LOGGER.debug(DOTTED_LINE)
LOGGER.info("Start creating new Sprint board for each team")

for team in TEAM_INFO:
    team_info = TEAM_INFO[team]
    organ_name = team_info['organ_name']
    start_ym = team_info['start_ym']
    sprint_n = compute_sprint_n(start_ym)

    board_name = get_board_name(sprint_n, last_month=True)
    bid = get_board_id(organ_name, board_name)

    if bid:
        # move done cards in last month board
        done_list_id = get_list_id(bid, DONE_LIST_NAME)

        if done_list_id:
            n_card = get_the_number_of_card(done_list_id)

            if n_card > 0:
                archive_list_name = get_archive_name(last_month=True)
                archive_list_id, existance = create_list(bid, archive_list_name)
                if existance:
                    LOGGER.info("List(" + archive_list_name + ") is already in " + board_name)
                else:
                    LOGGER.info("Created archive-list(" + team + ") in " + board_name)
                move_all_cards(bid, done_list_id, archive_list_id)
                LOGGER.info("Moved all cards in done-list")
            else:
                LOGGER.error("No card in done-list")
        else:
            LOGGER.error("No done-list in the board")

        # create new board
        new_board_name = get_board_name(sprint_n)
        new_bid, existance = create_board(organ_name, new_board_name)
        if existance:
            LOGGER.info("Sprint board(" + new_board_name + ") is already in " + organ_name)
        else:
            LOGGER.info("Created new Sprint board(" + new_board_name + ") in " + organ_name)

        # update board labels
        labels = get_labels_data(bid)
        for label in labels:
            if 'name' in label:
                update_board_label(new_bid, label['color'], label['name'])
                LOGGER.info("Updated label(name: %s, color: %s)", label['name'], label['color'])

        # update board members
        mem_list = get_members_data(bid)
        for mem in mem_list:
            if mem['username'] == ADMIN_USER_NAME:
                mem_type = 'admin'
            else:
                mem_type = 'normal'

            update_board_member(new_bid, mem['id'], mem_type)
            LOGGER.info("Updated %s in board member", mem['username'])


        # move lists to new board
        for list_name in reversed(BOARD_LISTS):
            list_id = get_list_id(bid, list_name)
            if list_id:
                move_list(new_bid, list_id)
                LOGGER.info("Moved %s list", list_name)
            else:
                LOGGER.error("No %s list", list_name)
    else:
        LOGGER.error("No prior board in " + organ_name)
