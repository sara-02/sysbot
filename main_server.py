from flask import Flask, jsonify
from flask import request, json, Response
from github_functions import label_opened_issue, issue_comment_approve_github, github_pull_request_label, issue_assign
from stemming.porter2 import stem
from nltk.tokenize import word_tokenize
from auth_credentials import announcement_channel_id, BOT_ACCESS_TOKEN
from slack_functions import dm_new_users, check_newcomer_requirements, approve_issue_label_slack, assign_issue_slack
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)


@app.route('/')
def home():
    return 'Response to test hosting.'

#This function will recieve all the github events
@app.route('/web_hook', methods=['POST'])
def github_hook_receiver_function():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        print(json.dumps(data))
        action = data.get('action', None)
        if action!=None:
            if action == 'opened' and data.get('pull_request', '') == '':
                #If it's an issue opened event and not PR opened event
                response = label_opened_issue(data)
            elif action == 'created' and data.get('comment', '') != '':
                #If it's a issue comment event
                issue_number = data.get('issue', {}).get('number', '')
                repo_name = data.get('repository', {}).get('name', '')
                repo_owner = data.get('repository', {}).get('owner', {}).get('login', '')
                comment_body = data.get('comment', {}).get('body', '')
                tokens = comment_body.split(' ')
                #If comment is for approving issue
                if comment_body.lower() == '@sys-bot approve':
                    issue_comment_approve_github(issue_number, repo_name, repo_owner)
                #If comment is to assign issue
                elif comment_body.lower().startswith('@sys-bot assign') and len(tokens) == 3:
                    issue_assign(issue_number, repo_name, tokens[2], repo_owner)
            elif action == 'opened' and data.get('pull_request', '') != '':
                #If a new PR has been sent
                pr_number = data.get('number', '')
                repo_name = data.get('repository', {}).get('name', '')
                repo_owner = data.get('repository', {}).get('owner', {}).get('login', '')
                github_pull_request_label(pr_number, repo_name, repo_owner)
        else:
            pass
            #currently the bot isn't handeling any other cases
        return jsonify(request.json)


@app.route('/challenge', methods=['POST'])
def slack_hook_receiver_function():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        challenge = data.get('challenge',None)
        #The url is sent a challenge data first time to verify the url
        if challenge != None:
            #If challenge is made, return challenge key as required by the API
            return challenge
        else:
            #Else get the event type
            event = data.get('event',{}).get('type', None)
            if event == 'member_joined_channel':
                #Check that it's a member_joined_channel event
                channel = data.get('event',{}).get('channel', None)
                if channel == announcement_channel_id:
                    #Check if channel_id is the required channel, i.e, Announcements channel
                    dm_new_users(data)
        return json.dumps(request.json)

#Recieve responses from sysbot_invite slash command
@app.route('/invite', methods=['POST', 'GET'])
def invite():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        slash_user_info = request.form
        uid = slash_user_info.get('user_id','')
        if uid != "":
            check_newcomer_requirements(uid)
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


def get_stems(sentence):
    #Generator expressions with joins are much faster than conversion to strings and appending to stemmed tokens to lists and overheads of string conversion.
    stemmed_sentence = ' '.join(stem(token) for token in word_tokenize(sentence))
    return stemmed_sentence

def lemmatize_sent(sentence):
    #Generator expressions with joins are much faster than conversion to strings and appending to stemmed tokens to lists and overheads of string conversion.
    lemmatized_sentence = ' '.join(WordNetLemmatizer().lemmatize(token) for token in word_tokenize(sentence))
    return lemmatized_sentence

if __name__ == '__main__':
    app.run()
