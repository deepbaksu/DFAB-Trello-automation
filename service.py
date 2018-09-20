import os
import requests
import json
from common.exceptions import DuplicatedValueError

class TrelloResourceService:
    def __init__(self, base_url, tokens):
        self.base_url = base_url
        self.__params = tokens

    def get_board_id(self, organ_name, board_name):
        return self._get_id(self._make_board_url(organ_name), board_name)
        
    def _get_id(self, url, target):
        resp_data = self._request_to_get(url, self.__params)
        data_ids = [data['id'] for data in resp_data if data['name'] == target]

        if len(data_ids) == 1:
            return data_ids[0]

        if len(data_ids) > 1:
            raise DuplicatedValueError('{} 2개 이상 존재합니다.'.format(target))

        raise ValueError('{} 존재하지 않습니다.'.format(target))

    def _make_board_url(self, organ_name):
        return os.path.join(self.base_url, 'organization', organ_name, 'boards')

    def _request_to_get(self, url, params):
        return self._convert_json(requests.get(url, params=params).text)

    def _request_to_post(self, url, params):
        return self._convert_json(requests.post(url, params=params).text)

    def _request_to_put(self, url, params):
        return self._convert_json(requests.put(url, params=params).text)

    def _convert_json(self, text_data):
        return json.loads(text_data)
