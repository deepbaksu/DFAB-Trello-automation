#!/usr/bin/python

import sys
sys.path.append('./')
import unittest
import mock
import json
from service import TrelloResourceService
from requests.exceptions import HTTPError
from common.exceptions import DuplicatedValueError

class TestTrelloResourceService(unittest.TestCase):
    def setUp(self):
        self.params = {'key': 'key', 'token': 'token'}
        self.url = 'http://test.url.com'
        self.service = TrelloResourceService(self.url, self.params)
        self.organ_name = 'test_organization'
        self.board_name = 'test_board'
        self.list_name = 'test_list'
        self.board_id = 'boardId'

    @mock.patch('requests.get')
    def test_get_board_id(self, mock_req):
        resp_data = [{'name': self.board_name + '1', 'id': 'anotherBoardId'},
                     {'name': self.board_name, 'id': self.board_id}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.get_board_id(self.organ_name, self.board_name), resp_data[1]['id'])
        mock_req.assert_called_with('{}/organization/{}/boards'.format(self.url, self.organ_name), params=self.params)

    @mock.patch('requests.get')
    def test_failed_get_board_id(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.get_board_id, self.organ_name, self.board_name)
        mock_req.assert_called_with('{}/organization/{}/boards'.format(self.url, self.organ_name), params=self.params)

    @mock.patch('requests.get')
    def test_not_exist_board_id(self, mock_req):
        self._mock_request(mock_req=mock_req, resp_data=[])
        self.assertIsNone(self.service.get_board_id(self.organ_name, self.board_name))
        mock_req.assert_called_with('{}/organization/{}/boards'.format(self.url, self.organ_name), params=self.params)

    @mock.patch('requests.get')
    def test_failed_exist_multi_board_ids(self, mock_req):
        resp_data = [{'name': self.board_name, 'id': self.board_id}, {'name': self.board_name, 'id': self.board_id}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertRaises(DuplicatedValueError, self.service.get_board_id, self.organ_name, self.board_name)
        mock_req.assert_called_with('{}/organization/{}/boards'.format(self.url, self.organ_name), params=self.params)

    @mock.patch('requests.get')
    def test_get_list_id(self, mock_req):
        resp_data = [{'name': self.list_name + '1', 'id': 'anotherListId'}, {'name': self.list_name, 'id': 'listId'}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.get_list_id(self.board_id, self.list_name), resp_data[1]['id'])
        mock_req.assert_called_with('{}/boards/{}/lists'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.get')
    def test_failed_get_list_id(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.get_list_id, self.board_id, self.list_name)
        mock_req.assert_called_with('{}/boards/{}/lists'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.get')
    def test_not_exist_list_id(self, mock_req):
        self._mock_request(mock_req=mock_req, resp_data=[])
        self.assertIsNone(self.service.get_list_id(self.board_id, self.list_name))
        mock_req.assert_called_with('{}/boards/{}/lists'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.get')
    def test_failed_exist_multi_list_ids(self, mock_req):
        resp_data = [{'name': self.list_name, 'id': 'listId'}, {'name': self.list_name, 'id': 'listId'}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertRaises(DuplicatedValueError, self.service.get_list_id, self.board_id, self.list_name)
        mock_req.assert_called_with('{}/boards/{}/lists'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.get')
    def test_get_board_labels(self, mock_req):
        resp_data = [{'name': 'greenLabel', 'color': 'green'}, {'name': 'yellowLabel', 'color': 'yellow'}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.get_board_labels(self.board_id), resp_data)
        mock_req.assert_called_with('{}/boards/{}/labels'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.get')
    def test_failed_get_board_labels(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.get_board_labels, self.board_id)
        mock_req.assert_called_with('{}/boards/{}/labels'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.get')
    def test_get_board_members(self, mock_req):
        resp_data = [{'id': 'memberId1', 'username': 'normalMember'}, {'id': 'memberId2', 'username': 'adminMember'}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.get_board_members(self.board_id), resp_data)
        mock_req.assert_called_with('{}/boards/{}/members'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.get')
    def test_failed_get_board_labels(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.get_board_members, self.board_id)
        mock_req.assert_called_with('{}/boards/{}/members'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_create_archived_list(self, mock_get_req, mock_post_req):
        list_id = 'listId'
        resp_data = {'name': self.list_name, 'id': list_id}
        self._mock_request(mock_req=mock_get_req, resp_data=[])
        self._mock_request(mock_req=mock_post_req, resp_data=resp_data)
        self.assertEqual(self.service.create_archived_list(self.board_id, self.list_name), list_id)
        mock_get_req.assert_called_with('{}/boards/{}/lists'.format(self.url, self.board_id), params=self.params)
        self._update_test_params({'name': self.list_name, 'pos': 'bottom'})
        mock_post_req.assert_called_with('{}/boards/{}/lists'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.get')
    def test_exist_archived_list(self, mock_req):
        list_id = 'listId'
        resp_data = [{'name': self.list_name, 'id': list_id}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.create_archived_list(self.board_id, self.list_name), list_id)
        mock_req.assert_called_with('{}/boards/{}/lists'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.get')
    def test_failed_exist_archived_list(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.create_archived_list, self.board_id, self.list_name)
        mock_req.assert_called_with('{}/boards/{}/lists'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_failed_create_archived_list(self, mock_get_req, mock_post_req):
        self._mock_request(mock_req=mock_get_req, resp_data=[])
        self._mock_request_http_error(mock_post_req)
        self.assertRaises(HTTPError, self.service.create_archived_list, self.board_id, self.list_name)
        mock_get_req.assert_called_with('{}/boards/{}/lists'.format(self.url, self.board_id), params=self.params)
        self._update_test_params({'name': self.list_name, 'pos': 'bottom'})
        mock_post_req.assert_called_with('{}/boards/{}/lists'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_create_sprint_board(self, mock_get_req, mock_post_req):
        resp_data = {'name': self.board_name, 'id': self.board_id}
        self._mock_request(mock_req=mock_get_req, resp_data=[])
        self._mock_request(mock_req=mock_post_req, resp_data=resp_data)
        self.assertEqual(self.service.create_sprint_board(self.organ_name, self.board_name), self.board_id)
        mock_get_req.assert_called_with('{}/organization/{}/boards'.format(self.url, self.organ_name),
                                        params=self.params)
        self._update_test_params({'name': self.board_name, 'idOrganization': self.organ_name,
                                  'defaultLists': 'false', 'pos': 'top', 'prefs_permissionLevel': 'org'})
        mock_post_req.assert_called_with('{}/boards'.format(self.url), params=self.params)

    @mock.patch('requests.get')
    def test_exist_sprint_board(self, mock_req):
        resp_data = [{'name': self.board_name, 'id': self.board_id}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.assertEqual(self.service.create_sprint_board(self.organ_name, self.board_name), self.board_id)
        mock_req.assert_called_with('{}/organization/{}/boards'.format(self.url, self.organ_name), params=self.params)

    @mock.patch('requests.get')
    def test_failed_exist_sprint_board(self, mock_req):
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.create_sprint_board, self.organ_name, self.board_name)
        mock_req.assert_called_with('{}/organization/{}/boards'.format(self.url, self.organ_name), params=self.params)

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_failed_create_sprint_board(self, mock_get_req, mock_post_req):
        self._mock_request(mock_req=mock_get_req, resp_data=[])
        self._mock_request_http_error(mock_post_req)
        self.assertRaises(HTTPError, self.service.create_sprint_board, self.organ_name, self.board_name)
        mock_get_req.assert_called_with('{}/organization/{}/boards'.format(self.url, self.organ_name),
                                        params=self.params)
        self._update_test_params({'name': self.board_name, 'idOrganization': self.organ_name,
                                  'defaultLists': 'false', 'pos': 'top', 'prefs_permissionLevel': 'org'})
        mock_post_req.assert_called_with('{}/boards'.format(self.url), params=self.params)

    @mock.patch('requests.post')
    def test_move_done_cards(self, mock_req):
        from_list_id = 'toListId'
        to_list_id = 'toListId'
        resp_data = [{'idList': to_list_id}]
        self._mock_request(mock_req=mock_req, resp_data=resp_data)
        self.service.move_done_cards(self.board_id, from_list_id, to_list_id)
        self._update_test_params({'idBoard': self.board_id, 'idList': to_list_id})
        mock_req.assert_called_with('{}/lists/{}/moveAllCards'.format(self.url, from_list_id), params=self.params)

    @mock.patch('requests.post')
    def test_failed_move_done_cards(self, mock_req):
        from_list_id = 'toListId'
        to_list_id = 'toListId'
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.move_done_cards, self.board_id, from_list_id, to_list_id)
        self._update_test_params({'idBoard': self.board_id, 'idList': to_list_id})
        mock_req.assert_called_with('{}/lists/{}/moveAllCards'.format(self.url, from_list_id), params=self.params)

    @mock.patch('requests.put')
    def test_update_board_labels(self, mock_req):
        labels_data = [{'name': 'greenLabel', 'color': 'green'}, {'name': 'yellowLabel', 'color': 'yellow'}]
        self._mock_request(mock_req=mock_req, resp_data={})
        self.service.update_board_labels(self.board_id, labels_data)
        self._update_test_params({'labelNames/' + label['color']: label['name'] for label in labels_data})
        mock_req.assert_called_with('{}/boards/{}'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.put')
    def test_failed_wrong_labels_data(self, mock_req):
        labels_data = [{}, {}]
        self._mock_request(mock_req=mock_req, resp_data={})
        self.assertRaises(ValueError, self.service.update_board_labels, self.board_id, labels_data)

    @mock.patch('requests.put')
    def test_failed_update_board_labels(self, mock_req):
        labels_data = [{'name': 'greenLabel', 'color': 'green'}, {'name': 'yellowLabel', 'color': 'yellow'}]
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.update_board_labels, self.board_id, labels_data)
        self._update_test_params({'labelNames/' + label['color']: label['name'] for label in labels_data})
        mock_req.assert_called_with('{}/boards/{}'.format(self.url, self.board_id), params=self.params)

    @mock.patch('requests.put')
    def test_update_board_member(self, mock_req):
        member_id = 'memberId'
        member_type = 'memberType'
        self._mock_request(mock_req=mock_req, resp_data={})
        self.service.update_board_member(self.board_id, member_id, member_type)
        self._update_test_params({'type': member_type})
        mock_req.assert_called_with('{}/boards/{}/members/{}'.format(self.url, self.board_id, member_id),
                                    params=self.params)

    @mock.patch('requests.put')
    def test_failed_update_board_member(self, mock_req):
        member_id = 'memberId'
        member_type = 'memberType'
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.update_board_member, self.board_id, member_id, member_type)
        self._update_test_params({'type': member_type})
        mock_req.assert_called_with('{}/boards/{}/members/{}'.format(self.url, self.board_id, member_id),
                                    params=self.params)

    @mock.patch('requests.put')
    def test_move_list(self, mock_req):
        list_id = 'listId'
        self._mock_request(mock_req=mock_req, resp_data={})
        self.service.move_list(self.board_id, list_id)
        self._update_test_params({'value': self.board_id})
        mock_req.assert_called_with('{}/lists/{}/idBoard'.format(self.url, list_id), params=self.params)

    @mock.patch('requests.put')
    def test_failed_move_list(self, mock_req):
        list_id = 'listId'
        self._mock_request_http_error(mock_req)
        self.assertRaises(HTTPError, self.service.move_list, self.board_id, list_id)
        self._update_test_params({'value': self.board_id})
        mock_req.assert_called_with('{}/lists/{}/idBoard'.format(self.url, list_id), params=self.params)

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

    def _update_test_params(self, params_data):
        self.params.update(params_data)

if __name__ == '__main__':
    unittest.main()
