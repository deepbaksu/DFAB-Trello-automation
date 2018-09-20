#!/usr/bin/python

import sys
sys.path.append('./')
import unittest
import mock
import json
from service import TrelloResourceService
from lib.config import TRELLO_API

class TestTrelloResourceService(unittest.TestCase):
    def setUp(self):
        self.service = TrelloResourceService(TRELLO_API)
        self.resp_data = "[{'test': 'test'}]"
        self.url = 'http://test.url.com'
        self.params = 'params'

    @mock.patch('requests.get')
    def test_request_get_data(self, mock_req):
        mock_req.return_value = self._mock_resp(self.resp_data)
        self.assertEqual(self.service.request_to_get(self.url, self.params), self.resp_data)

    @mock.patch('requests.post')
    def test_create_list(self, mock_req):
        mock_req.return_value = self._mock_resp(self.resp_data)
        self.assertEqual(self.service.request_to_post(self.url, self.params), self.resp_data)

    @mock.patch('requests.put')
    def test_create_list(self, mock_req):
        mock_req.return_value = self._mock_resp(self.resp_data)
        self.assertEqual(self.service.request_to_put(self.url, self.params), self.resp_data)

    def _mock_resp(self, resp_data, status_code=200):
        mock_resp = mock.Mock()
        mock_resp.status_code = status_code
        mock_resp.text = json.dumps(resp_data)
        return mock_resp

if __name__ == '__main__':
    unittest.main()
