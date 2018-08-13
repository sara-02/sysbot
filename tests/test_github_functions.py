import unittest
from code.github_functions import (check_approved_tag, label_opened_issue, send_github_invite,
                                   issue_comment_approve_github, github_pull_request_label,
                                   issue_assign, check_assignee_validity, github_comment,
                                   issue_claim_github, check_multiple_issue_claim,
                                   get_issue_author, unassign_issue, check_issue_template,
                                   close_pr, are_issue_essential_components_present,
                                   list_open_prs_from_repo, open_issue_github, check_pr_template,
                                   label_list_issue, fetch_issue_body, pr_reviewed_label)
from code.messages import MESSAGE
from setup_data import (correct_issue_data, wrong_issue_data, missing_params_issue_data,
                        pr_template_with_fixes_number, pr_template_with_fixes_text,
                        pr_template_without_fixes, pr_changes_requested_review_event_data,
                        pr_approved_review_event_data, pr_review_error_event_data)


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
        # successful_invitation = send_github_invite('prachi1210')
        unsuccessful_invitation = send_github_invite('sammy19997')
        # self.assertEqual(successful_invitation, {'message': 'Success', 'status': 200})
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

    def test_issue_assign(self):
        successful_assign_status = issue_assign('87', 'sysbot-test', 'sys-bot', 'systers')
        failed_assign_status = issue_assign('105', 'sysbot-testing', 'sammy1997', 'systers')
        self.assertEqual(successful_assign_status, 200)
        self.assertEqual(failed_assign_status, 404)

    def test_check_assignee_validity(self):
        valid_assignee_status = check_assignee_validity('sysbot', 'sys-bot', 'systers')
        invalid_assignee_status = check_assignee_validity('sysbot', 'sammy19997', 'systers')
        self.assertEqual(valid_assignee_status, 204)
        self.assertEqual(invalid_assignee_status, 404)

    def test_github_comment(self):
        successful_comment = github_comment('Testing', 'systers', 'sysbot-test', '71')
        unsuccessful_comment_status = github_comment('Testing', 'syster', 'sysbot-testing', '71')
        self.assertEqual(successful_comment, 201)
        self.assertEqual(unsuccessful_comment_status, 404)

    def test_issue_claim_github(self):
        successful_claim = issue_claim_github('sys-bot', '71', 'sysbot-test', 'systers')
        unsuccessful_claim = issue_claim_github('sammy19997', '71', 'sysbot-test', 'systers')
        self.assertEqual(successful_claim, {"message": "Issue claimed", "status": 204})
        self.assertEqual(unsuccessful_claim, {"message": "Not a member of the organization", "status": 404})

    def test_check_multiple_issue_claim(self):
        true_response = check_multiple_issue_claim('systers', 'sysbot-test', '75')
        false_response = check_multiple_issue_claim('systers', 'sysbot-test', '85')
        self.assertEqual(true_response, True)
        self.assertEqual(false_response, False)

    def test_open_issue_github(self):
        successful_issue_open = open_issue_github('systers', 'sysbot-test', 'Test Issue', 'Test body',
                                                  'Test list item', '1 hour', 'sys-bot')
        failed_issue_open = open_issue_github('syster', 'sysbot-testing', 'Test Issue', 'Test body',
                                              'Test list item', '1 hour', 'sys-bot')
        self.assertEqual(successful_issue_open, 201)
        self.assertEqual(failed_issue_open, 404)

    def test_get_issue_author(self):
        existent_author = get_issue_author('systers', 'sysbot-test', '74')
        non_existent_author = get_issue_author('syster', 'sysbot-testing', '74')
        self.assertEqual(existent_author, 'sys-bot')
        self.assertEqual(non_existent_author, '')

    def test_unassign_issue(self):
        unassign_success_status = unassign_issue('systers', 'sysbot-test', '87', 'sammy1997')
        unassign_failure_status = unassign_issue('syster', 'sysbot-testing', '87', 'sammy1997')
        self.assertEqual(unassign_success_status, 200)
        self.assertEqual(unassign_failure_status, 404)

    def test_close_pr(self):
        successful_close_pr_status = close_pr('systers', 'sysbot-test', '84')
        failure_close_pr_status = close_pr('syster', 'sysbot-testing', '84')
        self.assertEqual(successful_close_pr_status, 200)
        self.assertEqual(failure_close_pr_status, 404)

    def test_check_issue_template(self):
        template_matching_issue = check_issue_template('systers', 'sysbot-test', '87',
                                                       MESSAGE.get("issue_template") % ('author', 'body',
                                                                                        'list item', '1'))
        template_mis_matching_issue = check_issue_template('systers', 'sysbot-test', '66', 'Testing')
        self.assertEqual(template_mis_matching_issue, {"message": "Issue Template mismatch", "label_status": 200})
        self.assertEqual(template_matching_issue, {"message": "Issue Template match"})

    def test_are_issue_essential_components_present(self):
        correct_template_user_story = are_issue_essential_components_present(MESSAGE.get("issue_template") %
                                                                             ('author', 'body', 'list item', '1'))
        self.assertEqual(correct_template_user_story, True)
        correct_template_feature = are_issue_essential_components_present(MESSAGE.get("issue_template_feature") %
                                                                          ("Yes.", "Solution", "Alternatives"))
        self.assertEqual(correct_template_feature, True)
        correct_template_bug = are_issue_essential_components_present(MESSAGE.get("issue_template_bug") %
                                                                      ("Description", "Reproduce", "Expected", "Linux"))
        self.assertEqual(correct_template_bug, True)
        wrong_template = are_issue_essential_components_present("Test test")
        self.assertEqual(wrong_template, False)

    def test_check_pr_template(self):
        response_correct_template = check_pr_template(pr_template_with_fixes_number %
                                                      ("Description", "Type of Change", "Tested", "Checklist Point"),
                                                      'systers', 'sysbot-testing', '12')
        self.assertEqual(response_correct_template, True)
        response_no_fixes_statement = check_pr_template(pr_template_without_fixes %
                                                        ("Description", "Type of Change", "Tested", "Checklist Point"),
                                                        'systers', 'sysbot-testing', '12')
        self.assertEqual(response_no_fixes_statement, False)
        response_text_fixes_statement = check_pr_template(pr_template_with_fixes_text %
                                                          ("Description", "Type of Change", "Tested", "Checklist Point"),
                                                          'systers', 'sysbot-testing', '12')
        self.assertEqual(response_text_fixes_statement, False)
        response_wrong_template = check_pr_template("Test test",
                                                    'systers', 'sysbot-testing', '12')
        self.assertEqual(response_wrong_template, False)

    def test_label_list_issue(self):
        response_all_labelled = label_list_issue('systers', 'sysbot-test', 140, "@sys-bot label test-label, bug")
        self.assertEqual(response_all_labelled, {"message": "All labels added to issue", "status": 200})
        response_error = label_list_issue('systers', 'sysbot-testing', 140, "@sys-bot label test-label, bug")
        self.assertEqual(response_error, {"message": "Some error occurred", "status": 400})

    def test_fetch_issue_body(self):
        response_successful_fetch = fetch_issue_body('systers', 'sysbot-test', 178)
        self.assertEqual(response_successful_fetch, {'issue_body': 'Abcd', 'status': 200})
        response_failed_fetch = fetch_issue_body('systers', 'sysbot-testing', 178)
        self.assertEqual(response_failed_fetch, {'message': 'Wrong information provided', 'status': 404})

    def test_pr_reviewed_label(self):
        response_pr_changes_requested = pr_reviewed_label(pr_changes_requested_review_event_data)
        self.assertEqual(response_pr_changes_requested, {"message": "Labelled as under review", "status": 200})
        response_pr_approved = pr_reviewed_label(pr_approved_review_event_data)
        self.assertEqual(response_pr_approved, {"message": "Labelled as approved", "status": 200})
        response_pr_error = pr_reviewed_label(pr_review_error_event_data)
        self.assertEqual(response_pr_error, {"message": "Some error occurred", "status": 400})
