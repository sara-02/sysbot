# -*- coding: utf-8 -*-

import requests
from flask import request, json, jsonify
from auth_credentials import  BOT_ACCESS_TOKEN, maintainer_usergroup_id, legacy_token
from request_urls import dm_channel_open_url, dm_chat_post_message_url, get_maintainer_list
from messages import MESSAGE

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
            return {'status': 200, 'is_maintainer': True}
    else:
        return {'status': 400, 'message': 'Wrong parameters'}
