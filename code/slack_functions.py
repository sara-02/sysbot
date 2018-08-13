# -*- coding: utf-8 -*-

import requests
from flask import json
from nltk.tokenize import sent_tokenize, word_tokenize

from auth_credentials import (BOT_ACCESS_TOKEN, maintainer_usergroup_id, legacy_token, org_repo_owner, path_secret,
                              api_key)
from topic_extractor import NPExtractor
from request_urls import (dm_channel_open_url, dm_chat_post_message_url, get_maintainer_list,
                          get_user_profile_info_url, chat_post_ephimeral_message_url, luis_agent_intent_classify_call)
from messages import MESSAGE, ANSWERS_FAQS
from github_functions import (send_github_invite, issue_comment_approve_github, issue_assign,
                              check_assignee_validity, check_multiple_issue_claim,
                              open_issue_github, get_issue_author, check_approved_tag, fetch_issue_body,
                              label_list_issue)
from dictionaries import slack_team_vs_repo_dict, techstack_vs_projects, message_key_vs_list_of_alternatives, \
    CHANNEL_LIST

headers = {'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(BOT_ACCESS_TOKEN)}
headers_legacy_urlencoded = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer {}'.format(legacy_token)
}


def dm_new_users(data):
    # Get user id of the user who joined
    uid = data.get('event', {}).get('user', None)
    if uid is not None:
        body = {'user': uid}
        # Open a DM channel to the user. Request goes to im.open
        r = requests.post(dm_channel_open_url, data=json.dumps(body), headers=headers)
        response = r.json()
        if response.get('ok', False):
            # Get the channel just opened for DM
            dm_channel_id = response.get('channel', {}).get('id', '')
            if dm_channel_id != '':
                body = {
                    'username': 'Sysbot', 'as_user': True,
                    'text': MESSAGE.get('first_timer_message', 'Some error occured'),
                    'channel': dm_channel_id
                }
                # Send a DM request
                r = requests.post(dm_chat_post_message_url, data=json.dumps(body), headers=headers)
                return {'message': 'Success', 'status': 200}
    return {'message': 'Data format wrong', 'status': 400}


def is_maintainer_comment(commenter_id):
    # Using the id of usergroup maintainers
    body = {'usergroup': maintainer_usergroup_id, 'include_disabled': True}
    # Get list of maintainers. For more info :  usergroups.users.list in Slack API
    r = requests.post(get_maintainer_list, data=body, headers=headers_legacy_urlencoded)
    response = r.json()
    if response.get('ok', False):
        # Extract the maintainers
        maintainers = response.get('users', [])
        if commenter_id in maintainers:
            return {'status': 200, 'is_maintainer': True}
        else:
            return {'status': 200, 'is_maintainer': False}
    else:
        return {'status': 400, 'message': 'Wrong parameters'}


