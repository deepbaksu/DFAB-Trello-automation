#!/usr/bin/python

import sys
sys.path.append('./')
import unittest
import mock
import json
from service import TrelloResourceService
from lib.config import TRELLO_API
from requests.exceptions import HTTPError
from common.exceptions import DuplicatedValueError

class TestTrelloResourceService(unittest.TestCase):
    def setUp(self):
        self.service = TrelloResourceService(TRELLO_API, {'key': 'key', 'token': 'token'})
        self.organ_name = 'test_organization'
        self.board_name = 'test_board'
        self.list_name = 'test_list'
        self.url = 'http://test.url.com'

    @mock.patch('requests.get')
    def test_get_board_id(self, mock_req):
        resp_data = [{'name': self.board_name + '1', 'id': 'anotherBoardId'},
                     {'name': self.board_name, 'id': 'boardId'}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.get_board_id(self.organ_name, self.board_name), resp_data[1]['id'])

    @mock.patch('requests.get')
    def test_failed_get_board_id(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.get_board_id, self.organ_name, self.board_name)

    @mock.patch('requests.get')
    def test_not_exist_board_id(self, mock_req):
        self._mock_request(mock_req=mock_req, resp_data=[])
        self.assertIsNone(self.service.get_board_id(self.organ_name, self.board_name))

    @mock.patch('requests.get')
    def test_failed_exist_multi_board_ids(self, mock_req):
        resp_data = [{'name': self.board_name, 'id': 'boardId'}, {'name': self.board_name, 'id': 'boardId'}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertRaises(DuplicatedValueError, self.service.get_board_id, self.organ_name, self.board_name)

    @mock.patch('requests.get')
    def test_get_list_id(self, mock_req):
        resp_data = [{'name': self.list_name + '1', 'id': 'anotherListId'}, {'name': self.list_name, 'id': 'listId'}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.get_list_id('1', self.list_name), resp_data[1]['id'])

    @mock.patch('requests.get')
    def test_failed_get_list_id(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.get_list_id, 'boardId', self.list_name)

    @mock.patch('requests.get')
    def test_not_exist_list_id(self, mock_req):
        self._mock_request(mock_req=mock_req, resp_data=[])
        self.assertIsNone(self.service.get_list_id('1', self.list_name))

    @mock.patch('requests.get')
    def test_failed_exist_multi_list_ids(self, mock_req):
        resp_data = [{'name': self.list_name, 'id': 'listId'}, {'name': self.list_name, 'id': 'listId'}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertRaises(DuplicatedValueError, self.service.get_list_id, 'boardId', self.list_name)

    @mock.patch('requests.get')
    def test_get_board_labels(self, mock_req):
        resp_data = ['labels_data']
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.get_board_labels('boardId'), resp_data)

    @mock.patch('requests.get')
    def test_failed_get_board_labels(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.get_board_labels, 'boardId')

    @mock.patch('requests.get')
    def test_get_board_members(self, mock_req):
        resp_data = ['members_data']
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.get_board_members('boardId'), resp_data)

    @mock.patch('requests.get')
    def test_failed_get_board_labels(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.get_board_members, 'boardId')

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_create_archived_list(self, mock_get_req, mock_post_req):
        resp_data = {'name': self.list_name, 'id': 'listId'}
        self._mock_request(mock_req=mock_get_req, resp_data=[])
        self._mock_request(mock_req=mock_post_req, resp_data=resp_data)
        self.assertEqual(self.service.create_archived_list('boardId', self.list_name), resp_data['id'])

    @mock.patch('requests.get')
    def test_exist_archived_list(self, mock_req):
        resp_data = [{'name': self.list_name, 'id': 'listId'}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.create_archived_list('boardId', self.list_name), resp_data[0]['id'])

    @mock.patch('requests.get')
    def test_failed_exist_archived_list(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.create_archived_list, 'boardId', self.list_name)

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_failed_create_archived_list(self, mock_get_req, mock_post_req):
        self._mock_request(mock_req=mock_get_req, resp_data=[])
        self._mock_request_http_error(mock_post_req)
        self.assertRaises(HTTPError, self.service.create_archived_list, 'boardId', self.list_name)

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_create_sprint_board(self, mock_get_req, mock_post_req):
        resp_data = {'name': self.board_name, 'id': 'boardId'}
        self._mock_request(mock_req=mock_get_req, resp_data=[])
        self._mock_request(mock_req=mock_post_req, resp_data=resp_data)
        self.assertEqual(self.service.create_sprint_board(self.organ_name, self.board_name), resp_data['id'])

    @mock.patch('requests.get')
    def test_exist_sprint_board(self, mock_get_req):
        resp_data = [{'name': self.list_name, 'id': 'boardId'}]
        self._mock_request(mock_req=mock_get_req, resp_data=resp_data)
        self.assertEqual(self.service.create_archived_list('boardId', self.list_name), resp_data[0]['id'])

    @mock.patch('requests.get')
    def test_failed_exist_sprint_board(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.create_archived_list, '1', self.list_name)

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_failed_create_sprint_board(self, mock_get_req, mock_post_req):
        self._mock_request(mock_req=mock_get_req, resp_data=[])
        self._mock_request_http_error(mock_post_req)
        self.assertRaises(HTTPError, self.service.create_archived_list, 'boardId', self.list_name)

    @mock.patch('requests.post')
    def test_move_done_cards(self, mock_req):
        resp_data = [{'idList': 'toListId'}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.move_done_cards('boardId', 'fromListId', 'toListId'), resp_data)

    @mock.patch('requests.post')
    def test_failed_move_done_cards(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.move_done_cards, 'boardId', 'fromListId', 'toListId')

    # Todo: test case가 너무 많은데 resource request 객체를 빼서 테스트 따로 할까 생각 중(500에 대한 error는 여기서 안해도 되자나 request 별로 한번씩만 하면 되자너)
    # Todo: url에 대한 test 추가

    def _mock_request(self, mock_req, resp_data="[]", status_code=200, raise_for_status=None):
        mock_resp = mock.Mock()
        mock_resp.raise_for_status = mock.Mock()

        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status

        mock_resp.text = json.dumps(resp_data)
        mock_resp.status_code = status_code

        mock_req.return_value = mock_resp

    def _mock_request_http_error(self, mock_req):
        self._mock_request(mock_req=mock_req, status_code=500, raise_for_status=HTTPError('Trello API is not working'))

if __name__ == '__main__':
    unittest.main()
