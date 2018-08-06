"""This module handles and listen to various events."""

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


def label_opened_issue(data):
    """Each newly opened issue is labelled to be 'Not Approced' by the bot.

    param data: json response with key value pairs containing repo
    information. return message: response message and request status
    code.
    """
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
    """Send github invite to join newcomer team.

    Command to get invited to the necomer team and become the member of the
    org. However checks if the newcomer member level is completed.
    param github_id: ID of the github user.
    return: response message and request status code.
    """
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
    """Approve issues via approve comments on Github and via Slack.

    param issue_number: ID of the issue.
    param repo_name: Name of the repository.
    param repo_owner: Owner of the repository.
    param comment_authon: Author of the 'approve' comment.
    param is_from_slack: If the command is made from slack.
    return: response message and request status code.
    """
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
    """Label newly opened PRs with under review label.

    param pr_number: ID of the pull request.
    param repo_name: Name of the repository.
    param repo_owner: Name of the owner.
    return: response status code from post request.
    """
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    label = '["Not Reviewed"]'
    # Add label of under review to new PRs
    request_url = add_label_url % (repo_owner, repo_name, pr_number)
    response = session.post(request_url, data=label, headers=headers)
    return response.status_code


def issue_assign(issue_number, repo_name, assignee, repo_owner):
    """Assign issue via github and slack.

    Assign issues from github and slack.Maintainers and collaborators can assign an issue to a member by the comment.
    param issue_number: ID of the issue.
    param repo_name: Name of the repository.
    param repo_owner: Owner of the issue.
    param assignee: User to whom the issue is to be assigned.
    return: response status code from PATCH request.
    """
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/json'}
    data = '{"assignees": ["%s"]}' % assignee
    # Request to assign the issue
    request_url = assign_issue_url % (repo_owner, repo_name, issue_number)
    response = session.patch(request_url, data=data, headers=headers)
    return response.status_code


def check_assignee_validity(repo_name, assignee, repo_owner):
    """Check if an assignee is valid (if the assignee is a member).

    param repo_name: Name of the repository.
    param assignee: User to whom the issue is assigned.
    param repo_owner: Owner of the repository.
    return: response status code from GET request.
    """
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = check_assignee_url % (repo_owner, repo_name, assignee)
    response = session.get(request_url)
    return response.status_code


def github_comment(message, repo_owner, repo_name, issue_number):
    """Add comments on github with the author as sys-bot.

    param message: Comment message.
    param issue_number: ID of the issue.
    param repo_name: Name of the repository.
    param repo_owner: Owner of the issue.
    return: response status code from POST request.
    """
    body = '{"body":"%s"}' % message
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    headers = {'Accept': 'application/vnd.github.machine-man-preview',
               'Content-Type': 'application/x-www-form-urlencoded'}
    request_url = github_comment_url % (repo_owner, repo_name, issue_number)
    response = session.post(request_url, data=body, headers=headers)
    return response.status_code


def issue_claim_github(assignee, issue_number, repo_name, repo_owner):
    """Assign a user to an issue, .i.e handles both assign and claim commands.

    param assignee: User to whom the issue is to be assigned.
    param issue_number: ID of the issue.
    param repo_name: Name of the repository.
    param repo_owner: Owner of the issue.
    return: response status code from check_assignee_validity().
    """
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
    """Check if same issue is being claimed multiple times.

    param issue_number: ID of the issue.
    param repo_name: Name of the repository.
    param repo_owner: Owner of the issue.
    return: True if the issues has been claimed.
    """
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
    """Open github issue following template.

    Open new issue following Systers template.The issues are opened
    in full markdown format, and the author's name is mentioned at the top.
    param repo_owner: Owner of the repository.
    param repo_name: Name of the repository:
    param issue_tittle: Tittle of the issue.
    param issue_description: Description of the issue.
    param update_list_item: Add checklist .i.e Acceptance Criteria list items.
    param estimation: Estimated time required to work on the issue.
    param author: Author of the issue.
    return: Response status code from POST request.
    """
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
    """Fetch the author of the issues .i.e user who opened the issue.

    param issue_number: ID of the issue.
    param repo_name: Name of the repository.
    param repo_owner: Owner of the issue.
    return: author of the opened issue.
    """
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = get_issue_url % (repo_owner, repo_name, issue_number)
    response = session.get(request_url).json()
    return response.get('user', {}).get('login', '')


def check_approved_tag(repo_owner, repo_name, issue_number):
    """Check if the issues has been approved by maintainers or collaborators.

    param issue_number: ID of the issue.
    param repo_name: Name of the repository.
    param repo_owner: Owner of the issue.
    return: True if the issue is approved.
    """
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = get_labels % (repo_owner, repo_name, issue_number)
    labels = session.get(request_url).json()
    label_approved_present = False
    for label in labels:
        if label.get('name', '') == 'issue-approved':
            label_approved_present = True
        if label.get('name', '') == 'Template Mismatch':
            return False
    return label_approved_present


