# -*- coding: utf-8 -*-

import requests
from flask import request, json, jsonify
from auth_credentials import  BOT_ACCESS_TOKEN, maintainer_usergroup_id, legacy_token, org_repo_owner
from request_urls import (dm_channel_open_url, dm_chat_post_message_url, get_maintainer_list, get_user_profile_info_url, chat_post_ephimeral_message_url)
from messages import MESSAGE
from github_functions import (send_github_invite, issue_comment_approve_github, issue_assign, check_assignee_validity, check_multiple_issue_claim, open_issue_github)

headers = {'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(BOT_ACCESS_TOKEN)}
headers_legacy_urlencoded = {'Content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer {}'.format(legacy_token)}

def dm_new_users(data):
    #Get user id of the user who joined
    uid = data.get('event',{}).get('user',None)
    if uid != None:
        body = {'user': uid}
        #Open a DM channel to the user. Request goes to im.open
        r = requests.post(dm_channel_open_url, data=json.dumps(body), headers=headers)
        response = r.json()
        if response.get('ok',False):
            #Get the channel just opened for DM
            dm_channel_id = response.get('channel',{}).get('id','')
            if dm_channel_id != '':
                body = {'username': 'Sysbot', 'as_user': True, 'text': MESSAGE.get('first_timer_message','Some error occured'), 'channel': dm_channel_id}
                #Send a DM request
                r = requests.post(dm_chat_post_message_url, data=json.dumps(body), headers=headers)
                print("Response: %s" % json.dumps(r.json()))
                return {'message':'Success','status': 200}
    return {'message':'Data format wrong', 'status':400}


def is_maintainer_comment(commenter_id):
    #Using the id of usergroup maintainers
    body = {'usergroup': maintainer_usergroup_id, 'include_disabled': True}
    #Get list of maintainers. For more info :  usergroups.users.list in Slack API
    r = requests.post(get_maintainer_list, data= body, headers=headers_legacy_urlencoded)
    response = r.json()
    if response.get('ok',False):
        #Extract the maintainers
        maintainers = response.get('users',[])
        if commenter_id in maintainers:
            return {'status': 200, 'is_maintainer': True}
        else:
            return {'status': 200, 'is_maintainer': False}
    else:
        return {'status': 400, 'message': 'Wrong parameters'}


def approve_issue_label_slack(data):
    result = is_maintainer_comment(data.get('user_id', ''))
    channel_id = data.get('channel_id','')
    uid = data.get('user_id','')
    if result.get('is_maintainer', False):
        params = data.get('text','')
        if params != '' and len(params.split(' ')) == 2:
            response = issue_comment_approve_github(params.split(' ')[1], params.split(' ')[0], org_repo_owner)
            status = response.get('status', 500)
            if status == 404:
                #Information given is wrong
                send_message_ephimeral(channel_id, uid, MESSAGE.get('wrong_info',''))
            elif status == 200:
                #Successful labeling
                send_message_ephimeral(channel_id, uid, MESSAGE.get('success',''))
            elif status == 500:
                #Some internal error occured
                send_message_ephimeral(channel_id, uid, MESSAGE.get('error_slash_command',''))
        else:
            #Wrong format of command was used
            send_message_ephimeral(channel_id, uid, MESSAGE.get('correct_approve_format',''))
    else:
        #The commentor is not a maintainer
        send_message_ephimeral(channel_id, uid, MESSAGE.get('not_a_maintainer',''))


def check_newcomer_requirements(uid, channel_id):
    body = {'user': uid, 'include_labels': True}
    get_profile_response = requests.post(get_user_profile_info_url, data=body, headers=headers_legacy_urlencoded)
    profile_response_json = get_profile_response.json()
    if profile_response_json.get('ok', False):
        profile = profile_response_json.get('profile', {})
        custom_fields = profile.get('fields', {})
        github_profile_present = False
        github_id = ""
        for key in custom_fields:
            github_link = custom_fields.get(key, {}).get('value', '')
            if 'github.com/' in github_link:
                github_profile_present = True
                github_id = github_link.split('github.com/')[1]
                break
        if github_profile_present and profile.get('first_name', "") != "" and profile.get('last_name',"")!="" and profile.get('title',"")!="" and profile.get('image_original',"")!="" and not profile.get('phone',"").isdigit():
            send_github_invite(github_id)
            send_message_ephimeral(channel_id, uid, MESSAGE.get('invite_sent',''))
        else:
            send_message_ephimeral(channel_id, uid, MESSAGE.get('newcomer_requirement_incomplete',''))


def assign_issue_slack(data):
    result = is_maintainer_comment(data.get('user_id', ''))
    channel_id = data.get('channel_id','')
    uid = data.get('user_id','')
    if result.get('is_maintainer', False):
        params = data.get('text','')
        tokens = params.split(' ')
        if params != '' and len(tokens) == 3:
            #The tokens are issue number, repo name, and assignee username
            is_issue_claimed_or_assigned = check_multiple_issue_claim(org_repo_owner, tokens[0], tokens[1])
            #If issue has been claimed, send message to the channel
            if is_issue_claimed_or_assigned:
                send_message_ephimeral(channel_id, uid, MESSAGE.get('already_claimed',''))
                return
            #If issue is available, then check for assign status
            status = issue_assign(tokens[1], tokens[0], tokens[2], org_repo_owner)
            if status == 404:
                #Information given is wrong
                send_message_ephimeral(channel_id, uid, MESSAGE.get('wrong_info',''))
            elif status == 200:
                #Successful assignment
                send_message_ephimeral(channel_id, uid, MESSAGE.get('success',''))
            elif status == 500:
                #Some internal error occured
                send_message_ephimeral(channel_id, uid, MESSAGE.get('error_slash_command',''))
        else:
            #Wrong format of command was used
            send_message_ephimeral(channel_id, uid, MESSAGE.get('correct_assign_format',''))
    else:
        #The commentor is not a maintainer
        send_message_ephimeral(channel_id, uid, MESSAGE.get('not_a_maintainer',''))


def claim_issue_slack(data):
    params = data.get('text','')
    tokens = params.split(' ')
    channel_id = data.get('channel_id','')
    uid = data.get('user_id','')
    if params != '' and len(tokens) == 3:
        #The tokens are issue number, repo name, and claimant's username
        is_issue_claimed_or_assigned = check_multiple_issue_claim(org_repo_owner, tokens[0], tokens[1])
        #If issue has been claimed, send message to the channel
        if is_issue_claimed_or_assigned:
            send_message_ephimeral(channel_id, uid, MESSAGE.get('already_claimed',''))
            return
        #If issue is available, then check for assign status
        status = issue_assign(tokens[1], tokens[0], tokens[2], org_repo_owner)
        #If a 404 error status is raised, check if the assignee can be assigned.
        if status == 404:
            #Check assignee status
            assignee_status = check_assignee_validity(tokens[0], tokens[2], org_repo_owner)
            if assignee_status == 404:
                #Can't be assigned as not a member
                send_message_ephimeral(channel_id, uid, MESSAGE.get('not_a_member',''))
                return
            else:
                #Information given is wrong
                send_message_ephimeral(channel_id, uid, MESSAGE.get('wrong_info',''))
        elif status == 200:
            #Successful claim
            send_message_ephimeral(channel_id, uid, MESSAGE.get('success',''))
        elif status == 500:
            #Some internal error occured
            send_message_ephimeral(channel_id, uid, MESSAGE.get('error_slash_command',''))
    else:
        #Wrong format of command was used
        send_message_ephimeral(channel_id, uid, MESSAGE.get('correct_claim_format',''))


def send_message_to_channels(channel_id, message):
    body = {'username': 'Sysbot', 'as_user': True, 'text': message, 'channel': channel_id}
    requests.post(dm_chat_post_message_url, data=json.dumps(body), headers=headers)



def send_message_ephimeral(channel_id, uid, message):
    body = {'username': 'Sysbot', 'as_user': True, 'text': message, 'channel': channel_id, 'user': uid}
    requests.post(chat_post_ephimeral_message_url, data=json.dumps(body), headers=headers)


def open_issue_slack(data):
    channel_id = data.get('channel_id', '')
    #Get the command parameters used by the user
    command_params = data.get('text','')
    #For getting author name and repo name
    tokens = command_params.split(' ')
    #For extracting title and body
    title_body_tokens = command_params.split('*')
    if command_params=="" or len(tokens) < 4 or len(title_body_tokens) <3 or title_body_tokens[1]=='' or title_body_tokens[2]=='':
        send_message_to_channels(channel_id, MESSAGE.get('wrong_params_issue_command',''))
        return
    issue_title = title_body_tokens[1]
    issue_body = title_body_tokens[2]
    status = open_issue_github(org_repo_owner, tokens[0], issue_title, issue_body, tokens[1])
    if status == 201:
        #If issue has been opened successfully
        send_message_to_channels(channel_id, MESSAGE.get('success_issue', ''))
    else:
        send_message_to_channels(channel_id, MESSAGE.get('error_issue', ''))
