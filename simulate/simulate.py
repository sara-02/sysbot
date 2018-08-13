import json
import os
import requests

host = os.environ.get("HOST", "127.0.0.1")
port = os.environ.get("PORT", "5000")
SERVER_URL = "http://{}:{}/".format(host, port)
slack_data = ""
github_data = ""


cwd = os.path.dirname(os.path.realpath(__file__))

with open(cwd + '/data/github_data.json') as f:
    github_data = json.load(f)

with open(cwd + '/data/slack_data.json') as f:
    slack_data = json.load(f)

header_application_json = {
    "Content-Type": "application/json"
}
header_application_form = {
    "Content-Type": "application/x-www-form-urlencoded"
}


def simulate_all():
    simulate_github_events()
    simulate_slack_events()


def simulate_github_events():
    github_approve_comment()
    github_claim_comment()
    github_assign_comment()
    github_unclaim_comment()
    github_unassign_comment()
    github_issue_opened()
    github_pr_opened()


def simulate_slack_events():
    slack_app_mention()
    slack_challenge()
    slack_channel_message()
    slack_member_joined_channel()
    slack_sysbot_approve_issue()
    slack_sysbot_assign_issue()
    slack_sysbot_claim()
    slack_sysbot_help()
    slack_sysbot_invite()
    slack_sysbot_open_issue()


def github_approve_comment():
    response = requests.post(SERVER_URL + "web_hook", data=json.dumps(github_data['approve_comment']),
                             headers=header_application_json)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def github_claim_comment():
    response = requests.post(SERVER_URL + "web_hook", data=json.dumps(github_data['claim_comment']),
                             headers=header_application_json)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def github_assign_comment():
    response = requests.post(SERVER_URL + "web_hook", data=json.dumps(github_data['assign_comment']),
                             headers=header_application_json)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def github_unclaim_comment():
    response = requests.post(SERVER_URL + "web_hook", data=json.dumps(github_data['unclaim_comment']),
                             headers=header_application_json)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def github_unassign_comment():
    response = requests.post(SERVER_URL + "web_hook", data=json.dumps(github_data['unassign_comment']),
                             headers=header_application_json)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def github_issue_opened():
    response = requests.post(SERVER_URL + "web_hook", data=json.dumps(github_data['issue_opened']),
                             headers=header_application_json)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def github_pr_opened():
    response = requests.post(SERVER_URL + "web_hook", data=json.dumps(github_data['pr_opened']),
                             headers=header_application_json)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def slack_sysbot_invite():
    response = requests.post(SERVER_URL + "invite", data=json.dumps(slack_data['sysbot_invite']),
                             headers=header_application_form)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def slack_sysbot_help():
    response = requests.post(SERVER_URL + "help", data=json.dumps(slack_data['sysbot_help']),
                             headers=header_application_form)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def slack_sysbot_approve_issue():
    response = requests.post(SERVER_URL + "slack_approve_issue", data=json.dumps(slack_data['sysbot_approve_issue']),
                             headers=header_application_form)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def slack_sysbot_assign_issue():
    response = requests.post(SERVER_URL + "slack_assign_issue", data=json.dumps(slack_data['sysbot_assign_issue']),
                             headers=header_application_form)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def slack_sysbot_claim():
    response = requests.post(SERVER_URL + "claim", data=json.dumps(slack_data['sysbot_claim']),
                             headers=header_application_form)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def slack_sysbot_open_issue():
    response = requests.post(SERVER_URL + "open_issue", data=json.dumps(slack_data['sysbot_open_issue']),
                             headers=header_application_form)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def slack_member_joined_channel():
    response = requests.post(SERVER_URL + "challenge", data=json.dumps(slack_data['member_joined_channel']),
                             headers=header_application_json)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def slack_app_mention():
    response = requests.post(SERVER_URL + "challenge", data=json.dumps(slack_data['app_mention']),
                             headers=header_application_json)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def slack_challenge():
    response = requests.post(SERVER_URL + "challenge", data=json.dumps(slack_data['challenge']),
                             headers=header_application_json)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


def slack_channel_message():
    response = requests.post(SERVER_URL + "challenge", data=json.dumps(slack_data['channel_message']),
                             headers=header_application_json)
    if response.status_code == 200:
        print("Success")
    else:
        print(response.reason)


if __name__ == '__main__':
    simulate_all()