def unassign_issue(repo_owner, repo_name, issue_number, assignee):
    """Remove the assignee from the issue.

    param repo_owner: Owner of the issue.
    param repo_name: Name of the repository.
    param issue_number: ID of the issue.
    param assignee: User who had been assigned to the issue.
    return: Response status code
    """
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = remove_assignee_url % (repo_owner, repo_name, issue_number)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/json'}
    data = '{"assignees": ["%s"]}' % assignee
    response = session.delete(request_url, data=data, headers=headers)
    return response.status_code


def close_pr(repo_owner, repo_name, pr_number):
    """Close the pull request.

    It could only be closed by members of the org or the user itself.
    param repo_owner: Owner of the issue.
    param repo_name: Name of the repository.
    param pr_number: ID of the issue.
    return: Response status code.
    """
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    request_url = close_pull_request_url % (repo_owner, repo_name, pr_number)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/json'}
    request_body = '{"state": "closed"}'
    # Update PR status to closed
    response = session.patch(request_url, data=request_body, headers=headers)
    return response.status_code


def check_issue_template(repo_owner, repo_name, issue_number, body):
    """Check if issue follows atleast one of 3 templates otherwise labels it.

    param repo_owner: Owner of the issue.
    param repo_name: Name of the repository.
    param issue_number: ID of the issue.
    param body: Description of the issue.
    return: Issue template match or mismatch message.
    """
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
    """Check if issue has all essential components of a template. Used by
    check_issue_template.

    param body: json response with key value pairs of issue template components.
    return: True if all essential componentsa are present.
    """
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
    """List all open PRs from a repo that were opened within 7 days of the
    passed date.

    param repo_owner: Owner of the issue.
    param repo_name: Name of the repository.
    return: list of PRs url, opened within 7 days and marked 'not reviewed'.
    """
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
    """Validate the PR template.

    Check if the PR template is followed .i.e comparing with the necessary elements set of PR template.
    param pr_body: Content of the PR.
    param repo_owner: Owner of the repository.
    param repo_name: Name of the repository.
    param pr_number: ID of the PR.
    return: True if the PR template is followed.
    """
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


def label_list_issue(repo_owner, repo_name, issue_number, comment, commenter):
    """Label the issues within list with proper labels.

    param repo_owner: Owner of the repository.
    param repo_name: Name of the repository.
    param issue_number: ID of the issue.
    param comment: comment message.
    param commenter: ID of the commenter.
    return: response message and status code.
    """
    tokens = comment.split(",")
    labelled = 0
    for label_name in tokens:
        if tokens.index(label_name) == 0:
            label_name = label_name.split("@sys-bot label")[1].strip()
        session = requests.Session()
        session.auth = (USERNAME, PASSWORD)
        if label_name.strip() != "":
            label_request_body = '["%s"]' % label_name.strip()
            request_url = add_label_url % (repo_owner, repo_name, issue_number)
            response = session.post(request_url, data=label_request_body, headers=headers)
            if response.status_code == 200:
                labelled = labelled + 1
    if labelled == len(tokens):
        return {"message": "All labels added to issue", "status": 200}
    elif labelled == 0:
        return {"message": "Some error occurred", "status": 400}
    else:
        return {"message": "Some labels added to issue", "status": 204}


def pr_reviewed_label(data):
    """Label review state (reviewed or under review).

    param data: json response data containing repo information.
    return: succes message and status code.
    """
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    pr_number = data.get("pull_request", {}).get('number', '')
    repo_name = data.get('repository', {}).get('name', '')
    repo_owner = data.get('repository', {}).get('owner', {}).get('login', '')
    # Get state of submitted review
    review_state = data.get("review", {}).get("state", "")
    author_association = data.get("review", {}).get("author_association", "")
    request_url = add_label_url % (repo_owner, repo_name, pr_number)
    if (review_state == "commented" or review_state == "changes_requested") and \
            (author_association == "COLLABORATOR" or author_association == "OWNER"):
        remove_label_not_reviewed = '/Not%20Reviewed'
        remove_label_approved = '/Approved'
        # Delete the not reviewed and approved labels first
        session.delete(request_url + remove_label_not_reviewed, headers=headers)
        session.delete(request_url + remove_label_approved, headers=headers)
        label = '["under review"]'
        response = session.post(request_url, data=label, headers=headers)
        if response.status_code == 200:
            return {"message": "Labelled as under review", "status": 200}
        else:
            return {"message": "Some error occurred", "status": 400}
    elif review_state == "approved" and (author_association == "COLLABORATOR" or author_association == "OWNER"):
        remove_label_not_reviewed = '/Not%20Reviewed'
        remove_label_approved = '/under%20review'
        # Delete the not reviewed and under review labels first
        session.delete(request_url + remove_label_not_reviewed, headers=headers)
        session.delete(request_url + remove_label_approved, headers=headers)
        label = '["approved"]'
        response = session.post(request_url, data=label, headers=headers)
        if response.status_code == 200:
            return {"message": "Labelled as approved", "status": 200}
        else:
            return {"message": "Some error occurred", "status": 400}
    return
