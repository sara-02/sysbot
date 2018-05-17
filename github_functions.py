import requests
from flask import request, json
from request_urls import *
from auth_credentials import *

# labels newly opened issues with "Not Approved" tag
def label_opened_issue(data):
    session = requests.Session()
    #create a authenticated session
    session.auth = (USERNAME, PASSWORD)
    #extract issue and repo data from webhook's response
    issue_number = data['issue']['number']
    repo_name = data['repository']['name']
    repo_owner = data['repository']['owner']['login']
    # Request headers
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/x-www-form-urlencoded'}
    #raw body( string ) with list of tags
    label = '["Not Approved"]'
    #construct the request url
    request_url = add_label_url % (repo_owner, repo_name,issue_number)
    #send request
    r = session.post(request_url, data=label, headers=headers)
    #check response
    if r.status_code == 201:
        print 'Successfully created label'
    else:
        print 'Unsuccessful.Response:', r.content
    return
