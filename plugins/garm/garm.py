#!/usr/bin/env python3
import datetime

import requests
from pytz import timezone
from slackbot.bot import respond_to, listen_to
from api import CybApi

from settings import api_url, api_client_id, \
                api_client_secret, api_password, api_username

api = CybApi(api_username, api_password, api_client_id, api_client_secret, api_url)

role_lis = {
        "design": 24,
        "arkiv": 26,
        "web": 23,
        "dj": 20,
        "kafefunk": 19,
        "barfunk": 18,
        "arrmester": 17,
        "kaffemester": 16,
        "skjenkemester": 15
        }


@respond_to(r'!garm (.*)')
@listen_to(r'!garm (.*)')
def garm(message, what=None):
    args = what.split()
    user = message.channel._client.users[message.body['user']][u'name']
    
    if not user_allowed(user):
        message.reply("you don't have permission to do this ;)")
        return

    if "add_card" in args[0]:
        if garm_add_card(args[1], args[2]):
            message.reply('OK. {}ing {} as {}'.format(args[0], args[1], args[2]))
        else:
            message.reply('failed...')
    elif "add_role" in args[0]:
        if garm_add_role(args[1], args[2]):
            message.reply('OK. adding {} to {}'.format(args[1], args[2]))
        else:
            message.reply('failed...')
    elif "remove" in args[0]:
        garm_remove(message, args[1], args[2])
    elif "list_roles" in args[0]:
        roles = ""
        for key in role_lis.keys():
            roles+=", {}".format(key)
        message.reply(roles[2:])
    elif "info" in args[0]:
        roles = intern(args[1])
        message.reply('{} is {}'.format(args[1], roles[2:]))
    else:
        message.reply("Usage:\n"
        "!garm add_card <username> <cardnumber>\n"
        "!garm add_role <role> <username>\n"
        "!garm list_roles\n"
        "!garm info <username>\n"
        "!garm remove <role> <username>")
        
def garm_remove(message, role, username):
    message.reply("Not implemented :(")
    #if api.remove_role:
    #    return True
    #else:
    #    return False

def garm_add_card(username, card):
    userid = api.get_userid(username)
    for u in userid:
        if api.register_card(u['id'], card):
            return True
        else:
            return False

def garm_add_role(role, username):
    if api.register_internrole(username, role_lis.get(role)):
        return True
    else:
        return False

@respond_to(r'!sm$')
@listen_to(r'!sm$')
def sm(message):
    interns = api.get_sm()
    sm = ""
    for i in interns:
        if i['intern']['user']['username'] not in sm:
            sm+=", {}".format(i['intern']['user']['username'])
    if sm is "":
        sm = "  nothing"
    message.reply('{}: {}'.format("Skjenkemestere", sm[2:]))

@respond_to(r'!km$')
@listen_to(r'!km$')
def km(message):
    interns = api.get_km()
    km = ""
    for i in interns:
        if i['intern']['user']['username'] not in km:
            km+=", {}".format(i['intern']['user']['username'])
    if km is "":
        km = "  nothing"
    message.reply('{}: {}'.format("Kaffemestere", km[2:]))

def intern(name):
    interns = api.get_roles(name)
    roles = ""
    for i in interns:
        for k in i['roles']:
            roles+=", {}".format(k['role']['name'])
    if roles is "":
        roles = "  nothing"
    return roles

def user_allowed(user):
    roles = api.get_roles(user)
    for i in roles:
        for k in i['roles']:
            if "Internansvarlig" in k['role']['name']:
                return True
    return False
