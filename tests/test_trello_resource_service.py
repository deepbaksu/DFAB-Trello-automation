#!/usr/bin/python

import sys
sys.path.append('./')
import unittest
import mock
import json
from service import TrelloResourceService
from lib.config import TRELLO_API
from common.exceptions import DuplicatedValueError

class TestTrelloResourceService(unittest.TestCase):
    def setUp(self):
        self.service = TrelloResourceService(TRELLO_API, 'tokens')
        self.organ_name = 'test_organization'
        self.board_name = 'test_board'
        self.url = 'http://test.url.com'

    @mock.patch('requests.get')
    def test_get_board_id(self, mock_req):
        resp_data = [{'name': 'Sprint5 for Sep.', 'id': '1'}, {'name': self.board_name, 'id': '2'}]
        mock_req.return_value = self._mock_resp(resp_data)
        self.assertEqual(self.service.get_board_id(self.organ_name, self.board_name), '2')

    @mock.patch('requests.get')
    def test_not_exist_board_id(self, mock_req):
        mock_req.return_value = self._mock_resp([])
        self.assertRaises(ValueError, self.service.get_board_id, self.organ_name, self.board_name)

    @mock.patch('requests.get')
    def test_exist_multi_board_ids(self, mock_req):
        resp_data = [{'name': self.board_name, 'id': '1'}, {'name': self.board_name, 'id': '2'}]
        mock_req.return_value = self._mock_resp(resp_data)
        self.assertRaises(DuplicatedValueError, self.service.get_board_id, self.organ_name, self.board_name)

    def _mock_resp(self, resp_data, status_code=200):
        mock_resp = mock.Mock()
        mock_resp.status_code = status_code
        mock_resp.text = json.dumps(resp_data)
        return mock_resp

if __name__ == '__main__':
    unittest.main()
