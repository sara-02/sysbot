import unittest
from code.slack_functions import (get_github_username_profile, get_detailed_profile,
                                  is_maintainer_comment, check_newcomer_requirements,
                                  luis_classifier, dm_new_users, slack_team_name_reply,
                                  answer_keyword_faqs, approve_issue_label_slack,
                                  assign_issue_slack, claim_issue_slack, view_issue_slack, label_issue_slack)
from setup_data import (profile_with_github, profile_without_github, query_getting_started,
                        query_gender_participation, new_user_data, faq_sentence,
                        slash_command_approve_issue_data, slash_command_assign_issue_data,
                        slash_command_claim_data, slash_command_view_issue_data, slash_command_label_issue_data)


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

    def test_check_newcomer_requirements(self):
        profile_complete = check_newcomer_requirements('U7KMRCS5Q', 'CAP9GA5MJ')
        profile_incomplete = check_newcomer_requirements('UASFP3GHW', 'CAP9GA5MJ')
        error_response = check_newcomer_requirements('U7KMRCMNR', 'CAP9GA5MJ')
        self.assertEqual(profile_complete, {"message": "Invitation sent"})
        self.assertEqual(profile_incomplete, {"message": "Newcomer requirements incomplete"})
        self.assertEqual(error_response, {"message": "Error with slash command"})

    def test_luis_classifier(self):
        response_getting_started = luis_classifier(query_getting_started, 'CAP9GA5MM', 1532589895.000165)
        self.assertEqual(response_getting_started, {'message': 'Getting started question'})
        response_participant_gender = luis_classifier(query_gender_participation, 'CAP9GA5MM', 1532589895.000165)
        self.assertEqual(response_participant_gender, {'message': 'Participant gender question'})

    def test_dm_new_users(self):
        response_successful_dm = dm_new_users(new_user_data)
        self.assertEqual(response_successful_dm, {'message': 'Success', 'status': 200})

    def test_slack_team_name_reply(self):
        response_wrong_channel = slack_team_name_reply(new_user_data)
        self.assertEqual(response_wrong_channel, {'message': 'Team does not exist in records.'})
        new_user_data["event"]["channel"]="CAEDCBACW"
        response_not_classified = slack_team_name_reply(new_user_data)
        self.assertEqual(response_not_classified, {'message': 'Not classified query'})
        new_user_data["event"]["channel"] = "CAP9GA5MJ"
        new_user_data["event"]["text"] = ""
        response_illegal_query = slack_team_name_reply(new_user_data)
        self.assertEqual(response_illegal_query, {'message': 'Illegitimate query.'})

    def test_answer_keyword_faqs(self):
        response = answer_keyword_faqs(faq_sentence, 'CAP8GX5NH', '15000032.23411')
        self.assertEqual(response, {"message": "Keyword FAQs answered"})

    def test_approve_issue_label_slack(self):
        slash_command_approve_issue_data["channel_id"] = "CAP8GH5MX"
        slash_command_approve_issue_data["text"] = "sysbot-test 36"
        response_author = approve_issue_label_slack(slash_command_approve_issue_data)
        self.assertEqual(response_author, {"message": "Author cannot approve an issue"})
        slash_command_approve_issue_data["text"] = "sysbot-testing 36"
        response_wrong_info = approve_issue_label_slack(slash_command_approve_issue_data)
        self.assertEqual(response_wrong_info, {"message": "Information provided is wrong", "status": 404})
        slash_command_approve_issue_data["text"] = "sysbot-test"
        response_wrong_params = approve_issue_label_slack(slash_command_approve_issue_data)
        self.assertEqual(response_wrong_params, {"message": "Wrong parameters for for approval command"})

    def test_assign_issue_slack(self):
        slash_command_assign_issue_data["text"]="sysbot-test 150 sammy1997"
        response_assign_claimed = assign_issue_slack(slash_command_assign_issue_data)
        self.assertEqual(response_assign_claimed, {"message": "Issue already claimed"})
        slash_command_assign_issue_data["text"] = "sysbot-test 152 sammy1997"
        response_assign_not_approved = assign_issue_slack(slash_command_assign_issue_data)
        self.assertEqual(response_assign_not_approved, {"message": "Issue not approved"})
        slash_command_assign_issue_data["text"] = "sysbot-testing 152 sammy1997"
        response_assign_wrong_info = assign_issue_slack(slash_command_assign_issue_data)
        self.assertEqual(response_assign_wrong_info, {"message": "Wrong information provided", "status": 404})
        slash_command_assign_issue_data["text"] = "sysbot-testing 152"
        response_assign_wrong_format = assign_issue_slack(slash_command_assign_issue_data)
        self.assertEqual(response_assign_wrong_format, {"message": "Wrong format of command"})

    def test_claim_issue_slack(self):
        slash_command_claim_data["text"] = "sysbot-test 150 sys-bot"
        response_already_claimed = claim_issue_slack(slash_command_claim_data)
        self.assertEqual(response_already_claimed, {"message": "Issue already claimed"})
        slash_command_claim_data["text"] = "sysbot-test 152 sammy1997"
        response_not_approved = claim_issue_slack(slash_command_claim_data)
        self.assertEqual(response_not_approved, {"message": "Issue not approved"})

    def test_view_issue_slack(self):
        response_success = view_issue_slack(slash_command_view_issue_data)
        self.assertEqual(response_success, {'message': 'Success in viewing.'})
        slash_command_view_issue_data['text'] = "sysbot-testing 178"
        response_wrong_info = view_issue_slack(slash_command_view_issue_data)
        self.assertEqual(response_wrong_info, {'message': "Wrong info provided"})
        slash_command_view_issue_data['text'] = "sysbot-testing 178 sammy1997"
        response_wrong_params = view_issue_slack(slash_command_view_issue_data)
        self.assertEqual(response_wrong_params, {'message': "Error in using command"})

    def test_label_issue_slack(self):
        label_success = label_issue_slack(slash_command_label_issue_data)
        self.assertEqual(label_success, {'message': 'Labelled issue'})
        slash_command_label_issue_data['text'] = "sysbot-testing 181 [bug, enhancement]"
        label_wrong_info = label_issue_slack(slash_command_label_issue_data)
        self.assertEqual(label_wrong_info, {'message': 'Wrong info'})
        slash_command_label_issue_data['text'] = "sysbot-testing 181"
        label_wrong_params = label_issue_slack(slash_command_label_issue_data)
        self.assertEqual(label_wrong_params, {'message': 'Wrong format'})
