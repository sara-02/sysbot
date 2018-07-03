import unittest
from code.slack_functions import (get_github_username_profile, get_detailed_profile,
                                  send_message_to_channels, is_maintainer_comment,
                                  check_newcomer_requirements, open_issue_slack)
from setup_data import (profile_with_github, profile_without_github, slash_command_data,
                        slash_command_data_wrong_info, slash_command_data_command_params_missing)


class TestSlackFunctions(unittest.TestCase):
    def test_get_github_username_profile(self):
        profile_url_present = get_github_username_profile(profile_with_github.get('profile'))
        profile_url_missing = get_github_username_profile(profile_without_github.get('profile'))
        self.assertEqual(profile_url_present, {'github_profile_present': True, 'github_id': 'sammy1997'})
        self.assertEqual(profile_url_missing, {'github_profile_present': False})

    def test_get_detailed_profile(self):
        # Wrong UID
        false_profile = get_detailed_profile('U7KMRCMNR')
        # Correct UID
        correct_profile = get_detailed_profile('U7KMRCS5Q')
        self.assertEqual(false_profile, {'ok': False})
        self.assertEqual(correct_profile, {'profile': profile_with_github.get('profile'), 'ok': True})

    def test_is_maintainer_comment(self):
        maintainer_comment = is_maintainer_comment('U7KMRCS5Q')
        non_maintainer_comment = is_maintainer_comment('U7KMRCMNR')
        self.assertEqual(maintainer_comment, {'status': 200, 'is_maintainer': True})
        self.assertEqual(non_maintainer_comment, {'status': 200, 'is_maintainer': False})

    def test_send_message_to_channels(self):
        successful_message = send_message_to_channels('CAP9GA5MJ', 'Message generated while testing')
        failed_message = send_message_to_channels('CAP9GAMNR', 'Failed message')
        self.assertEqual(successful_message, {'message': 'Success', 'status': 200})
        self.assertEqual(failed_message, {'message': 'Wrong information', 'status': 404})

    def test_check_newcomer_requirements(self):
        profile_complete = check_newcomer_requirements('U7KMRCS5Q', 'CAP9GA5MJ')
        profile_incomplete = check_newcomer_requirements('U9BAL65KK', 'CAP9GA5MJ')
        error_response = check_newcomer_requirements('U7KMRCMNR', 'CAP9GA5MJ')
        self.assertEqual(profile_complete, {"message": "Invitation sent"})
        self.assertEqual(profile_incomplete, {"message": "Newcomer requirements incomplete"})
        self.assertEqual(error_response, {"message": "Error with slash command"})

    def test_open_issue_slack(self):
        open_issue_success = open_issue_slack(slash_command_data)
        open_issue_failure = open_issue_slack(slash_command_data_wrong_info)
        wrong_command_format = open_issue_slack(slash_command_data_command_params_missing)
        self.assertEqual(open_issue_success, {"message": "Successfully opened issue", "status": 201})
        self.assertEqual(open_issue_failure, {"message": "Error in opening issue", "status": 404})
        self.assertEqual(wrong_command_format, {"message": "Wrong parameters for command"})
