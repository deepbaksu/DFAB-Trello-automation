#_*_ coding: utf-8 _*_

import requests
import json
import os
from query import QUERY
import config

def get_tboard_id(organ_name, target_board_name):
    url = os.path.join(config.TRELLO_API, 'organization', organ_name, 'boards')
    boards = requests.request("GET", url, params=QUERY)
    boards_jdata = json.loads(boards.text)

    for jd in boards_jdata:
        if jd['name'] == target_board_name:
            return jd['id']

    return None

def search_done_list(bid):
    url = os.path.join(config.TRELLO_API, 'board', bid, 'lists')
    lists = requests.request("GET", url, params=QUERY)

    for l in json.loads(lists.text):
        if l['name'].encode() == config.TARGET_LIST.encode():
            url = os.path.join(config.TRELLO_API, 'list', l['id'], 'cards?fields=all')
            cards_in_list = requests.request("GET", url, params=QUERY)
            return l['id'], len(json.loads(cards_in_list.text))

    return None, 0
        
def create_archive_list(bid, last_month=False):
    url = os.path.join(config.TRELLO_API, 'board', bid, 'lists')
    new_q = QUERY.copy()

    if last_month:
        m_name = config.LAST_MONTH_NAME
    else:
        m_name = config.MONTH_NAME

    new_q['name'] = "아카이브(~ " + str(config.THE_DAY_BEFORE) + " " + m_name + ".)"
    new_q['pos'] = "bottom"
    existance = get_list_ids(bid, [new_q['name']])

    if not existance:
        res = requests.request("POST", url, params=new_q)
        archive_list = json.loads(res.text)
        return archive_list['id']
    else:
        return existance[0]

def move_all_cards(did, id_board, id_list):
    url = os.path.join(config.TRELLO_API, 'lists', did, 'moveAllCards')
    new_q = QUERY.copy()
    new_q['idBoard'] = id_board
    new_q['idList'] = id_list
    res = requests.request("POST", url, params=new_q)

def get_board_labels(bid):
    result = []
    url = os.path.join(config.TRELLO_API, 'boards', bid, 'labels')
    res = requests.request("GET", url, params=QUERY)
    labels = json.loads(res.text)

    for l in labels:
        dic = {}
        dic['name'] = l['name']
        dic['color'] = l['color']
        result.append(dic)

    return result

def create_board(n, organ_name, team_visible=True):
    url = os.path.join(config.TRELLO_API, 'boards')
    new_q = QUERY.copy()
    new_q['name'] =  "Sprint" + str(n) + " for " + config.MONTH_NAME + "."
    existance_id = get_tboard_id(organ_name, new_q['name'])

    if existance_id:
        return existance_id, new_q['name'], True

    if team_visible:
        new_q['prefs_permissionLevel'] = 'org'

    new_q['idOrganization'] = organ_name
    new_q['defaultLists'] = "false"
    new_q['pos'] = "top"
    res = requests.request("POST", url, params=new_q)

    return json.loads(res.text)['id'], new_q['name'], False

def update_board_labels(new_bid, labels):
    for l in labels:
        label_value = 'labelNames/' + l['color'] + '?value=' + l['name']
        url = os.path.join(config.TRELLO_API, 'boards', new_bid, label_value)
        res = requests.request("PUT", url, params=QUERY)

def get_list_ids(bid, board_lists):
    list_ids = []
    url = os.path.join(config.TRELLO_API, 'boards', bid, 'lists')
    board_lists = [ board_list.encode() for board_list in board_lists ]
    res = requests.request("GET", url, params=QUERY)
    blists = json.loads(res.text)
    
    for bl in blists:
        if bl['name'].encode() in board_lists:
            list_ids.append(bl['id'])

    return list_ids
    
def move_lists(list_ids, new_bid):
    list_ids.reverse()
    for lid in list_ids:
        url = os.path.join(config.TRELLO_API, 'lists', lid, 'idBoard')
        new_q = QUERY.copy()
        new_q['value'] = new_bid
        res = requests.request("PUT", url, params=new_q)

def get_members(bid):
    mem_ids, admin_id = [], None
    url = os.path.join(config.TRELLO_API, 'boards', bid, 'members')
    res = requests.request("GET", url, params=QUERY)
    memlists = json.loads(res.text)

    for mem in memlists:
        mem_ids.append(mem['id'])
        if mem['username'] == config.ADMIN_USER_NAME:
            admin_id = mem['id']

    return mem_ids, admin_id

def update_board_members(bid, mem_ids, admin_id):
    new_q = QUERY.copy()
    for mid in mem_ids:
        if admin_id and mid == admin_id:
            new_q['type'] = 'admin'
        else:
            new_q['type'] = 'normal'
        url = os.path.join(config.TRELLO_API, 'boards', bid, 'members', mid)
        res = requests.request("PUT", url, params=new_q)

def compute_sprint_n(start_ym):
    sy, sm = start_ym.split('-')    
    ty, tm = config.TODAY.strftime('%Y-%m').split('-')
    n = (int(ty) - int(sy)) * 12 + (int(tm) - int(sm)) + 1
    return n

def get_tboard_name(team, last_month=False):
    info = config.TEAM_INFO[team]
    n = compute_sprint_n(info['start_ym'])

    if last_month:
        board_name = "Sprint" + str(n-1) + " for " + config.LAST_MONTH_NAME + "." 
    else:
        board_name = "Sprint" + str(n) + " for " + config.MONTH_NAME + "." 

    return board_name
        