def approve_issue_label_slack(data):
    channel_id = data.get('channel_id', '')
    uid = data.get('user_id', '')
    result = is_maintainer_comment(uid)
    response = get_detailed_profile(uid)
    if response.get('ok', False):
        profile = response.get('profile', '')
        get_github_username = get_github_username_profile(profile)
        github_profile_present = get_github_username.get('github_profile_present', False)
        if not github_profile_present:
            send_message_ephemeral(channel_id, uid, MESSAGE.get('newcomer_requirement_incomplete', ''))
            return {"message": "Newcomer Requirement Incomplete"}
        else:
            github_id = get_github_username.get('github_id', '')
            if result.get('is_maintainer', False):
                params = data.get('text', '')
                if params != '' and len(params.split(' ')) == 2:
                    issue_author = get_issue_author(org_repo_owner, params.split(' ')[0], params.split(' ')[1])
                    if issue_author == github_id:
                        send_message_ephemeral(channel_id, uid, MESSAGE.get('author_cannot_approve', ''))
                        return {"message": "Author cannot approve an issue"}
                    response = issue_comment_approve_github(params.split(' ')[1], params.split(' ')[0],
                                                            org_repo_owner, github_id, True)
                    status = response.get('status', 500)
                    if status == 404:
                        # Information given is wrong
                        send_message_ephemeral(channel_id, uid, MESSAGE.get('wrong_info', ''))
                        return {"message": "Information provided is wrong", "status": 404}
                    elif status == 200:  # pragma: no cover
                        # Successful labeling
                        send_message_ephemeral(channel_id, uid, MESSAGE.get('success', ''))
                        return {"message": "Success", "status": 200}
                    elif status == 500:  # pragma: no cover
                        # Some internal error occured
                        send_message_ephemeral(channel_id, uid, MESSAGE.get('error_slash_command', ''))
                        return {"message": "Error with slash command", "status": 500}
                else:
                    # Wrong format of command was used
                    send_message_ephemeral(channel_id, uid, MESSAGE.get('correct_approve_format', ''))
                    return {"message": "Wrong parameters for for approval command"}
            else:
                # The commentor is not a maintainer
                send_message_ephemeral(channel_id, uid, MESSAGE.get('not_a_maintainer', ''))
                return {"message": "Non-maintainer cannot use the command"}
    else:
        send_message_ephemeral(channel_id, uid, MESSAGE.get('error_slash_command', ''))
        return {"message": "Error with slash command"}


def check_newcomer_requirements(uid, channel_id):
    response = get_detailed_profile(uid)
    if response.get('ok', False):
        profile = response.get('profile', '')
        get_github_username = get_github_username_profile(profile)
        github_profile_present = get_github_username.get('github_profile_present', False)
        if github_profile_present and profile.get('first_name', "") != "" and profile.get('last_name', "") != "" \
                and profile.get('title', "") != "" and profile.get('image_original', "") != "" \
                and not profile.get('phone', "").isdigit():
            github_id = get_github_username.get('github_id', '')
            send_github_invite(github_id)
            send_message_ephemeral(channel_id, uid, MESSAGE.get('invite_sent', ''))
            return {"message": "Invitation sent"}
        else:
            send_message_ephemeral(channel_id, uid, MESSAGE.get('newcomer_requirement_incomplete', ''))
            return {"message": "Newcomer requirements incomplete"}
    else:
        send_message_ephemeral(channel_id, uid, MESSAGE.get('error_slash_command', ''))
        return {"message": "Error with slash command"}


def assign_issue_slack(data):
    result = is_maintainer_comment(data.get('user_id', ''))
    channel_id = data.get('channel_id', '')
    uid = data.get('user_id', '')
    if result.get('is_maintainer', False):
        params = data.get('text', '')
        tokens = params.split(' ')
        if params != '' and len(tokens) == 3:
            # The tokens are issue number, repo name, and assignee username
            is_issue_claimed_or_assigned = check_multiple_issue_claim(org_repo_owner, tokens[0], tokens[1])
            # Check if issue is approved
            is_issue_approved = check_approved_tag(org_repo_owner, tokens[0], tokens[1])
            # If issue has been claimed, send message to the channel
            if is_issue_claimed_or_assigned:
                send_message_ephemeral(channel_id, uid, MESSAGE.get('already_claimed', ''))
                return {"message": "Issue already claimed"}
            # If issue has not been approved, send message to the channel
            if type(is_issue_approved) is dict:
                send_message_ephemeral(channel_id, uid, MESSAGE.get('wrong_info', ''))
                return {"message": "Wrong information provided", "status": 404}
            if not is_issue_approved:
                send_message_ephemeral(channel_id, uid, MESSAGE.get('not_approved', ''))
                return {"message": "Issue not approved"}
            # If issue is available, then check for assign status
            status = issue_assign(tokens[1], tokens[0], tokens[2], org_repo_owner)
            if status == 404:
                # Information given is wrong
                send_message_ephemeral(channel_id, uid, MESSAGE.get('wrong_info', ''))
                return {"message": "Wrong information provided", "status": 404}
            elif status == 200:  # pragma: no cover
                # Successful assignment
                send_message_ephemeral(channel_id, uid, MESSAGE.get('success', ''))
                return {"message": "Success", "status": 200}
            elif status == 500:  # pragma: no cover
                # Some internal error occured
                send_message_ephemeral(channel_id, uid, MESSAGE.get('error_slash_command', ''))
                return {"message": "Author cannot approve an issue", "status": 500}
        else:
            # Wrong format of command was used
            send_message_ephemeral(channel_id, uid, MESSAGE.get('correct_assign_format', ''))
            return {"message": "Wrong format of command"}
    else:
        # The commentor is not a maintainer
        send_message_ephemeral(channel_id, uid, MESSAGE.get('not_a_maintainer', ''))
        return {"message": "Not a maintainer"}


