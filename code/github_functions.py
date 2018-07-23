import requests
from flask import json
from request_urls import (add_label_url, send_team_invite, assign_issue_url,
                          check_assignee_url, github_comment_url, get_issue_url, open_issue_url,
                          get_labels, remove_assignee_url, close_pull_request_url, list_open_prs_url)
from auth_credentials import USERNAME, PASSWORD, newcomers_team_id
from messages import MESSAGE
from datetime import datetime


# Request headers
headers = {
    'Accept': 'application/vnd.github.symmetra-preview+json',
    'Content-Type': 'application/x-www-form-urlencoded'
}


# Labels newly opened issues with "Not Approved" tag
def label_opened_issue(data):
    session = requests.Session()
    # Create a authenticated session
    session.auth = (USERNAME, PASSWORD)
    # Extract issue and repo data from webhook's response
    issue_number = data.get('issue', {}).get('number', -1)
    repo_name = data.get('repository', {}).get('name', '')
    repo_owner = data.get('repository', {}).get('owner', {}).get('login', "")
    # Raw body( string ) with list of tags
    label = '["Not Approved"]'
    # Construct the request url
    request_url = add_label_url % (repo_owner, repo_name, issue_number)
    if issue_number != -1 and repo_name != "" and repo_owner != "":
        # Send request
        r = session.post(request_url, data=label, headers=headers)
        # Check response
        if r.status_code == 200:
            return {'message': 'Success', 'status': r.status_code}
        else:
            return {'message': 'Error', 'status': r.status_code}
    return {'message': 'Format of data provided is wrong or misformed', 'status': 400}


def send_github_invite(github_id):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # Header as required by Github API
    headers = {'Accept': 'application/vnd.github.hellcat-preview+json',
               'Content-Type': 'application/x-www-form-urlencoded'}
    request_url = send_team_invite % (newcomers_team_id, github_id)
    r = session.put(request_url, data=json.dumps({'role': 'member'}), headers=headers)
    if r.status_code == 200:
        return {'message': 'Success', 'status': r.status_code}
    else:
        return {'message': 'Error', 'status': r.status_code}


def issue_comment_approve_github(issue_number, repo_name, repo_owner, comment_author, is_from_slack):
    if not is_from_slack:
        issue_author = get_issue_author(repo_owner, repo_name, issue_number)
        if issue_author == comment_author:
            github_comment(MESSAGE.get('author_cannot_approve', ''), repo_owner, repo_name, issue_number)
            return {'message': 'Author cannot approve.', 'status': 400}
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # Name of label to be removed
    remove_label_name = '/Not%20Approved'
    # Label to be added
    label = '["issue-approved"]'
    request_url = add_label_url % (repo_owner, repo_name, issue_number)
    # Delete the not approved label first
    response = session.delete(request_url + remove_label_name, headers=headers)
    if response.status_code == 200 or response.status_code == 404:
        # Add the new label
        response = session.post(request_url, data=label, headers=headers)
        if response.status_code == 200:
            return {'message': 'Success', 'status': response.status_code}
        else:
            return {'message': 'Error', 'status': response.status_code}
    return {'message': 'Data provided is wrong', 'status': 400}


def github_pull_request_label(pr_number, repo_name, repo_owner):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    label = '["Not Reviewed"]'
    # Add label of under review to new PRs
    request_url = add_label_url % (repo_owner, repo_name, pr_number)
    response = session.post(request_url, data=label, headers=headers)
    return response.status_code


def issue_assign(issue_number, repo_name, assignee, repo_owner):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/json'}
    data = '{"assignees": ["%s"]}' % assignee
    # Request to assign the issue
    request_url = assign_issue_url % (repo_owner, repo_name, issue_number)
    response = session.patch(request_url, data=data, headers=headers)
    return response.status_code


def check_assignee_validity(repo_name, assignee, repo_owner):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = check_assignee_url % (repo_owner, repo_name, assignee)
    response = session.get(request_url)
    return response.status_code


def github_comment(message, repo_owner, repo_name, issue_number):
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
    # Check if the assignee is valid
    if status == 404:
        # If member cant be assigned
        github_comment(MESSAGE.get('not_an_org_member', ''),
                       repo_owner, repo_name, issue_number)
        return {"message": "Not a member of the organization", "status": 404}
    if status == 204:
        # If member can be assigned an issue.
        issue_assign(issue_number, repo_name, assignee, repo_owner)
        return {"message": "Issue claimed", "status": 204}
    return {"status": status}


def check_multiple_issue_claim(repo_owner, repo_name, issue_number):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = get_issue_url % (repo_owner, repo_name, issue_number)
    response = session.get(request_url).json()
    # Get the list of assignees
    assignee_list = response.get('assignees', [])
    if not assignee_list:
        # If issue hasn't been claimed send False
        return False
    else:
        # If issue has been claimed send True
        return True


def open_issue_github(repo_owner, repo_name, issue_title, issue_description, update_list_item, estimation, author):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = open_issue_url % (repo_owner, repo_name)
    # JSON issue body.
    issue_request_body = {
        "title": "%s" % issue_title,
        "body": MESSAGE.get("issue_template") % (author, issue_description, update_list_item, estimation)
    }
    response = session.post(request_url, json=issue_request_body, headers=headers)
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


def close_pr(repo_owner, repo_name, pr_number):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = close_pull_request_url % (repo_owner, repo_name, pr_number)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/json'}
    request_body = '{"state": "closed"}'
    # Update PR status to closed
    response = session.patch(request_url, data=request_body, headers=headers)
    return response.status_code


