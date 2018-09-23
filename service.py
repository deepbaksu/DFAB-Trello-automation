import json
import os

import requests

from common.exceptions import DuplicatedValueError


class TrelloResourceService:
    def __init__(self, base_url, tokens):
        self.base_url = base_url
        self.__params = tokens

    def get_board_id(self, organ_name, board_name):
        return self._get_id(self._organization_board_url(organ_name), board_name)

    def get_list_id(self, board_id, list_name):
        return self._get_id(self._list_url(board_id), list_name)

    def get_board_labels(self, board_id):
        return self._request_to_get(self._labels_url(board_id), self.__params)

    def get_board_members(self, board_id):
        return self._request_to_get(self._members_url(board_id), self.__params)

    def create_archived_list(self, board_id, list_name, list_pos="bottom"):
        list_id = self.get_list_id(board_id, list_name)
        if list_id:
            return list_id
        params = self.__params.copy()
        params['name'] = list_name
        params['pos'] = list_pos
        return self._request_to_post(self._list_url(board_id), params)['id']

    def create_sprint_board(self, organ_name, board_name, default_list="false", board_pos="top", prefs_perm="org"):
        params = self.__params.copy()
        params['name'] = board_name
        params['idOrganization'] = organ_name
        params['defaultLists'] = default_list
        params['pos'] = board_pos
        params['prefs_permissionLevel'] = prefs_perm
        return self._request_to_post(self._base_board_url(), params)['id']

    def move_done_cards(self, board_id, from_list_id, to_list_id):
        params = self.__params.copy()
        params['idBoard'] = board_id
        params['idList'] = to_list_id
        return self._request_to_post(self._move_all_cards_url(from_list_id), params)

    def _get_id(self, url, target):
        resp_data = self._request_to_get(url, self.__params)
        data_ids = [data['id'] for data in resp_data if data['name'] == target]

        if len(data_ids) == 1:
            return data_ids[0]
        if len(data_ids) > 1:
            raise DuplicatedValueError('{} 2개 이상 존재합니다.'.format(target))
        None

    def _organization_board_url(self, organ_name):
        return os.path.join(self.base_url, 'organization', organ_name, 'boards')

    def _base_board_url(self):
        return os.path.join(self.base_url, 'boards')

    def _list_url(self, board_id):
        return os.path.join(self._base_board_url(), board_id, 'lists')

    def _move_all_cards_url(self, list_id):
        return os.path.join(self.base_url, 'lists', list_id, 'moveAllCards')

    def _labels_url(self, board_id):
        return os.path.join(self._base_board_url(), board_id, 'labels')

    def _members_url(self, board_id):
        return os.path.join(self._base_board_url(), board_id, 'members')

    def _request_to_get(self, url, params):
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return self._convert_json(resp.text)

    def _request_to_post(self, url, params):
        resp = requests.post(url, params=params)
        resp.raise_for_status()
        return self._convert_json(resp.text)

    def _request_to_put(self, url, params):
        resp = requests.put(url, params=params)
        resp.raise_for_status()
        return self._convert_json(resp.text)

    def _convert_json(self, text_data):
        return json.loads(text_data)
