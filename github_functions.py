import requests
from flask import request, json
from request_urls import add_label_url
from auth_credentials import USERNAME,PASSWORD

#request headers
headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/x-www-form-urlencoded'}

#labels newly opened issues with "Not Approved" tag
def label_opened_issue(data):
    session = requests.Session()
    #create a authenticated session
    session.auth = (USERNAME, PASSWORD)
    #extract issue and repo data from webhook's response
    issue_number = data.get('issue',{}).get('number',-1)
    repo_name = data.get('repository',{}).get('name','')
    repo_owner = data.get('repository',{}).get('owner',{}).get('login',"")
    #raw body( string ) with list of tags
    label = '["Not Approved"]'
    #construct the request url
    request_url = add_label_url % (repo_owner, repo_name,issue_number)
    if issue_number !=-1 and repo_name !="" and repo_owner!="":
        #send request
        r = session.post(request_url, data=label, headers=headers)
        #check response
        if r.status_code == 201:
            print('Success')
            return {'message':'Success', 'status':r.status_code}
        else:
            print(r.content)
            return {'message':'Error', 'status':r.status_code}
    return {'message':'Format of data provided is wrong or misformed', 'status': 400}
