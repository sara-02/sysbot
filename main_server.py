from flask import Flask
from flask import request, json
from github_functions import label_opened_issue
from stemming.porter2 import stemmer
from nltk.tokenize import word_tokenize

app = Flask(__name__)


@app.route('/')
def home():
    return 'Response to test hosting.'

#This function will recieve all the github events
@app.route('/web_hook', methods=['POST'])
def github_hook_receiver_function():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        try:
            #This try-catch is checking if action key is present in event data passed by hook
            action = data['action']
            if action == 'opened':
                # If it's an issue opened event
                label_opened_issue(data)
            #No other events are being handled currently
        except KeyError:
            #Currently the bot isn't handling any other cases
            pass
        return json.dumps(request.json)


def get_stems(sentence):
    #Generator expressions with joins are much faster than conversion to strings and appending to stemmed tokens to lists and overheads of string conversion.
    stemmed_sentence = ' '.join(stemmer.stem(token) for token in word_tokenize(sentence))
    return stemmed_sentence

if __name__ == '__main__':
    app.run()
