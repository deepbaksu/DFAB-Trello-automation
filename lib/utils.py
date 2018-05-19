#_*_ coding: utf-8 _*_

import requests
import json
from query import *
from config import *

def get_tboard_id(organ_name, target_board_name):
    url = "https://api.trello.com/1/organization/" + organ_name + "/boards"
    boards = requests.request("GET", url, params=QUERY)
    boards_jdata = json.loads(boards.text)
    for jd in boards_jdata:
        if jd['name'] == target_board_name:
            return jd['id']
    return None

def search_done_list(bid):
    url = "https://api.trello.com/1/boards/"+bid+"/lists"
    lists = requests.request("GET", url, params=QUERY)
    for l in json.loads(lists.text):
        if l['name'] == TARGET_LIST:
            url = "https://api.trello.com/1/lists/"+l['id']+"/cards?fields=all"
            cards_in_list = requests.request("GET", url, params=QUERY)
            return l['id'], len(json.loads(cards_in_list.text))
    return None, 0
        
def create_archive_list(bid, last_month=False):
    url = "https://api.trello.com/1/boards/"+bid+"/lists"
    new_q = QUERY.copy()
    if last_month:
        m_name = LAST_MONTH_NAME
    else:
        m_name = MONTH_NAME
    new_q['name'] = "아카이브(~ " + str(THE_DAY_BEFORE) + " " + m_name + ".)"
    new_q['pos'] = "bottom"
    existance = get_list_ids(bid, [new_q['name']])
    if not existance:
        res = requests.request("POST", url, params=new_q)
        archive_list = json.loads(res.text)
        return archive_list['id']
    else:
        return existance[0]

def move_all_cards(did, idBoard, idList):
    url = "https://api.trello.com/1/lists/" + did + "/moveAllCards"
    new_q = QUERY.copy()
    new_q['idBoard'] = idBoard
    new_q['idList'] = idList
    res = requests.request("POST", url, params=new_q)

def compute_sprint_n(start_ym):
    sy, sm = start_ym.split('-')    
    ty, tm = TODAY.strftime('%Y-%m').split('-')
    n = (int(ty) - int(sy)) * 12 + (int(tm) - int(sm)) + 1
    return n

def get_tboard_name(team, last_month=False):
    info = TEAM_INFO[team]
    n = compute_sprint_n(info['start_ym'])

    if last_month:
        board_name = "Sprint" + str(n-1) + " for " + LAST_MONTH_NAME + "." 
    else:
        board_name = "Sprint" + str(n) + " for " + MONTH_NAME + "." 

    return board_name
        
def get_board_labels(bid):
    result = []
    url = "https://api.trello.com/1/boards/"+ bid + "/labels"
    res = requests.request("GET", url, params=QUERY)
    labels = json.loads(res.text)

    for l in labels:
        dic = {}
        dic['name'] = l['name']
        dic['color'] = l['color']
        result.append(dic)

    return result

def create_board(n, organ_name):
    url = "https://api.trello.com/1/boards/"
    new_q = QUERY.copy()
    new_q['name'] =  "Sprint" + str(n) + " for " + MONTH_NAME + "."
    existance = get_tboard_id(organ_name, new_q['name'])
    if existance:
        return existance[0], new_q['name'], existance

    new_q['idOrganization'] = organ_name
    new_q['defaultLists'] = "false"
    new_q['pos'] = "top"
    res = requests.request("POST", url, params=new_q)
    return json.loads(res.text)['id'], new_q['name'], existance

def update_board_labels(new_bid, labels):
    for l in labels:
        url = "https://api.trello.com/1/boards/" + new_bid + "/labels/"
        new_q = QUERY.copy()
        new_q['name'] = l['name']
        new_q['color'] = l['color']
        res = requests.request("POST", url, params=new_q)

def get_list_ids(bid, board_lists):
    list_ids = []
    url = "https://api.trello.com/1/boards/" + bid + "/lists"
    res = requests.request("GET", url, params=QUERY)
    blists = json.loads(res.text)
    
    for bl in blists:
        if bl['name'] in board_lists:
            list_ids.append(bl['id'])

    return list_ids
    
def move_lists(list_ids, new_bid):
    list_ids.reverse()
    for lid in list_ids:
        url = "https://api.trello.com/1/lists/" + lid + "/idBoard"  
        new_q = QUERY.copy()
        new_q['value'] = new_bid
        res = requests.request("PUT", url, params=new_q)

def get_members(bid):
    mem_ids, admin_id = [], None
    url = "https://api.trello.com/1/boards/" + bid + "/members"
    res = requests.request("GET", url, params=QUERY)
    memlists = json.loads(res.text)

    for mem in memlists:
        mem_ids.append(mem['id'])
        if mem['username'] == ADMIN_USER_NAME:
            admin_id = mem['id']

    return mem_ids, admin_id

def update_board_members(bid, mem_ids, admin_id):
    new_q = QUERY.copy()
    for mid in mem_ids:
        if admin_id and mid == admin_id:
            new_q['type'] = 'admin'
        else:
            new_q['type'] = 'normal'
        url = "https://api.trello.com/1/boards/" + bid + "/members/" + mid
        res = requests.request("PUT", url, params=new_q)
