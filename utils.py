#_*_ coding: utf-8 _*_

import requests
import json
from config import *

def get_tboard_id(organ_name, target_board_name, query):
    url = "https://api.trello.com/1/organization/" + organ_name + "/boards"
    boards = requests.request("GET", url, params=query)
    boards_jdata = json.loads(boards.text)
    for jd in boards_jdata:
        if jd['name'] == target_board_name:
            return jd['id']
    return None

def search_done_list(bid, query):
    url = "https://api.trello.com/1/boards/"+bid+"/lists"
    lists = requests.request("GET", url, params=query)
    for l in json.loads(lists.text):
        if l['name'] == target_list:
            url = "https://api.trello.com/1/lists/"+l['id']+"/cards?fields=all"
            cards_in_list = requests.request("GET", url, params=query)
            return l['id'], len(json.loads(cards_in_list.text))
    return None, 0
        
def create_archive_list(bid, month_name, date, query):
    url = "https://api.trello.com/1/boards/"+bid+"/lists"
    new_q = query.copy()
    new_q['name'] = "아카이브(~ " + str(date) + " " + month_name + ".)"
    new_q['pos'] = "bottom"
    existance = get_list_ids(bid, [new_q['name']], query)
    if not existance:
        res = requests.request("POST", url, params=new_q)
        archive_list = json.loads(res.text)
        return archive_list['id']
    else:
        return existance[0]

def move_all_cards(did, idBoard, idList, query):
    url = "https://api.trello.com/1/lists/" + did + "/moveAllCards"
    new_q = query.copy()
    new_q['idBoard'] = idBoard
    new_q['idList'] = idList
    res = requests.request("POST", url, params=new_q)
    print(res)

def compute_sprint_n(start_ym, today):
    sy, sm = start_ym.split('-')    
    ty, tm = today.strftime('%Y-%m').split('-')
    n = (int(ty) - int(sy)) * 12 + (int(tm) - int(sm)) + 1
    return n

def get_tboard_name(team, month_name):
    info = team_info[team]
    n = compute_sprint_n(info['start_ym'], today)
    board_name = "Sprint" + str(n) + " for " + month_name + "." 

    return board_name
        
def get_board_labels(bid, query):
    result = []
    url = "https://api.trello.com/1/boards/"+ bid + "/labels"
    res = requests.request("GET", url, params=query)
    labels = json.loads(res.text)

    for l in labels:
        dic = {}
        dic['name'] = l['name']
        dic['color'] = l['color']
        result.append(dic)

    return result

def create_board(n, month_name, organ_name, query):
    url = "https://api.trello.com/1/boards/"
    new_q = query.copy()
    new_q['name'] =  "Sprint" + str(n) + " for " + month_name + "."
    existance = get_tboard_id(organ_name, new_q['name'], query)
    if existance:
        return existance[0], new_q['name']

    new_q['idOrganization'] = organ_name
    new_q['defaultLists'] = "false"
    new_q['pos'] = "top"
    res = requests.request("POST", url, params=new_q)
    return json.loads(res.text)['id'], new_q['name']

def update_board_labels(new_bid, labels, query):
    for l in labels:
        url = "https://api.trello.com/1/boards/" + new_bid + "/labels/"
        new_q = query.copy()
        new_q['name'] = l['name']
        new_q['color'] = l['color']
        res = requests.request("POST", url, params=new_q)

def get_list_ids(bid, board_lists, query):
    list_ids = []
    url = "https://api.trello.com/1/boards/" + bid + "/lists"
    res = requests.request("GET", url, params=query)
    blists = json.loads(res.text)
    
    for bl in blists:
        if bl['name'] in board_lists:
            list_ids.append(bl['id'])

    return list_ids
    
def move_lists(list_ids, new_bid, query):
    list_ids.reverse()
    for lid in list_ids:
        url = "https://api.trello.com/1/lists/" + lid + "/idBoard"  
        new_q = query.copy()
        new_q['value'] = new_bid
        res = requests.request("PUT", url, params=new_q)
        print(res.text)
