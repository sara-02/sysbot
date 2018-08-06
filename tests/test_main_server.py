"""Test main server module."""

import unittest
import json
from code.main_server import app, get_stems, lemmatize_sent
from setup_data import (slash_command_help_data, sentence, slash_command_open_issue_data,
                        slash_command_claim_data, slash_command_assign_issue_data,
                        slash_command_approve_issue_data, data_with_challenge_token,
                        data_member_joined_channel, data_app_mention_channel, data_message_reply,
                        event_data_issue_opened, event_data_comment, event_data_pr_opened)


class TestMainServer(unittest.TestCase):
    """Tests main server."""

    def setUp(self):
        """Set up test client."""
        self.client = app.test_client()

    def test_help_slash_command(self):
        """Tests help_slash_commands()."""
        with self.client:
            response = self.client.post('/help', data=json.dumps(slash_command_help_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_get_stems(self):
        """Tests get_stems()."""
        response = get_stems(sentence)
        self.assertEqual(response, 'Approve approv approv')

    def test_lemmatize_sent(self):
        """Tests lemmatize_sent()."""
        response = lemmatize_sent(sentence)
        self.assertEqual(response, 'Approve approved approving')

    def test_open_issue_slash_command(self):
        """Tests open_issue_slash_command()."""
        with self.client:
            response = self.client.post('/open_issue', data=json.dumps(slash_command_open_issue_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_slash_claim_command(self):
        """Tests slash_claim_command()."""
        with self.client:
            response = self.client.post('/claim', data=json.dumps(slash_command_claim_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_slash_assign_issue_command(self):
        """Tests slash_assign_issue_command()."""
        with self.client:
            response = self.client.post('/slack_assign_issue', data=json.dumps(slash_command_assign_issue_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_slash_approve_issue(self):
        """Tests slash_approve_issue()."""
        with self.client:
            response = self.client.post('/slack_approve_issue', data=json.dumps(slash_command_approve_issue_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_slash_invite_command(self):
        """Tests slash_invite_command()."""
        with self.client:
            response = self.client.post('/invite', data=json.dumps(slash_command_approve_issue_data),
                                        content_type='application/x-www-form-urlencoded')
            self.assertEqual(200, response.status_code)

    def test_challenge(self):
        """Tests challenge()."""
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
        """Tests home()."""
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.data, 'Response to test hosting.')

    def test_github_hook_receiver(self):
        """Tests github_hook_reciever()."""
        with self.client:
            response_issue_opened = self.client.post('/web_hook', data=json.dumps(event_data_issue_opened),
                                                     content_type='application/json')
            self.assertEqual(response_issue_opened.data, '{\n  "message": "New issue opened event"\n}\n')
            response_coveralls_comment = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                          content_type='application/json')
            self.assertEqual(response_coveralls_comment.data, '{\n  "message": "Coveralls comment"\n}\n')
            event_data_comment['comment']['body']= "@sys-bot approve"
            response_approve = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                content_type='application/json')
            self.assertEqual(response_approve.data, '{\n  "message": "Approve command"\n}\n')
            event_data_comment['comment']['body'] = "@sys-bot assign"
            response_assign_wrong_format = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                            content_type='application/json')
            self.assertEqual(response_assign_wrong_format.data, '{\n  "message": "Wrong command format"\n}\n')
            event_data_comment['comment']['body'] = "@sys-bot assign sammy1997"
            response_assign_not_approved = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                            content_type='application/json')
            self.assertEqual(response_assign_not_approved.data, '{\n  "message": "Issue not approved"\n}\n')
            event_data_comment['issue']['number'] = "150"
            response_assign_already_claimed = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                               content_type='application/json')
            self.assertEqual(response_assign_already_claimed.data, '{\n  "message": "Issue already claimed"\n}\n')
            event_data_comment['issue']['number'] = "149"
            response_assign_not_permitted = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                             content_type='application/json')
            self.assertEqual(response_assign_not_permitted.data, '{\n  "message": "Not permitted"\n}\n')
            event_data_comment['comment']['body'] = "@sys-bot claim something"
            response_claim_wrong_format = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                           content_type='application/json')
            self.assertEqual(response_claim_wrong_format.data, '{\n  "message": "Wrong command format"\n}\n')
            event_data_comment['issue']['number'] = "150"
            event_data_comment['comment']['body'] = "@sys-bot claim"
            response_claim_already_claimed = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                              content_type='application/json')
            self.assertEqual(response_claim_already_claimed.data, '{\n  "message": "Already claimed"\n}\n')
            event_data_comment['issue']['number'] = "151"
            response_claim_not_approved = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                           content_type='application/json')
            self.assertEqual(response_claim_not_approved.data, '{\n  "message": "Issue not approved"\n}\n')
            event_data_comment['comment']['body'] = "@sys-bot unclaim"
            response_unclaim = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                content_type='application/json')
            self.assertEqual(response_unclaim.data, '{\n  "message": "Issue unclaimed"\n}\n')
            event_data_comment['comment']['body'] = "@sys-bot unclaim something"
            response_unclaim_wrong_format = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                             content_type='application/json')
            self.assertEqual(response_unclaim_wrong_format.data, '{\n  "message": "Wrong command format"\n}\n')
            event_data_comment['comment']['body'] = "@sys-bot unassign sammy1997"
            response_unassign = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                 content_type='application/json')
            self.assertEqual(response_unassign.data, '{\n  "message": "Issue unassigned"\n}\n')
            event_data_comment['comment']['body'] = "@sys-bot unassign"
            response_unassign_wrong_format = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                              content_type='application/json')
            self.assertEqual(response_unassign_wrong_format.data, '{\n  "message": "Wrong command format"\n}\n')
            event_data_comment['comment']['body'] = "@sys-bot label test-label, approved, bug"
            event_data_comment['issue']['number'] = "140"
            response_label_correct_format = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                             content_type='application/json')
            self.assertEqual(response_label_correct_format.data, '{\n  "message": "All labels added to issue"\n}\n')
            event_data_comment['comment']['body'] = "@sys-bot label"
            response_label_wrong_format = self.client.post('/web_hook', data=json.dumps(event_data_comment),
                                                             content_type='application/json')
            self.assertEqual(response_label_wrong_format.data, '{\n  "message": "Wrong command format"\n}\n')
            response_pr_to_unapproved_issue = self.client.post('/web_hook', data=json.dumps(event_data_pr_opened),
                                                               content_type='application/json')
            self.assertEqual(response_pr_to_unapproved_issue.data, '{\n  "message": "PR sent to unapproved issue"\n}\n')
            event_data_pr_opened["pull_request"]["body"] = "Anything"
            response_pr_template_not_followed = self.client.post('/web_hook', data=json.dumps(event_data_pr_opened),
                                                                 content_type='application/json')
            self.assertEqual(response_pr_template_not_followed.data, '{\n  "message": "PR template not followed"\n}\n')
            event_data_pr_opened["action"] = "closed"
            response_unhandled = self.client.post('/web_hook', data=json.dumps(event_data_pr_opened),
                                                  content_type='application/json')
            self.assertEqual(response_unhandled.data, '{\n  "message": "Unknown event"\n}\n')


if __name__ == '__main__':
    unittest.main()