def check_issue_template(repo_owner, repo_name, issue_number, body):
    if not are_issue_essential_components_present(body):
        session = requests.Session()
        session.auth = (USERNAME, PASSWORD)
        label = '["Template Mismatch"]'
        request_url = add_label_url % (repo_owner, repo_name, issue_number)
        response = session.post(request_url, data=label, headers=headers)
        github_comment(MESSAGE.get('template_mismatch', ''), repo_owner, repo_name, issue_number)
        return {"message": "Issue Template mismatch", "label_status": response.status_code}
    return {"message": "Issue Template match"}


def are_issue_essential_components_present(body):
    tokens = body.split('\r\n')
    # Remove blank strings
    tokens = [s.strip() for s in tokens if s != '']
    # Necessary components in the template: user story
    necessary_elements_set = {'## Description', '## Acceptance Criteria', '### Update [Required]',
                              '## Definition of Done', '## Estimation'}
    # Necessary components in the template: feature request
    necessary_elements_set_feature = {"**Is your feature request related to a problem? Please describe.**",
                                      "**Describe the solution you'd like**", "**Describe alternatives you've considered**"}
    # Necessary components in the template: bug report
    necessary_elements_set_bug_desktop = {"**Describe the bug**", "**To Reproduce**", "**Expected behavior**",
                                          "**Desktop (please complete the following information):**"}
    necessary_elements_set_bug_phone = {"**Describe the bug**", "**To Reproduce**", "**Expected behavior**",
                                        "**Smartphone (please complete the following information):**"}
    if set(tokens).intersection(necessary_elements_set) == necessary_elements_set:
        # Check if the template format has been followed and contents under any header isn't empty
        if tokens[tokens.index('## Description') + 1] != '## Mocks' and tokens[tokens.index('## Description') + 1] != \
                '## Acceptance Criteria' and tokens[
                tokens.index('## Acceptance Criteria') + 1] == '### Update [Required]' \
                and tokens[tokens.index('### Update [Required]') + 1] != '## Definition of Done' and \
                tokens[tokens.index('### Update [Required]') + 1] != '### Enhancement to Update [Optional]' and \
                tokens[tokens.index('## Definition of Done') + 1] != '## Estimation' and \
                tokens[-1] != '## Estimation':
            return True
    elif set(tokens).intersection(necessary_elements_set_feature) == necessary_elements_set_feature:
        if tokens[tokens.index("**Is your feature request related to a problem? Please describe.**") + 1] != \
                "**Describe the solution you'd like**" and tokens[
                tokens.index("**Describe the solution you'd like**") + 1] != \
                "**Describe alternatives you've considered**":
            return True
    elif set(tokens).intersection(necessary_elements_set_bug_desktop) == necessary_elements_set_bug_desktop or \
            set(tokens).intersection(necessary_elements_set_bug_phone) == necessary_elements_set_bug_phone:
        if tokens[tokens.index("**Describe the bug**") + 1] != "**To Reproduce**" and \
                tokens[tokens.index("**To Reproduce**") + 1] != "**Expected behavior**" and \
                (tokens[tokens.index("**Expected behavior**") + 1] !=
                 "**Desktop (please complete the following information):**" or
                 tokens[tokens.index("**Expected behavior**") + 1] !=
                 "**Smartphone (please complete the following information):**"):
            return True
    return False


def list_open_prs_from_repo(repo_owner, repo_name):  # pragma: no cover
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = list_open_prs_url % (repo_owner, repo_name)
    pr_list = session.get(request_url).json()
    pr_url_list = ""
    for pr in pr_list:
        today = datetime.now()
        try:
            opened_date = datetime.strptime(pr.get('created_at', ''), "%Y-%m-%dT%H:%M:%SZ")
            if (today - opened_date).days <= 7:
                labels = pr.get('labels', '')
                for label in labels:
                    if label.get('name', '') == "not reviewed":
                        pr_url_list = pr_url_list + pr.get('html_url', '') + ','
                        break
        except AttributeError:
            pass
    return pr_url_list


def check_pr_template(pr_body, repo_owner, repo_name, pr_number):
    tokens = pr_body.split('\r\n')
    # Remove blank strings
    tokens = [s.strip() for s in tokens if s != '']
    # Necessary components in the PR template
    necessary_elements_set = {'# Description', '# Type of Change:', '# How Has This Been Tested?',
                              '# Checklist:'}
    # Check if issue linking statement is present
    if 'Fixes #' not in pr_body:
        github_comment(MESSAGE.get('pr_not_linked_to_issue'), repo_owner, repo_name, pr_number)
        close_pr(repo_owner, repo_name, pr_number)
        return False
    else:
        # Checking if issue number is provided
        for token in tokens:
            if 'Fixes #' in token:
                issue_number = token.split('Fixes #')[1]
                if not issue_number.isdigit():
                    github_comment(MESSAGE.get('pr_not_linked_to_issue'), repo_owner, repo_name, pr_number)
                    close_pr(repo_owner, repo_name, pr_number)
                    return False
    # Check if the template format has been followed and contents under any header isn't empty
    if set(tokens).intersection(necessary_elements_set) == necessary_elements_set:
        if tokens[tokens.index('# Description') + 1] != '# Type of Change:' and \
                tokens[tokens.index('# Type of Change:') + 1] != '# How Has This Been Tested?' and \
                tokens[tokens.index('# How Has This Been Tested?') + 1] != '# Checklist:' and \
                tokens[-1] != '# Checklist:':
            return True

    github_comment(MESSAGE.get('pr_template_not_followed'), repo_owner, repo_name, pr_number)
    close_pr(repo_owner, repo_name, pr_number)
    return False
