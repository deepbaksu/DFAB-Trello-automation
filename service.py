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
        return self._request_to_get(self._base_members_url(board_id), self.__params)

    def create_archived_list(self, board_id, list_name, list_pos="bottom"):
        list_id = self.get_list_id(board_id, list_name)
        if list_id:
            return list_id

        params = self._update_params({'name': list_name, 'pos': list_pos})
        return self._request_to_post(self._list_url(board_id), params)['id']

    def create_sprint_board(self, organ_name, board_name, default_list="false", board_pos="top", prefs_perm="org"):
        board_id = self.get_board_id(organ_name, board_name)
        if board_id:
            return board_id

        params = self._update_params({'name': board_name, 'idOrganization': organ_name,
                                      'defaultLists': default_list, 'pos': board_pos,
                                      'prefs_permissionLevel': prefs_perm})
        return self._request_to_post(self._base_board_url(), params)['id']

    def move_done_cards(self, board_id, from_list_id, to_list_id):
        params = self._update_params({'idBoard': board_id, 'idList': to_list_id})
        self._request_to_post(self._move_all_cards_url(from_list_id), params)

    def update_board_labels(self, board_id, labels_data):
        if labels_data != [data for data in labels_data if ('color' in data and 'name' in data)]:
            raise ValueError('Wrong labels_data')

        params_data = {'labelNames/' + label['color']: label['name'] for label in labels_data}
        params = self._update_params(params_data)
        self._request_to_put(self._base_board_id_url(board_id), params)

    def update_board_member(self, board_id, member_id, member_type):
        params = self._update_params({'type': member_type})
        self._request_to_put(self._members_url(board_id, member_id), params)

    def move_list(self, board_id, list_id):
        params = self._update_params({'value': board_id})
        self._request_to_put(self._move_list_url(list_id), params)

    def _get_id(self, url, target):
        resp_data = self._request_to_get(url, self.__params)
        data_ids = [data['id'] for data in resp_data if data['name'] == target]

        if len(data_ids) == 1:
            return data_ids[0]
        if len(data_ids) > 1:
            raise DuplicatedValueError('{} has more than two id.'.format(target))
        None

    def _update_params(self, params_data={}):
        params = self.__params.copy()
        params.update(params_data)
        return params

    def _organization_board_url(self, organ_name):
        return os.path.join(self.base_url, 'organization', organ_name, 'boards')

    def _base_board_url(self):
        return os.path.join(self.base_url, 'boards')

    def _base_board_id_url(self, board_id):
        return os.path.join(self.base_url, 'boards', board_id)

    def _base_list_id_url(self, list_id):
        return os.path.join(self.base_url, 'lists', list_id)

    def _list_url(self, board_id):
        return os.path.join(self._base_board_id_url(board_id), 'lists')

    def _move_all_cards_url(self, list_id):
        return os.path.join(self._base_list_id_url(list_id), 'moveAllCards')

    def _labels_url(self, board_id):
        return os.path.join(self._base_board_id_url(board_id), 'labels')

    def _base_members_url(self, board_id):
        return os.path.join(self._base_board_id_url(board_id), 'members')

    def _members_url(self, board_id, member_id):
        return os.path.join(self._base_members_url(board_id), member_id)

    def _move_list_url(self, list_id):
        return os.path.join(self._base_list_id_url(list_id), 'idBoard')

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
