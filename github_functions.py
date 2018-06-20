import requests
from flask import request, json
from request_urls import (add_label_url, send_team_invite, assign_issue_url, check_assignee_url, github_comment_url, get_issue_url, open_issue_url, get_labels, remove_assignee_url)
from auth_credentials import USERNAME,PASSWORD, newcomers_team_id
from messages import MESSAGE

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


def send_github_invite(github_id):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    #Header as required by Github API
    headers = {'Accept': 'application/vnd.github.hellcat-preview+json',
               'Content-Type': 'application/x-www-form-urlencoded'}
    request_url =  send_team_invite %(newcomers_team_id, github_id)
    r = session.put(request_url, data=json.dumps({'role': 'member'}), headers=headers)
    if r.status_code == 200:
        return {'message':'Success', 'status':r.status_code}
    else:
        return {'message':'Error', 'status':r.status_code}
    return {'message':'Data provided is wrong', 'status': 400}


def issue_comment_approve_github(issue_number, repo_name, repo_owner, comment_author, is_from_slack):
    if not is_from_slack:
        issue_author = get_issue_author(repo_owner, repo_name, issue_number)
        if issue_author == comment_author:
            github_comment(MESSAGE.get('author_cannot_approve',''), repo_owner, repo_name, issue_number)
            return
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    #Name of label to be removed
    remove_label_name = '/Not%20Approved'
    #Label to be added
    label = '["issue-approved"]'
    request_url = add_label_url % (repo_owner, repo_name, issue_number)
    #Delete the not approved label first
    response = session.delete(request_url+remove_label_name, headers=headers)
    if response.status_code == 200 or response.status_code == 404:
        #Add the new label
        response = session.post(request_url, data=label, headers=headers)
        if response.status_code == 200:
            return {'message':'Success', 'status':response.status_code}
        else:
            return {'message':'Error', 'status':response.status_code}
    return {'message':'Data provided is wrong', 'status': 400}


def github_pull_request_label(pr_number, repo_name, repo_owner):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/x-www-form-urlencoded'}
    label = '["under review"]'
    #Add label of under review to new PRs
    request_url = add_label_url % (repo_owner, repo_name, pr_number)
    response = session.post(request_url, data=label, headers=headers)
    return response.status_code


def issue_assign(issue_number, repo_name, assignee, repo_owner):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/json'}
    data = '{"assignees": ["%s"]}' % assignee
    #Request to assign the issue
    request_url = assign_issue_url % (repo_owner, repo_name, issue_number)
    response = session.patch(request_url, data=data, headers=headers)
    return response.status_code


def check_assignee_validity(repo_name, assignee, repo_owner):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = check_assignee_url % (repo_owner, repo_name, assignee)
    response = session.get(request_url)
    return response.status_code


def github_comment(message,repo_owner, repo_name,issue_number):
    body = '{"body":"%s"}' % message
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    headers = {'Accept': 'application/vnd.github.machine-man-preview',
               'Content-Type': 'application/x-www-form-urlencoded'}
    request_url = github_comment_url % (repo_owner, repo_name, issue_number)
    response = session.post(request_url, data=body, headers=headers)
    return response.status_code


def issue_claim_github(assignee, issue_number, repo_name, repo_owner):
    status = check_assignee_validity(repo_name, assignee, repo_owner)
    #Check if the assignee is valid. For more info : https://developer.github.com/v3/issues/assignees/#check-assignee
    if status == 404:
        #If member cant be assigned
        github_comment(MESSAGE.get('not_an_org_member', ''),
                       repo_owner, repo_name, issue_number)
    if status == 204:
        #If member can be assigned an issue.
        issue_assign(issue_number, repo_name, assignee, repo_owner)


def check_multiple_issue_claim(repo_owner, repo_name, issue_number):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = get_issue_url % (repo_owner, repo_name, issue_number)
    response = session.get(request_url).json()
    #Get the list of assignees
    assignee_list = response.get('assignees', [])
    if not assignee_list:
        #If issue hasn't been claimed send False
        return False
    else:
        #If issue has been claimed send True
        return True


def open_issue_github(repo_owner, repo_name, issue_title, issue_body, author):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = open_issue_url % (repo_owner, repo_name)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/json'}
    #Raw issue body.
    issue_request_body = '{"title": "%s", "body": "%s.<br>Authored by %s via Slack", "assignees": [], "labels": []}' % (issue_title, issue_body, author)
    response = session.post(request_url, data=issue_request_body, headers=headers)
    return response.status_code


def get_issue_author(repo_owner, repo_name, issue_number):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = get_issue_url % (repo_owner, repo_name, issue_number)
    response = session.get(request_url).json()
    return response.get('user', {}).get('login', '')


def check_approved_tag(repo_owner, repo_name, issue_number):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = get_labels % (repo_owner, repo_name, issue_number)
    labels = session.get(request_url).json()
    for label in labels:
        if label.get('name', '') == 'issue-approved':
            return True
    return False


def unassign_issue(repo_owner, repo_name, issue_number, assignee):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = remove_assignee_url % (repo_owner, repo_name, issue_number)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/json'}
    data = '{"assignees": ["%s"]}' % assignee
    response = session.delete(request_url, data=data, headers=headers)
    return response.status_code
