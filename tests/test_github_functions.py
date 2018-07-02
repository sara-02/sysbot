import unittest
from code.github_functions import (check_approved_tag, label_opened_issue, send_github_invite,
                                   issue_comment_approve_github, github_pull_request_label)
from setup_data import (correct_issue_data, wrong_issue_data, missing_params_issue_data)


class TestGithubFunctions(unittest.TestCase):
    def test_label_opened_issue(self):
        correct_issue = label_opened_issue(correct_issue_data)
        wrong_issue = label_opened_issue(wrong_issue_data)
        missing_params_issue = label_opened_issue(missing_params_issue_data)
        self.assertEqual(correct_issue, {'message': 'Success', 'status': 200})
        self.assertEqual(missing_params_issue,
                         {'message': 'Format of data provided is wrong or misformed', 'status': 400})
        self.assertEqual(wrong_issue, {'message': 'Error', 'status': 404})

    def test_send_github_invite(self):
        successful_invitation = send_github_invite('sammy1997')
        unsuccessful_invitation = send_github_invite('sammy19997')
        self.assertEqual(successful_invitation, {'message': 'Success', 'status': 200})
        self.assertEqual(unsuccessful_invitation, {'message': 'Error', 'status': 404})

    def test_issue_comment_approve(self):
        author_tries_approving = issue_comment_approve_github('104', 'sysbot-test', 'systers', 'sys-bot', False)
        self.assertEqual(author_tries_approving, {'message': 'Author cannot approve.', 'status': 400})
        wrong_data = issue_comment_approve_github('104', 'sysbot-testing', 'systers', 'sys-bot', True)
        self.assertEqual(wrong_data, {'message': 'Error', 'status': 404})
        successful_approval = issue_comment_approve_github('87', 'sysbot-test', 'systers', 'sys-bot', True)
        self.assertEqual(successful_approval, {'message': 'Success', 'status': 200})

    def test_check_approved_tag(self):
        true_response = check_approved_tag('systers', 'sysbot-test', 75)
        self.assertEqual(true_response, True)
        false_response = check_approved_tag('systers', 'sysbot-test', 77)
        self.assertEqual(false_response, False)

    def test_github_pull_request_label(self):
        successful_label = github_pull_request_label('78', 'sysbot-test', 'systers')
        failed_label = github_pull_request_label('78', 'sysbot-testing', 'systers')
        self.assertEqual(successful_label, 200)
        self.assertEqual(failed_label, 404)