def claim_issue_slack(data):
    params = data.get('text', '')
    tokens = params.split(' ')
    channel_id = data.get('channel_id', '')
    uid = data.get('user_id', '')
    if params != '' and (len(tokens) == 3 or len(tokens) == 2):
        # The tokens are issue number, repo name, and claimant's username
        is_issue_claimed_or_assigned = check_multiple_issue_claim(org_repo_owner, tokens[0], tokens[1])
        # Check if issue is approved
        is_issue_approved = check_approved_tag(org_repo_owner, tokens[0], tokens[1])
        # If issue has been claimed, send message to the channel
        if is_issue_claimed_or_assigned:
            send_message_ephemeral(channel_id, uid, MESSAGE.get('already_claimed', ''))
            return {"message": "Issue already claimed"}
        # If issue has not been approved, send message to the channel
        if isinstance(is_issue_approved, dict):
            send_message_ephemeral(channel_id, uid, MESSAGE.get('wrong_info', ''))
            return {"message": "Wrong information provided", "status": 404}
        if not is_issue_approved:
            send_message_ephemeral(channel_id, uid, MESSAGE.get('not_approved', ''))
            return {"message": "Issue not approved"}
        # If the format /sysbot_claim <repo_name> <issue_number> is used
        if len(tokens) == 2:
            response = get_detailed_profile(uid)
            if response.get('ok', False):
                response = get_github_username_profile(response.get('profile', {}))
                if response.get('github_profile_present', False):
                    # Find if the username is present in Slack profile
                    github_username = response.get('github_id', '')
                else:
                    send_message_ephemeral(channel_id, uid, MESSAGE.get('error_claim_alternate', ''))
                    return {"message": "Incomplete profile for using command"}
            else:
                send_message_ephemeral(channel_id, uid, MESSAGE.get('error_slash_command', ''))
                return {"message": "Error in command parameters"}
        else:
            github_username = tokens[2]

        # If issue is available, then check for assign status
        status = issue_assign(tokens[1], tokens[0], github_username, org_repo_owner)
        # If a 404 error status is raised, check if the assignee can be assigned.
        if status == 404:
            # Check assignee status
            assignee_status = check_assignee_validity(tokens[0], github_username, org_repo_owner)
            if assignee_status == 404:
                # Can't be assigned as not a member
                send_message_ephemeral(channel_id, uid, MESSAGE.get('not_a_member', ''))
                return {"message": "Not a member", "status": 404}
            else:
                # Information given is wrong
                send_message_ephemeral(channel_id, uid, MESSAGE.get('wrong_info', ''))
                return {"message": "Wrong information provided"}
        elif status == 200:  # pragma: no cover
            # Successful claim
            send_message_ephemeral(channel_id, uid, MESSAGE.get('success', ''))
            return {"message": "Success", "status": 404}
        elif status == 500:  # pragma: no cover
            # Some internal error occured
            send_message_ephemeral(channel_id, uid, MESSAGE.get('error_slash_command', ''))
            return {"message": "Error slash command", "status": 500}
    else:
        # Wrong format of command was used
        send_message_ephemeral(channel_id, uid, MESSAGE.get('correct_claim_format', ''))
        return {"message": "Correct claim format"}


