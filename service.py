import requests
import json

class TrelloResourceService:
    def __init__(self, base_url):
        self.base_url = base_url

    def request_to_get(self, url, params):
        return self._convert_json(requests.get(url, params=params).text)

    def request_to_post(self, url, params):
        return self._convert_json(requests.post(url, params=params).text)

    def request_to_put(self, url, params):
        return self._convert_json(requests.put(url, params=params).text)

    def _convert_json(self, text_data):
        return json.loads(text_data)
