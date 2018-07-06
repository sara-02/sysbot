from flask import Flask, jsonify
from flask import request, json, Response
from github_functions import (label_opened_issue, issue_comment_approve_github,
                              github_pull_request_label, issue_assign, github_comment, issue_claim_github,
                              check_multiple_issue_claim, check_approved_tag, unassign_issue, close_pr,
                              check_issue_template, list_open_prs_from_repo)
from stemming.porter2 import stem
from nltk.tokenize import word_tokenize
from auth_credentials import announcement_channel_id
from slack_functions import (dm_new_users, check_newcomer_requirements,
                             approve_issue_label_slack, assign_issue_slack, claim_issue_slack,
                             open_issue_slack, send_message_ephimeral, send_message_to_channels,
                             slack_team_name_reply)
from nltk.stem import WordNetLemmatizer
from messages import MESSAGE
from apscheduler.schedulers.background import BackgroundScheduler
from dictionaries import repo_vs_channel_id_dict

app = Flask(__name__)


def collect_unreviewed_prs():
    for key, value in repo_vs_channel_id_dict.iteritems():
        # Collect PRs for each repo
        pr_list = list_open_prs_from_repo('systers', key)
        if pr_list != '':
            # Constructing message( excluding the last comma from pr_list)
            message = MESSAGE.get('list_of_unreviewed_prs', '%s') % pr_list[0:-1]
            # Send pr_list to respective channels
            send_message_to_channels(value, message)


schedule = BackgroundScheduler(daemon=True)
schedule.add_job(collect_unreviewed_prs, 'interval', days=7)
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
            if action == 'opened' and data.get('pull_request', '') == '':
                # If it's an issue opened event and not PR opened event
                issue_number = data.get('issue', {}).get('number', '')
                repo_name = data.get('repository', {}).get('name', '')
                repo_owner = data.get('repository', {}).get('owner', {}).get('login', '')
                issue_body = data.get('issue', {}).get('body', '')
                # Label newly opened issue
                label_opened_issue(data)
                # Check if opened issue follows issue template
                check_issue_template(repo_owner, repo_name, issue_number, issue_body)
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

                # If comment is for approving issue
                if comment_body.lower() == '@sys-bot approve':
                    issue_comment_approve_github(issue_number, repo_name, repo_owner, commenter, False)
                    return jsonify(request.json)

                # If comment is to assign issue
                if comment_body.lower().startswith('@sys-bot assign'):
                    is_approved = check_approved_tag(repo_owner, repo_name, issue_number)
                    if len(tokens) == 3 and not is_issue_claimed_or_assigned and \
                            (author_association == 'COLLABORATOR' or author_association == 'OWNER') and is_approved:
                        issue_assign(issue_number, repo_name, tokens[2], repo_owner)
                    elif len(tokens) != 3 and not is_issue_claimed_or_assigned:
                        github_comment(MESSAGE.get('wrong_format_github', ''), repo_owner, repo_name, issue_number)
                    elif not is_approved:
                        github_comment(MESSAGE.get('not_approved', ''), repo_owner, repo_name, issue_number)
                    elif is_issue_claimed_or_assigned:
                        github_comment(MESSAGE.get('already_claimed', ''), repo_owner, repo_name, issue_number)
                    elif author_association != 'COLLABORATOR' and author_association != 'OWNER':
                        github_comment(MESSAGE.get('no_permission', ''), repo_owner, repo_name, issue_number)
                    return jsonify(request.json)

                # If comment is to claim issue
                if comment_body.lower().startswith('@sys-bot claim'):
                    is_approved = check_approved_tag(repo_owner, repo_name, issue_number)
                    if len(tokens) == 2 and not is_issue_claimed_or_assigned and is_approved:
                        assignee = commenter
                        issue_claim_github(assignee, issue_number, repo_name, repo_owner)
                    elif len(tokens) != 2 and not is_issue_claimed_or_assigned:
                        github_comment(MESSAGE.get('wrong_format_github', ''), repo_owner, repo_name, issue_number)
                    elif is_issue_claimed_or_assigned:
                        github_comment(MESSAGE.get('already_claimed', ''), repo_owner, repo_name, issue_number)
                    elif not is_approved:
                        github_comment(MESSAGE.get('not_approved', ''), repo_owner, repo_name, issue_number)
                    elif is_issue_claimed_or_assigned:
                        github_comment(MESSAGE.get('already_claimed', ''), repo_owner, repo_name, issue_number)
                    return jsonify(request.json)

                # If comment is to unclaim an issue
                if comment_body.lower().startswith('@sys-bot unclaim'):
                    if len(tokens) == 2:
                        assignee = commenter
                        unassign_issue(repo_owner, repo_name, issue_number, assignee)
                    else:
                        github_comment(MESSAGE.get('wrong_format_github', ''), repo_owner, repo_name, issue_number)

                # If comment is to unassign an issue
                if comment_body.lower().startswith('@sys-bot unassign'):
                    if len(tokens) == 3:
                        unassign_issue(repo_owner, repo_name, issue_number, tokens[2])
                    else:
                        github_comment(MESSAGE.get('wrong_format_github', ''), repo_owner, repo_name, issue_number)
            elif action == 'opened' and data.get('pull_request', '') != '':
                # If a new PR has been sent
                pr_number = data.get('number', '')
                repo_name = data.get('repository', {}).get('name', '')
                repo_owner = data.get('repository', {}).get('owner', {}).get('login', '')
                github_pull_request_label(pr_number, repo_name, repo_owner)
                pr_body = data.get('pull_request', {}).get('body', '')
                if pr_body != '':
                    # Extract the issue number mentioned in PR body if PR follows template
                    issue_number = pr_body.split('Fixes #')[1].split('\r\n')[0].strip()
                    if issue_number != '':
                        is_issue_approved = check_approved_tag(repo_owner, repo_name, issue_number)
                        if not is_issue_approved:
                            github_comment(MESSAGE.get('pr_to_unapproved_issue', ''), repo_owner, repo_name, pr_number)
                            close_pr(repo_owner, repo_name, pr_number)
        else:
            pass
            # Currently the bot isn't handeling any other cases
        return jsonify(request.json)


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
            if event == 'member_joined_channel':
                # Check that it's a member_joined_channel event
                channel = data.get('event', {}).get('channel', None)
                if channel == announcement_channel_id:
                    # Check if channel_id is the required channel, i.e, Announcements channel
                    dm_new_users(data)
            elif event == 'app_mention':
                # Check if app has been mentioned in a query
                slack_team_name_reply(data)
        return json.dumps(request.json)


# Recieve responses from sysbot_invite slash command
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
        send_message_ephimeral(user_info.get('channel_id', ''),
                               user_info.get('user_id', ''), MESSAGE.get('help_message', ''))
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

if __name__ == '__main__':
    app.run()
