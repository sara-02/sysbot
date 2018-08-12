from flask import Flask, jsonify
from flask import request, json, Response
from github_functions import (label_opened_issue, issue_comment_approve_github,
                              github_pull_request_label, issue_assign, github_comment, issue_claim_github,
                              check_multiple_issue_claim, check_approved_tag, unassign_issue, close_pr,
                              check_issue_template, list_open_prs_from_repo, check_pr_template, label_list_issue,
                              pr_reviewed_label)
from stemming.porter2 import stem
from nltk.tokenize import word_tokenize
from auth_credentials import announcement_channel_id, BOT_UID
from slack_functions import (dm_new_users, check_newcomer_requirements,
                             approve_issue_label_slack, assign_issue_slack, claim_issue_slack,
                             open_issue_slack, send_message_ephemeral, send_message_to_channels,
                             slack_team_name_reply, handle_message_answering, view_issue_slack, label_issue_slack)
from nltk.stem import WordNetLemmatizer
from messages import MESSAGE
from apscheduler.scheduler import Scheduler
from dictionaries import repo_vs_channel_id_dict, CHANNEL_LIST

# The list of channels on which the bot will respond to queries


app = Flask(__name__)


def collect_unreviewed_prs():  # pragma: no cover
    for key, value in repo_vs_channel_id_dict.iteritems():
        # Collect PRs for each repo
        pr_list = list_open_prs_from_repo('systers', key)
        if pr_list != '':
            # Constructing message( excluding the last comma from pr_list)
            message = MESSAGE.get('list_of_unreviewed_prs', '%s') % pr_list[0:-1]
            # Send pr_list to respective channels
            send_message_to_channels(value, message)
        else:
            send_message_to_channels(value, MESSAGE.get('no_unreviewed_prs', ""))


schedule = Scheduler(daemon=True)
schedule.add_cron_job(collect_unreviewed_prs, day_of_week='thu', hour=15, minute=30)
schedule.start()


@app.route('/')
def home():
    return 'Response to test hosting.'


