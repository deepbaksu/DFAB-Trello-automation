#_*_ coding: utf-8 _*_

import os
import json
import requests
import config
from query import QUERY

def get_board_id(organ_name, target_board_name):
    """Get target board id in given organization.

    Args:
        organ_name (str): organization name.
        target_board_name (str): board name.

    Returns:
        str: board id if it exists, else None.
    """
    url = os.path.join(config.TRELLO_API, 'organization', organ_name, 'boards')
    boards = requests.request("GET", url, params=QUERY)
    boards_jdata = json.loads(boards.text)

    for data in boards_jdata:
        if data['name'] == target_board_name:
            return data['id']

    return None


def get_list_id(bid, target_list_name):
    """Get list id in given board id.

    Args:
        bid (str): board id.
        target_list_name (str): list name.

    Returns:
        str: done list id if it exists, else None.
    """
    url = os.path.join(config.TRELLO_API, 'board', bid, 'lists')
    lists = requests.request("GET", url, params=QUERY)

    for list_data in json.loads(lists.text):
        if list_data['name'].encode() == target_list_name.encode():
            return list_data['id']

    return None


def get_the_number_of_card(lid):
    """Get the number of cards in given list id.

    Args:
        lid (str): list id.

    Returns:
        int: the number of done cards if they exist, else 0.
    """
    url = os.path.join(config.TRELLO_API, 'list', lid, 'cards?fields=all')
    cards_in_list = requests.request("GET", url, params=QUERY)
    return len(json.loads(cards_in_list.text))


def get_labels_data(bid):
    """Get labels in given board id.

    Args:
        bid (str): board id.

    Returns:
        list: labels data.
    """
    url = os.path.join(config.TRELLO_API, 'boards', bid, 'labels')
    res = requests.request("GET", url, params=QUERY)
    labels = json.loads(res.text)

    return labels


def create_list(bid, list_name, list_pos="bottom"):
    """Create list in given board id.

    Args:
        bid (str): board id.
        list_name (str): list name.
        list_pos (str): list position in board(default "bottom").

    Returns:
        str: created list id if it does not exist, else existing list id.
        bool: True for existing list, False new list.
    """
    existing_id = get_list_id(bid, list_name)
    if existing_id:
        return existing_id, True

    url = os.path.join(config.TRELLO_API, 'board', bid, 'lists')
    new_q = QUERY.copy()
    new_q['name'] = list_name
    new_q['pos'] = list_pos
    res = requests.request("POST", url, params=new_q)
    archive_list = json.loads(res.text)

    return archive_list['id'], False


def create_board(organ_name, board_name, default_list="false", board_pos="top", prefs_perm="org"):
    """Create board in given organization.

    Args:
        organ_name (str): organization name.
        board_name (str): board name.
        default_list (str): "false" for no default list, "true" for default list.
        board_pos (str): board position in organization(default "top").
        prefs_perm (str): prefs_permissionLevel(default "org").

    Returns:
        str: created board id if it does not exist, else existing board id.
        bool: True for existing board, False new board.
    """
    existing_id = get_board_id(organ_name, board_name)
    if existing_id:
        return existing_id, True

    url = os.path.join(config.TRELLO_API, 'boards')
    new_q = QUERY.copy()
    new_q['name'] = board_name
    new_q['idOrganization'] = organ_name
    new_q['defaultLists'] = default_list
    new_q['pos'] = board_pos
    new_q['prefs_permissionLevel'] = prefs_perm
    res = requests.request("POST", url, params=new_q)

    return json.loads(res.text)['id'], False


def move_all_cards(bid, from_lid, to_lid):
    """Move all cards from prior list to new list in given board id.

    Args:
        bid (str): board id.
        from_lid (str): prior list id.
        to_lid (str): new list id.
    """
    url = os.path.join(config.TRELLO_API, 'lists', from_lid, 'moveAllCards')
    new_q = QUERY.copy()
    new_q['idBoard'] = bid
    new_q['idList'] = to_lid
    requests.request("POST", url, params=new_q)


def update_board_label(bid, label_color, label_name):
    """Update board label name of color in given board.

    Args:
        bid (str): board id.
        label_color (str): label color.
        label_name (str): label name.
    """
    label_value = 'labelNames/' + label_color + '?value=' + label_name
    url = os.path.join(config.TRELLO_API, 'boards', bid, label_value)
    requests.request("PUT", url, params=QUERY)


def move_list(bid, lid):
    """Move list to another board.

    Args:
        bid (str): board id.
        lid (str): label id.
    """
    url = os.path.join(config.TRELLO_API, 'lists', lid, 'idBoard')
    new_q = QUERY.copy()
    new_q['value'] = bid
    requests.request("PUT", url, params=new_q)


def get_members_data(bid):
    """Get members in given board id.

    Args:
        bid (str): board id.

    Returns:
        list: members data.
    """
    url = os.path.join(config.TRELLO_API, 'boards', bid, 'members')
    mem_list = requests.request("GET", url, params=QUERY)
    return json.loads(mem_list.text)


def update_board_member(bid, mid, mem_type):
    """Update member in given board id.

    Args:
        bid (str): board id.
        mid (str): member id
        mem_type (str): member type.
    """
    url = os.path.join(config.TRELLO_API, 'boards', bid, 'members', mid)
    new_q = QUERY.copy()
    new_q['type'] = mem_type
    requests.request("PUT", url, params=new_q)


def compute_sprint_n(start_ym):
    """Compute sprint number.

    Args:
        start_ym (str): "year-month" of starting board.

    Returns:
        str: sprint_n.
    """
    start_y, start_m = start_ym.split('-')
    today_y, today_m = config.TODAY.strftime('%Y-%m').split('-')
    sprint_n = (int(today_y) - int(start_y)) * 12 + (int(today_m) - int(start_m)) + 1
    return sprint_n


def get_board_name(sprint_n, last_month=False):
    """Get board name.

    Args:
        sprint_n (int): sprint number.
        last_month (bool): False for this month board, True for last month board.

    Returns:
        str: board name.
    """
    if last_month:
        num = sprint_n - 1
        month = config.LAST_MONTH_NAME
    else:
        num = sprint_n
        month = config.MONTH_NAME

    return "Sprint" + str(num) + " for " + month + "."


def get_archive_name(last_month=False):
    """Get list name for archive

    Args:
        last_month (bool): False for this month board, True for last month board.

    Returns:
        str: archive list name
    """
    if last_month:
        m_name = config.LAST_MONTH_NAME
    else:
        m_name = config.MONTH_NAME
    return "아카이브(~ " + str(config.THE_DAY_BEFORE) + " " + m_name + ".)"
