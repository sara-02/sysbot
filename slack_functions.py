# -*- coding: utf-8 -*-

import requests
from flask import request, json, jsonify
from auth_credentials import  BOT_ACCESS_TOKEN, maintainer_usergroup_id, legacy_token
from request_urls import dm_channel_open_url, dm_chat_post_message_url, get_maintainer_list, get_user_profile_info_url
from messages import MESSAGE
from github_functions import send_github_invite, issue_comment_approve_github, issue_assign

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
    if result.get('is_maintainer', False):
        params = data.get('text','')
        if params != '' and len(params.split(' ')) == 2:
            response = issue_comment_approve_github(params.split(' ')[1], params.split(' ')[0], 'systers')
            status = response.get('status', 500)
            if status == 404:
                #Information given is wrong
                send_message_to_channels(channel_id, MESSAGE.get('wrong_info',''))
            elif status == 200:
                #Successful labeling
                send_message_to_channels(channel_id, MESSAGE.get('success',''))
            elif status == 500:
                #Some internal error occured
                send_message_to_channels(channel_id, MESSAGE.get('error_slash_command',''))
        else:
            #Wrong format of command was used
            send_message_to_channels(channel_id, MESSAGE.get('correct_approve_format',''))
    else:
        #The commentor is not a maintainer
        send_message_to_channels(channel_id, MESSAGE.get('not_a_maintainer',''))


def send_message_to_channels(channel_id, message):
    body = {'username': 'Sysbot', 'as_user': True, 'text': message, 'channel': channel_id}
    requests.post(dm_chat_post_message_url, data=json.dumps(body), headers=headers)


def check_newcomer_requirements(uid):
    body = {'user': uid, 'include_labels': True}
    r = requests.post(get_user_profile_info_url, data=body, headers=headers_legacy_urlencoded)
    response = r.json()
    if response.get('ok', False):
        profile = response.get('profile', {})
        custom_fields = profile.get('fields', {})
        github_profile_present = False
        github_id = ""
        for key in custom_fields:
            github_link = custom_fields.get(key, {}).get('value', '')
            if github_link.startswith('https://www.github.com/'):
                github_profile_present = True
                github_id = github_link.split('https://www.github.com/')[1]
                break
        if github_profile_present and profile.get('first_name', "") != "" and profile.get('last_name',"")!="" and profile.get('title',"")!="" and profile.get('image_original',"")!="" and not profile.get('phone',"").isdigit():
            send_github_invite(github_id)
        else:
            data = {"text": MESSAGE.get('newcomer_requirement_incomplete','')}
            headers = {'Content-type': 'application/json'}

            requests.post(dm_chat_post_message_url, data=json.dumps(data), headers=headers)


def assign_issue_slack(data):
    result = is_maintainer_comment(data.get('user_id', ''))
    channel_id = data.get('channel_id','')
    if result.get('is_maintainer', False):
        params = data.get('text','')
        tokens = params.split(' ')
        if params != '' and len(tokens) == 3:
            #The tokens are issue number, repo name, and assignee username
            status = issue_assign(tokens[1], tokens[0], tokens[2], 'systers')
            if status == 404:
                #Information given is wrong
                send_message_to_channels(channel_id, MESSAGE.get('wrong_info',''))
            elif status == 200:
                #Successful assignment
                send_message_to_channels(channel_id, MESSAGE.get('success',''))
            elif status == 500:
                #Some internal error occured
                send_message_to_channels(channel_id, MESSAGE.get('error_slash_command',''))
        else:
            #Wrong format of command was used
            send_message_to_channels(channel_id, MESSAGE.get('correct_assign_format',''))
    else:
        #The commentor is not a maintainer
        send_message_to_channels(channel_id, MESSAGE.get('not_a_maintainer',''))


def send_message_to_channels(channel_id, message):
    body = {'username': 'Sysbot', 'as_user': True, 'text': message, 'channel': channel_id}
    requests.post(dm_chat_post_message_url, data=json.dumps(body), headers=headers)