# This function will recieve all the github events
@app.route('/web_hook', methods=['POST'])
def github_hook_receiver_function():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        action = data.get('action', None)
        if action is not None:
            if (action == 'opened' or action == 'reopened') and data.get('pull_request', '') == '':
                # If it's an issue opened event and not PR opened event
                issue_number = data.get('issue', {}).get('number', '')
                repo_name = data.get('repository', {}).get('name', '')
                repo_owner = data.get('repository', {}).get('owner', {}).get('login', '')
                issue_body = data.get('issue', {}).get('body', '')
                # Label newly opened issue
                label_opened_issue(data)
                # Check if opened issue follows issue template
                check_issue_template(repo_owner, repo_name, issue_number, issue_body)
                return jsonify({'message': "New issue opened event"})
            elif action == 'created' and data.get('comment', '') != '':
                # If it's a issue comment event
                issue_number = data.get('issue', {}).get('number', '')
                repo_name = data.get('repository', {}).get('name', '')
                repo_owner = data.get('repository', {}).get('owner', {}).get('login', '')
                comment_body = data.get('comment', {}).get('body', '')
                tokens = comment_body.split(' ')
                commenter = data.get('comment', {}).get('user', {}).get('login', '')
                author_association = data.get('comment', {}).get('author_association', '')
                is_issue_claimed_or_assigned = check_multiple_issue_claim(repo_owner, repo_name, issue_number)
                # Check if the comment by coveralls
                if commenter == 'coveralls' and 'Coverage decreased' in comment_body:
                    github_comment(MESSAGE.get('add_tests', ''), repo_owner, repo_name, issue_number)
                    return jsonify({'message': "Coveralls comment"})

                # If comment is for approving issue
                if comment_body.lower().strip().startswith('@sys-bot approve') or \
                        is_variant_of_approve(comment_body.lower()):
                    issue_comment_approve_github(issue_number, repo_name, repo_owner, commenter, False)
                    return jsonify({"message": "Approve command"})

                # If comment is to assign issue
                if comment_body.lower().strip().startswith('@sys-bot assign'):
                    is_approved = check_approved_tag(repo_owner, repo_name, issue_number)
                    if len(tokens) == 3 and not is_issue_claimed_or_assigned and \
                            (author_association == 'COLLABORATOR' or author_association == 'OWNER') and is_approved:
                        issue_assign(issue_number, repo_name, tokens[2], repo_owner)  # pragma: no cover
                    elif len(tokens) != 3 and not is_issue_claimed_or_assigned:
                        github_comment(MESSAGE.get('wrong_format_github', ''), repo_owner, repo_name, issue_number)
                        return jsonify({"message": "Wrong command format"})
                    elif not is_approved:
                        github_comment(MESSAGE.get('not_approved', ''), repo_owner, repo_name, issue_number)
                        return jsonify({"message": "Issue not approved"})
                    elif is_issue_claimed_or_assigned:
                        github_comment(MESSAGE.get('already_claimed', ''), repo_owner, repo_name, issue_number)
                        return jsonify({"message": "Issue already claimed"})
                    elif author_association != 'COLLABORATOR' and author_association != 'OWNER':
                        github_comment(MESSAGE.get('no_permission', ''), repo_owner, repo_name, issue_number)
                        return jsonify({"message": "Not permitted"})

                # If comment is to claim issue
                if comment_body.lower().strip().startswith('@sys-bot claim'):
                    is_approved = check_approved_tag(repo_owner, repo_name, issue_number)
                    if len(tokens) == 2 and not is_issue_claimed_or_assigned and is_approved:  # pragma: no cover
                        assignee = commenter
                        issue_claim_github(assignee, issue_number, repo_name, repo_owner)
                    elif len(tokens) != 2 and not is_issue_claimed_or_assigned:
                        github_comment(MESSAGE.get('wrong_format_github', ''), repo_owner, repo_name, issue_number)
                        return jsonify({"message": "Wrong command format"})
                    elif is_issue_claimed_or_assigned:
                        github_comment(MESSAGE.get('already_claimed', ''), repo_owner, repo_name, issue_number)
                        return jsonify({"message": "Already claimed"})
                    elif not is_approved:
                        github_comment(MESSAGE.get('not_approved', ''), repo_owner, repo_name, issue_number)
                        return jsonify({"message": "Issue not approved"})

                # If comment is to unclaim an issue
                if comment_body.lower().strip().startswith('@sys-bot unclaim'):
                    if len(tokens) == 2:
                        assignee = commenter
                        unassign_issue(repo_owner, repo_name, issue_number, assignee)
                        return jsonify({"message": "Issue unclaimed"})
                    else:
                        github_comment(MESSAGE.get('wrong_format_github', ''), repo_owner, repo_name, issue_number)
                        return jsonify({"message": "Wrong command format"})
                # If comment is to unassign an issue
                if comment_body.lower().strip().startswith('@sys-bot unassign'):
                    if len(tokens) == 3 and (author_association == 'COLLABORATOR' or author_association == 'OWNER'):
                        unassign_issue(repo_owner, repo_name, issue_number, tokens[2])
                        return jsonify({"message": "Issue unassigned"})
                    elif len(tokens) == 3 and (author_association != 'COLLABORATOR' and author_association != 'OWNER'):
                        github_comment(MESSAGE.get('no_permission', ''), repo_owner, repo_name, issue_number)
                    else:
                        github_comment(MESSAGE.get('wrong_format_github', ''), repo_owner, repo_name, issue_number)
                        return jsonify({"message": "Wrong command format"})

                # If comment is for labelling an issue
                if comment_body.lower().strip().startswith("@sys-bot label"):
                    if len(tokens) < 3:
                        github_comment(MESSAGE.get('wrong_format_github', ''), repo_owner, repo_name, issue_number)
                        return jsonify({"message": "Wrong command format"})
                    elif len(tokens) >= 3 and (author_association != 'COLLABORATOR' and author_association != 'OWNER'):
                        github_comment(MESSAGE.get('no_permission', ''), repo_owner, repo_name, issue_number)
                        return jsonify({"message": "Not permitted"})
                    else:
                        response = label_list_issue(repo_owner, repo_name, issue_number, comment_body)
                        return jsonify({"message": response.get("message")})
            elif (action == 'opened' or action == 'reopened') and data.get('pull_request', '') != '':
                # If a new PR has been sent
                pr_number = data.get('number', '')
                repo_name = data.get('repository', {}).get('name', '')
                repo_owner = data.get('repository', {}).get('owner', {}).get('login', '')
                pr_body = data.get('pull_request', {}).get('body', '')
                is_template_followed = check_pr_template(pr_body, repo_owner, repo_name, pr_number)
                if is_template_followed:
                    github_pull_request_label(pr_number, repo_name, repo_owner)
                    # Extract the issue number mentioned in PR body if PR follows template
                    issue_number = pr_body.split('Fixes #')[1].split('\r\n')[0].strip()
                    is_issue_approved = check_approved_tag(repo_owner, repo_name, issue_number)
                    if not is_issue_approved:
                        github_comment(MESSAGE.get('pr_to_unapproved_issue', ''), repo_owner, repo_name, pr_number)
                        close_pr(repo_owner, repo_name, pr_number)
                        return jsonify({"message": "PR sent to unapproved issue"})
                else:
                    return jsonify({"message": "PR template not followed"})
            elif action == "submitted" and data.get("review", "") != "":
                pr_reviewed_label(data)
        return jsonify({"message": "Unknown event"})