def send_message_to_channels(channel_id, message):  # pragma: no cover
    body = {'username': 'Sysbot', 'as_user': True, 'text': message, 'channel': channel_id}
    response = requests.post(dm_chat_post_message_url, data=json.dumps(body), headers=headers)
    if response.json().get('ok', False):
        return {'message': 'Success', 'status': 200}
    else:
        return {'message': 'Wrong information', 'status': 404}


def send_message_thread(channel_id, message, thread_timestamp):  # pragma: no cover
    body = {'username': 'Sysbot', 'as_user': True, 'text': message, 'channel': channel_id, 'thread_ts': thread_timestamp}
    response = requests.post(dm_chat_post_message_url, data=json.dumps(body), headers=headers)
    return response.status_code


def send_message_ephemeral(channel_id, uid, message):
    body = {'username': 'Sysbot', 'as_user': True, 'text': message, 'channel': channel_id, 'user': uid}
    response = requests.post(chat_post_ephimeral_message_url, data=json.dumps(body), headers=headers)
    return response.status_code


def open_issue_slack(data):  # pragma: no cover
    channel_id = data.get('channel_id', '')
    uid = data.get('user_id', '')
    # Get the command parameters used by the user
    command_params = data.get('text', '')
    # For getting author name and repo name
    tokens = command_params.split(' ')
    # For extracting title, description, update list item, and estimation
    title_body_tokens = command_params.split('*')
    if command_params == "" or len(tokens) < 6 or len(title_body_tokens) < 5 or \
            title_body_tokens[1] == '' or title_body_tokens[2] == '' or \
            title_body_tokens[3] == '' or title_body_tokens[4] == '':
        send_message_ephemeral(channel_id, uid, MESSAGE.get('wrong_params_issue_command', ''))
        return {"message": "Wrong parameters for command"}
    # Each part is extracted and will be put into the template
    issue_title = title_body_tokens[1]
    issue_description = title_body_tokens[2]
    update_list_item = title_body_tokens[3]
    estimation = title_body_tokens[4]
    status = open_issue_github(org_repo_owner, tokens[0], issue_title, issue_description,
                               update_list_item, estimation, tokens[1])
    if status == 201:
        # If issue has been opened successfully
        send_message_ephemeral(channel_id, uid, MESSAGE.get('success_issue', ''))
        return {"message": "Successfully opened issue", "status": 201}
    else:
        send_message_ephemeral(channel_id, uid, MESSAGE.get('error_issue', ''))
        return {"message": "Error in opening issue", "status": status}


def get_detailed_profile(uid):
    body = {'user': uid, 'include_labels': True}
    profile_response_json = requests.post(get_user_profile_info_url, data=body, headers=headers_legacy_urlencoded).json()
    if profile_response_json.get('ok', False):
        profile = profile_response_json.get('profile', {})
        return {'profile': profile, 'ok': True}
    return {'ok': False}


def get_github_username_profile(profile):
        custom_fields = profile.get('fields', {})
        if custom_fields is not None:
            for key in custom_fields:
                github_link = custom_fields.get(key, {}).get('value', '')
                if 'github.com/' in github_link:
                    github_id = github_link.split('github.com/')[1]
                    return {'github_profile_present': True, 'github_id': github_id}
        return {'github_profile_present': False}


