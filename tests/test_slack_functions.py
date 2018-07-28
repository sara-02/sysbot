import unittest
from code.slack_functions import (get_github_username_profile, get_detailed_profile,
                                  is_maintainer_comment, check_newcomer_requirements,
                                  luis_classifier)
from setup_data import (profile_with_github, profile_without_github, query_getting_started,
                        query_gender_participation)


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