@app.route('/challenge', methods=['POST'])
def slack_hook_receiver_function():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        challenge = data.get('challenge', None)
        # The url is sent a challenge data first time to verify the url
        if challenge is not None:
            # If challenge is made, return challenge key as required by the API
            return challenge
        else:
            # Else get the event type
            event = data.get('event', {}).get('type', None)
            user = data.get('event', {}).get('user', None)
            channel = data.get('event', {}).get('channel', None)
            channel_type = data.get('event', {}).get('channel_type', None)
            msg_sub_type = data.get('event', {}).get('subtype')
            condition_subtype = msg_sub_type is None or msg_sub_type == 'message_replied'
            condition_user = user != BOT_UID and user != ''
            if event == 'member_joined_channel':
                # Check that it's a member_joined_channel event
                if channel == announcement_channel_id:
                    # Check if channel_id is the required channel, i.e, Announcements channel
                    dm_new_users(data)
                    return jsonify({'message': 'New member joined'})
            elif event == 'app_mention':
                # Check if app has been mentioned in a query
                slack_team_name_reply(data)
                return jsonify({'message': 'App mentioned'})
            # Check if the message is made on the 3 required channels
            elif event == 'message' and condition_user and condition_subtype and \
                    channel_type == 'channel' and channel in CHANNEL_LIST.values():
                handle_message_answering(data.get('event', {}))
                return jsonify({'message': 'FAQ answered'})
        return json.dumps(request.json)


# Receive responses from sysbot_invite slash command
@app.route('/invite', methods=['POST', 'GET'])
def invite():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        slash_user_info = request.form
        uid = slash_user_info.get('user_id', '')
        channel_id = slash_user_info.get('channel_id', '')
        if uid != "":
            check_newcomer_requirements(uid, channel_id)
    return Response(status=200)


@app.route('/slack_approve_issue', methods=['POST'])
def slack_approval_receiver():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        data = request.form
        approve_issue_label_slack(data)
        return Response(status=200)


@app.route('/slack_assign_issue', methods=['POST'])
def slack_assign_receiver():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        data = request.form
        assign_issue_slack(data)
        return Response(status=200)


@app.route('/claim', methods=['POST'])
def slack_claim_receiver():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        claimers_info = request.form
        claim_issue_slack(claimers_info)
        return Response(status=200)


@app.route('/open_issue', methods=['POST'])
def open_issue_receiver():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        openers_info = request.form
        open_issue_slack(openers_info)
        return Response(status=200)


@app.route('/help', methods=['POST'])
def help_command():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        user_info = request.form
        send_message_ephemeral(user_info.get('channel_id', ''),
                               user_info.get('user_id', ''), MESSAGE.get('help_message', ''))
        return Response(status=200)


@app.route('/view_issue', methods=['POST'])
def view_issue_command():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        event_data = request.form
        view_issue_slack(event_data)
        return Response(status=200)


@app.route('/label', methods=['POST'])
def label_issue():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        event_data = request.form
        label_issue_slack(event_data)
        return Response(status=200)


def get_stems(sentence):
    # Generator expressions with joins are much faster than conversion to strings
    # and appending to stemmed tokens to lists and overheads of string conversion.
    stemmed_sentence = ' '.join(stem(token) for token in word_tokenize(sentence))
    return stemmed_sentence


def lemmatize_sent(sentence):
    # Generator expressions with joins are much faster than conversion to strings
    # and appending to stemmed tokens to lists and overheads of string conversion.
    lemmatized_sentence = ' '.join(WordNetLemmatizer().lemmatize(token) for token in word_tokenize(sentence))
    return lemmatized_sentence


def is_variant_of_approve(sentence):
    stemmed_sentence_tokens = get_stems(sentence).split()
    # All variants of approve like approve, approved, approving and approval have the same stem approv
    return ('approv' in stemmed_sentence_tokens and 'no' not in stemmed_sentence_tokens and
            'not' not in stemmed_sentence_tokens)


if __name__ == '__main__':  # pragma: no cover
    app.run()
