import requests

from application.core.constants import LANDING_MESSAGE


# ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN = 'EAAGTzHZCz6UQBAD34ace0tANWeArDA5Qg0PvZCvHJNsZAJN4fV7ntjX9tQMSfBhAm3AuFnisC53C4uoffITnVlUbpZCa2Eck1ga2dFTfHfBVuqx89J89vzaKB32i5ycpDgIRlBRNg4CNWvhwoubn2hvR3rVoLZBFex2CLfFk9DwZDZD'

# VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
VERIFY_TOKEN = 'some_verify_token'

MESSENGER_PROFILE_URL = (
    'https://graph.facebook.com/v2.6/me/messenger_profile?access_token=%s' %
    ACCESS_TOKEN)

['Schools', 'Jobs', 'Events', 'News', 'Posts', 'Projects']

side_menu_payload = {
    "persistent_menu": [
        {
            "locale": "default",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "title": "Events",
                    "type": "postback",
                    "payload": "DISPLAY_ALL_EVENTS"
                },
                {
                    "title": "Jobs",
                    "type": "postback",
                    "payload": "DISPLAY_ALL_JOBS"
                },
                {
                    "title": "More",
                    "type": "nested",
                    "call_to_actions": [
                        {
                            "title": "Courses",
                            "type": "postback",
                            "payload": "DISPLAY_ALL_COURSES"
                        },
                        {
                            "title": "Projects",
                            "type": "postback",
                            "payload": "DISPLAY_ALL_PROJECTS"
                        },
                        {
                            "title": "More",
                            "type": "nested",
                            "call_to_actions": [
                                {
                                    "title": "Feeds",
                                    "type": "postback",
                                    "payload": "DISPLAY_ALL_FEEDS"
                                },
                                {
                                    "title": "News",
                                    "type": "postback",
                                    "payload": "DISPLAY_ALL_NEWS"
                                }
                            ]
                        }
                    ]
                },
            ]
        }
    ]
}
def add_side_menu():

    return requests.post(MESSENGER_PROFILE_URL, json=side_menu_payload).content


def add_get_started():
    payload = {
        "get_started": {
            "payload": "GET_STARTED_PAYLOAD"
        }
    }

    return requests.post(MESSENGER_PROFILE_URL, json=payload).content


def add_greeting():
    payload = {
        "greeting": [
            {
                "locale": "default",
                "text": LANDING_MESSAGE
            }, {
                "locale": "en_US",
                "text": LANDING_MESSAGE
            }
        ]
    }

    return requests.post(MESSENGER_PROFILE_URL, json=payload).content


if __name__ == '__main__':
    print(add_get_started())
    # print(add_side_menu())
    # print(add_greeting())
