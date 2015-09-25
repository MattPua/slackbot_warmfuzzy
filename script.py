#!/usr/bin/python
'''
====================================
IMPORTS
====================================
'''
import json
import requests
import traceback
import sys


from settings import *
'''
====================================
CONSTANTS
====================================
'''

BASE_URL             = 'https://slack.com/api/'
BASE_PARAMS          = {
"token": TOKEN,
}

CMD_NEW_MESSAGE      = 'chat.postMessage'
CMD_GET_USERS        = 'users.list'


'''
====================================
FUNCTIONS
====================================
'''




'''
Try and find a specific user by name
'''
def get_user(name):
    get_params = dict(BASE_PARAMS.items())

    response = requests.post(BASE_URL+CMD_GET_USERS,params=get_params)

    json = response.json()
    members = json['members']
    is_correct = False
    lower_name = name.lower()
    for member in members:
        if (member['deleted'] == True):
            continue
        if (member['profile']['real_name'].lower().find(lower_name) >= 0):
            user_input = raw_input("Are you looking for " + member['profile']['real_name'] + " [Y/N]?")
            is_correct = False if user_input=='n' else True
        if is_correct:
            print 'found member ' + member['real_name']
            return member
    print 'Could not find a matching member'
    return None

"""
Sends the new message to Slack via Direct Message
"""
def send_message(user_to_send,message,current_user=None):

    new_message_params = {
        "channel":user_to_send['id'],
        "username":"WarmFuzzies",
        "link_names":"1",
        "text":message,
        "icon_emoji": ":dog:",
        "as_user":"false"
    }
    new_message_params = dict(new_message_params.items() + BASE_PARAMS.items())

    response = requests.post(BASE_URL+CMD_NEW_MESSAGE,params=new_message_params)
    print "Successfully sent message to " + user_to_send['profile']['real_name']



'''
====================================
MAIN
====================================
'''
def main():
    try:
        user_name = ''
        message = ''
        is_anonymous = False
        is_anon = ''
        current_user = ''
        while (not user_name):
            user_name = raw_input("Enter the name you are looking for\n>")

        user_to_send = get_user(user_name)

        if (user_to_send is None):
            print "Could not find the user you are looking for. Please try again.\n"
            sys.exit(0)


        while (not message):
            message = raw_input("Please enter the message to be sent.\n>")

        while (not is_anon):
            is_anon = raw_input("Do you want this message to be anonymous? [Y/N] \n>")
            is_anon = '' if is_anon!='n' and is_anon!='y' else is_anon

        is_anonymous = True if is_anon=='y' else False


        if is_anonymous:

            print "Summary:\nYou want to send a message to %s with message: %s and it should be anonymous: %s" % (user_to_send['real_name'], message,is_anonymous)
            current_user = None
        else:
            while (not current_user):
                current_user = raw_input("You chose not to be anonymous. Please enter your name.\n>")

            current_user = get_user(current_user)

            if (current_user is None):
                print "Sorry, we could not find you. Please try again.\n"
                sys.exit(0)

            print "Summary:\nYou want to send a message to %s with message: %s and it should be from: %s" % (user_to_send['real_name'], message,current_user['real_name'])

        is_correct = ''
        while (not is_correct):
            is_correct = raw_input("Please verify this is correct. [Y/N]?\n>")

            is_correct = '' if is_correct != 'y' and is_correct!='n' else is_correct

            if (is_correct == 'n'):
                print "You indicated this is not correct. Please try again.\n"
                sys.exit(0)

        send_message(user_to_send,message,current_user)

    except Exception as e:
        traceback.print_exc()
        print "ERROR: " 
        print e


main()



