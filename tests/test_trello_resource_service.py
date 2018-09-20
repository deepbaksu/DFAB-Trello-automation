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
        self.list_name = 'test_list'
        self.url = 'http://test.url.com'

    @mock.patch('requests.get')
    def test_get_board_id(self, mock_req):
        resp_data = [{'name': self.board_name + '1', 'id': '1'}, {'name': self.board_name, 'id': '2'}]
        self._mock_request(mock_req, resp_data)
        self.assertEqual(self.service.get_board_id(self.organ_name, self.board_name), '2')

    @mock.patch('requests.get')
    def test_failed_not_exist_board_id(self, mock_req):
        self._mock_request(mock_req, [])
        self.assertRaises(ValueError, self.service.get_board_id, self.organ_name, self.board_name)

    @mock.patch('requests.get')
    def test_failed_exist_multi_board_ids(self, mock_req):
        resp_data = [{'name': self.board_name, 'id': '1'}, {'name': self.board_name, 'id': '2'}]
        self._mock_request(mock_req, resp_data)
        self.assertRaises(DuplicatedValueError, self.service.get_board_id, self.organ_name, self.board_name)

    @mock.patch('requests.get')
    def test_get_list_id(self, mock_req):
        resp_data = [{'name': self.list_name + '1', 'id': '1'}, {'name': self.list_name, 'id': '2'}]
        self._mock_request(mock_req, resp_data)
        self.assertEqual(self.service.get_list_id('1', self.list_name), '2')

    @mock.patch('requests.get')
    def test_get_list_id(self, mock_req):
        resp_data = [{'name': self.list_name + '1', 'id': '1'}, {'name': self.list_name, 'id': '2'}]
        self._mock_request(mock_req, resp_data)
        self.assertEqual(self.service.get_list_id('1', self.list_name), '2')

    @mock.patch('requests.get')
    def test_failed_not_exist_list_id(self, mock_req):
        self._mock_request(mock_req, [])
        self.assertRaises(ValueError, self.service.get_list_id, '1', self.list_name)

    @mock.patch('requests.get')
    def test_failed_exist_multi_list_ids(self, mock_req):
        resp_data = [{'name': self.list_name, 'id': '1'}, {'name': self.list_name, 'id': '2'}]
        self._mock_request(mock_req, resp_data)
        self.assertRaises(DuplicatedValueError, self.service.get_list_id, '1', self.list_name)

    @mock.patch('requests.get')
    def test_get_board_labels(self, mock_req):
        resp_data = ['labels_data']
        self._mock_request(mock_req, resp_data)
        self.assertEqual(self.service.get_board_labels('1'), resp_data)

    @mock.patch('requests.get')
    def test_get_board_members(self, mock_req):
        resp_data = ['members_data']
        self._mock_request(mock_req, resp_data)
        self.assertEqual(self.service.get_board_members('1'), resp_data)

    def _mock_request(self, mock_req, resp_data, status_code=200):
        mock_resp = mock.Mock()
        mock_resp.status_code = status_code
        mock_resp.text = json.dumps(resp_data)
        mock_req.return_value = mock_resp

if __name__ == '__main__':
    unittest.main()
