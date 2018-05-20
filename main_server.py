from flask import Flask, jsonify
from flask import request, json
from github_functions import label_opened_issue
from stemming.porter2 import stemmer
from nltk.tokenize import word_tokenize
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


def get_stems(sentence):
    #Generator expressions with joins are much faster than conversion to strings and appending to stemmed tokens to lists and overheads of string conversion.
    stemmed_sentence = ' '.join(stemmer.stem(token) for token in word_tokenize(sentence))
    return stemmed_sentence

def lemmatize_sent(sentence):
    #Generator expressions with joins are much faster than conversion to strings and appending to stemmed tokens to lists and overheads of string conversion.
    lemmatized_sentence = ' '.join(WordNetLemmatizer().lemmatize(token) for token in word_tokenize(sentence))
    return lemmatized_sentence

if __name__ == '__main__':
    app.run()
