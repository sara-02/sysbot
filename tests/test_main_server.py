import unittest
import json
from code.main_server import app, get_stems, lemmatize_sent
from setup_data import (slash_command_help_data, sentence, slash_command_open_issue_data,
                        slash_command_claim_data, slash_command_assign_issue_data,
                        slash_command_approve_issue_data, data_with_challenge_token,
                        data_member_joined_channel, data_app_mention_channel, data_message_reply)


class TestMainServer(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_help_slash_command(self):
        with self.client:
            response = self.client.post('/help', data=json.dumps(slash_command_help_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_get_stems(self):
        response = get_stems(sentence)
        self.assertEqual(response, 'Approve approv approv')

    def test_lemmatize_sent(self):
        response = lemmatize_sent(sentence)
        self.assertEqual(response, 'Approve approved approving')

    def test_open_issue_slash_command(self):
        with self.client:
            response = self.client.post('/open_issue', data=json.dumps(slash_command_open_issue_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_slash_claim_command(self):
        with self.client:
            response = self.client.post('/claim', data=json.dumps(slash_command_claim_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_slash_assign_issue_command(self):
        with self.client:
            response = self.client.post('/slack_assign_issue', data=json.dumps(slash_command_assign_issue_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_slash_approve_issue(self):
        with self.client:
            response = self.client.post('/slack_approve_issue', data=json.dumps(slash_command_approve_issue_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_slash_invite_command(self):
        with self.client:
            response = self.client.post('/invite', data=json.dumps(slash_command_approve_issue_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_challenge(self):
        with self.client:
            response_challenge_token = self.client.post('/challenge', data=json.dumps(data_with_challenge_token),
                                                        content_type='application/json')
            self.assertEqual(response_challenge_token.data, data_with_challenge_token.get('challenge'))
            response_to_member_joined = self.client.post('/challenge', data=json.dumps(data_member_joined_channel),
                                                         content_type='application/json')
            self.assertEqual(response_to_member_joined.data, '{\n  "message": "New member joined"\n}\n')
            response_app_mention = self.client.post('/challenge', data=json.dumps(data_app_mention_channel),
                                                    content_type='application/json')
            self.assertEqual(response_app_mention.data, '{\n  "message": "App mentioned"\n}\n')
            response_message_reply = self.client.post('/challenge', data=json.dumps(data_message_reply),
                                                      content_type='application/json')
            self.assertEqual(response_message_reply.data, '{\n  "message": "FAQ answered"\n}\n')

    def test_home(self):
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.data, 'Response to test hosting.')


if __name__ == '__main__':
    unittest.main()
