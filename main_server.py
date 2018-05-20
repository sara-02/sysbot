from flask import Flask, jsonify
from flask import request, json
from github_functions import label_opened_issue
from stemming.porter2 import stem
from nltk.tokenize import word_tokenize
from auth_credentials import announcement_channel_id, BOT_ACCESS_TOKEN
from slack_functions import dm_new_users

app = Flask(__name__)


@app.route('/')
def home():
    return 'Response to test hosting.'

#This function will recieve all the github events
@app.route('/web_hook', methods=['POST'])
def github_hook_receiver_function():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        action = data.get('action', None)
        if action!=None:
            if action == 'opened':
                #If it's an issue opened event
                response = label_opened_issue(data)
            #No other events are being handeled currently
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


def get_stems(sentence):
    #Generator expressions with joins are much faster than conversion to strings and appending to stemmed tokens to lists and overheads of string conversion.
    stemmed_sentence = ' '.join(stem(token) for token in word_tokenize(sentence))
    return stemmed_sentence

if __name__ == '__main__':
    app.run()
