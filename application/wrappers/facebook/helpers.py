import os
import requests

from pymessenger import Bot

from application.core.constants import FACEBOOK_PAGE_ID


ACCESS_TOKEN = os.environ['FACEBOOK_PAGE_ACCESS_TOKEN']
# ACCESS_TOKEN = 'EAAOlZBoXtZAmABACxIo85QJxVgygCUTpI0YtUWbM8HOTmafLnlyNSMgDwe36B9u6PGzyvotY68iIzgQOkLrDs5YcuyI9sBCaU0wUvGajtCRiIaR4OrL0ZBug1KQPZBoiJVPccoMd29pDYruJ1Q7LFCCyVLSO8S28IBZCQUiWYGAZDZD'

# VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
VERIFY_TOKEN = 'some_verify_token'

MESSENGER_PROFILE_URL = (
    'https://graph.facebook.com/v2.6/me/messenger_profile?access_token=%s' %
    ACCESS_TOKEN)
USER_PROFILE_URL = (
    "https://graph.facebook.com/v2.6/{user_id}?fields=first_name,last_name,"
    "profile_pic&access_token=%s" % ACCESS_TOKEN)


bot = Bot(ACCESS_TOKEN)


def verify_fb_token(token_sent):
    return token_sent == VERIFY_TOKEN


def send_message(recipient_id, response):
    response_type, response_content = response
    print('ABOUT TO SEND: %s' % response_type)

    func = type_funcs[response_type]

    print("FUNC: %s" % func)

    print(func(recipient_id, response_content))

    print("DONE: %s" % func)

    return "SUCCESS"
    # logging.info('Sending %s' % response)
    #
    # bot.send_text_message(recipient_id, response)
    #
    # logging.info('Sent %s' % response)
    #
    # return "success"


def send_quick_reply(recipient_id, text_quick_reply_options):
    text, quick_reply_options = text_quick_reply_options

    message = {
        "text": text,
        "quick_replies": quick_reply_options
    }

    print('SEND_QUICK_REPLY', message)

    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": message
    }

    return bot.send_raw(payload)


def set_typing_on():
#     curl - X
#     POST - H
#     "Content-Type: application/json" - d
#     '{
#     "recipient": {
#         "id": "<PSID>"
#     },
#     "sender_action": "typing_on"
#
# }'

    return requests.post(
        "https://graph.facebook.com/v2.6/me/messages?access_token=%s".format(
            ACCESS_TOKEN),
        headers={'content-type': 'application/json'},
        data={
            'recipient': {'id': FACEBOOK_PAGE_ID},
            'sender_action': 'typing_on'
        }
    ).content


def get_user_profile(user_id):
    return eval(requests.get(USER_PROFILE_URL.format(user_id=user_id)).content)


type_funcs = {
    'text': getattr(bot, 'send_text_message'),
    'quick_reply': send_quick_reply,
    'generic': getattr(bot, 'send_generic_message'),
    'buttons': getattr(bot, 'send_button_message')
}