def slack_team_name_reply(data):
    message = data.get('event', {}).get('text', '')
    channel_id = data.get('event', {}).get('channel', '')
    uid = data.get('event', {}).get('user', '')
    # Check if query format is ok
    if message != '' and len(message.split('<@UASFP3GHW>')) >= 2:
        # Extracting the query text from message. Here <@UASFP3GHW> is the bot mention.
        query = message.split('<@UASFP3GHW>')[1].strip()
        team_details = slack_team_vs_repo_dict.get(channel_id, '')
        # Check if query is empty or if channel doesn't have a team.
        if query != '' and team_details != '':
            # This is a constant command which will always work
            if query == 'maintainer team name':  # pragma: no cover
                send_message_ephemeral(channel_id, uid, MESSAGE.get('slack_team_message') % (
                    team_details[0], team_details[1]))
                return {'message': 'Team name requested'}
            else:
                query = query.replace(' ', '%20')
                request_url = luis_agent_intent_classify_call % (path_secret, api_key, query)
                response = requests.get(request_url).json()
                # Checking by matching intent. Keeping score high to prevent false positives.
                condition1 = response.get('topScoringIntent', {}).get('intent', '') == 'Maintainers'
                condition2 = float(response.get('topScoringIntent', {}).get('score', '0')) > 0.965
                if condition1 and condition2:  # pragma: no cover
                    send_message_ephemeral(channel_id, uid, MESSAGE.get('slack_team_message') % (
                        team_details[0], team_details[1]))
                    return {'message': 'Team name requested'}
                else:
                    # If query isn't recognized, return default answer
                    send_message_ephemeral(channel_id, uid, MESSAGE.get('no_answer'))
                    return {'message': 'Not classified query'}
        elif team_details == '':
            send_message_ephemeral(channel_id, uid, MESSAGE.get('slack_team_DNE'))
            return {'message': 'Team does not exist in records.'}
    send_message_ephemeral(channel_id, uid, MESSAGE.get('wrong_query_format'))
    return {'message': 'Illegitimate query.'}


def handle_message_answering(event_data):
    # Time stamp  of thread if present
    thread_ts = event_data.get('thread_ts', None)
    # Message time stamp
    reply_ts = event_data.get('ts', None)
    # If message is in a thread, then the UID of commenter of main message
    parent_uid = event_data.get('parent_user_id', None)
    # Current comment's author
    comment_user_uid = event_data.get('user', None)
    text = str(event_data.get('text', None))
    channel = event_data.get('channel', None)
    # Checking if it's a reply to a thread by any other user
    if thread_ts is not None and parent_uid != comment_user_uid:
        return {'message': 'Not handling replies made by others'}
    # If the message is in a thread and made by the parent commenter
    elif thread_ts is not None and parent_uid == comment_user_uid:
        reply_ts = thread_ts
    if channel == CHANNEL_LIST.get('intro'):  # pragma: no cover
        techs = techstack_vs_projects.keys()
        suggest_projects_set = set()
        search_text_tokens = word_tokenize(text.upper())
        # Finding all languages mentioned in comment common with the ones in Systers language list
        techs = list(set(search_text_tokens).intersection(set(techs)))
        for tech in techs:
            suggest_projects_set = suggest_projects_set.union(set(techstack_vs_projects[tech]))
        suggest_projects_list = list(suggest_projects_set)
        # No tech stack found in intro comment.
        if not suggest_projects_list and thread_ts is None:
            message = MESSAGE.get('answer_to_intro') % (MESSAGE.get('no_project'))
            send_message_thread(channel, message, reply_ts)
        elif suggest_projects_list:
            projects = ""
            for i, project in enumerate(suggest_projects_list):
                projects = projects + "\n" + str(i + 1) + ". www.github.com/systers/" + project + ", "
            # Message is not in a thread. Reply with full message.
            if thread_ts is None:
                message = MESSAGE.get('answer_to_intro') % (MESSAGE.get('projects_message') % projects[0:-2])
                send_message_thread(channel, message, reply_ts)
            # Message in thread. Reply with projects.
            elif thread_ts is not None:
                message = MESSAGE.get('projects_message') % projects[0:-2]
                send_message_thread(channel, message, reply_ts)
    # Answering some FAQs
    answer_keyword_faqs(text, channel, reply_ts)
    # Answering classification questions only on questions and intro and not in threads
    if thread_ts is None and (channel == CHANNEL_LIST.get('questions') or channel == CHANNEL_LIST.get('intro')):
        luis_classifier(text, channel, reply_ts)
        return {'message': 'Sent for intent classification'}
    return {'message': 'Not sent for classification'}


