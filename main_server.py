from flask import Flask
from flask import request, json
from github_functions import label_opened_issue
from stemming.porter2 import stem
from nltk.tokenize import word_tokenize

app = Flask(__name__)


@app.route('/')
def home():
    return 'Response to test hosting.'

#this function will recieve all the github events
@app.route('/web_hook', methods=['POST'])
def github_hook_receiver_function():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        try:
            # This try catch is checking if action key is present in event data passed by hook
            action = data['action']
            if action == 'opened':
                # If it's an issue opened event
                label_opened_issue(data)
            # No other events are being handeled currently
        except KeyError:
            #currently the bot isn't handeling any other cases
            pass
        return json.dumps(request.json)


def get_stems(sentence):
    result = list()
    tokens = word_tokenize(sentence)
    for word in tokens:
        result.append(stem(word))
    return result

if __name__ == '__main__':
    app.run()