def answer_keyword_faqs(comment_text, channel, reply_ts):
    sentences = sent_tokenize(comment_text)
    for sentence in sentences:
        is_question = check_is_question(sentence)
        if not is_question:
            continue
        main_subjects = NPExtractor(sentence).extract()
        for topic in main_subjects:
            for key in message_key_vs_list_of_alternatives.keys():
                if topic.lower() in message_key_vs_list_of_alternatives[key]:
                    send_message_thread(channel, ANSWERS_FAQS.get(key, ""), reply_ts)
                    break
    return {"message": "Keyword FAQs answered"}


def check_is_question(sentence):
    start_words = ["who", "what", "when", "where", "why", "how", "is", "can", "does", "do"]
    if sentence.endswith("?"):
        return True
    for word in start_words:
        if sentence.startswith(word):
            return True
    return False


def luis_classifier(query, channel, reply_ts):
    query = query.replace(' ', '%20')
    request_url = luis_agent_intent_classify_call % (path_secret, api_key, query)
    response = requests.get(request_url).json()
    top_intent = response.get('topScoringIntent', {}).get('intent', '')
    top_intent_score = float(response.get('topScoringIntent', {}).get('score', '0'))
    if top_intent == 'participation-gender' and top_intent_score > 0.6:
        send_message_thread(channel, ANSWERS_FAQS.get('contributor_gender'), reply_ts)
        return {'message': 'Participant gender question'}
    elif top_intent == 'getting-started' and top_intent_score > 0.6:
        send_message_thread(channel, ANSWERS_FAQS.get('getting_started'), reply_ts)
        return {'message': 'Getting started question'}


def view_issue_slack(event_data):
    command_text = event_data.get('text', '')
    channel_id = event_data.get('channel_id', '')
    uid = event_data.get('user_id', '')
    tokens = command_text.strip().split(' ')
    if len(tokens) == 2:
        response = fetch_issue_body(org_repo_owner, tokens[0], tokens[1])
        if response.get('status', 404) == 200:
            send_message_ephemeral(channel_id, uid, response.get('issue_body', ''))
            return {'message': 'Success in viewing.'}
        else:
            send_message_ephemeral(channel_id, uid, MESSAGE.get('incorrect_info_provided', ''))
            return {'message': "Wrong info provided"}
    else:
        send_message_ephemeral(channel_id, uid, MESSAGE.get('error_view_command', ''))
        return {'message': "Error in using command"}


def label_issue_slack(event_data):
    label_text = event_data.get('text', '')
    channel_id = event_data.get('channel_id', '')
    uid = event_data.get('user_id', '')
    response = is_maintainer_comment(uid)
    tokens = label_text.split(' ')
    label_list_tokens = label_text.split('[')
    if response.get('is_maintainer', False):
        if len(tokens) < 3 and len(label_list_tokens) != 2 and "]" not in label_text:
            send_message_ephemeral(channel_id, uid, MESSAGE.get('error_view_command', ''))
            return {'message': 'Wrong format'}
        else:
            label_list_tokens = '@sys-bot label %s' % label_list_tokens[1].split(']')[0]
            response = label_list_issue(org_repo_owner, tokens[0], tokens[1], label_list_tokens)
            if response.get('status', 400) == 400:
                send_message_ephemeral(channel_id, uid, MESSAGE.get('incorrect_info_provided', ''))
                return {'message': 'Wrong info'}
            else:
                send_message_ephemeral(channel_id, uid, MESSAGE.get('success', ''))
                return {'message': 'Labelled issue'}
    else:
        send_message_ephemeral(channel_id, uid, MESSAGE.get('not_a_maintainer', ''))
        return {'message': "Not a maintainer"}
