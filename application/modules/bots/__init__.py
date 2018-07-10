import json
import logging
import time
from urllib import parse as urlparse

from flask import Blueprint
from flask import g, make_response, redirect, request
from flask.views import MethodView
import requests

from application.conversations.helpers import (
    get_response, save_message, to_send_response)
from application.core.models.helpers import (
    orm_get_blocs_platform_by_name, orm_get_user_by_platform_uid)
from application.core.utils.helpers import get_typing_duration
from application.wrappers.facebook.helpers import (verify_fb_token,
    send_message, set_typing_on)


bots_blueprint = Blueprint('bots', __name__, url_prefix='/bots')


class FacebookBotHandler(MethodView):
    @property
    def platform(self):
        return orm_get_blocs_platform_by_name('Facebook Bot')

    def get(self):
        token_sent = request.args.get("hub.verify_token")
        hub_challenge = request.args.get("hub.challenge")

        if not verify_fb_token(token_sent):
            raise ValueError('Wrong FB token sent')

        return hub_challenge

    def post(self):
        output = request.get_json()

        for event in output['entry']:
            messaging = event['messaging']

            for message in messaging:
                response = None

                recipient_id = message['sender']['id']

                g.user = (
                    orm_get_user_by_platform_uid(
                        self.platform.id, recipient_id)
                )

                if g.user is None:
                    response = [('text', "Hi! Welcome to Blocs B)")]

                if message.get('message'):
                    text = message['message'].get('text')
                    attachments = message['message'].get('attachments')
                    sticker_id = message['message'].get('sticker_id')
                    quick_reply = message['message'].get('quick_reply')

                    try:
                        nlp = message['message']['nlp']['entities']
                    except:
                        nlp = None

                    if quick_reply:
                        response = get_response(
                            recipient_id, self.platform,
                            payload=quick_reply['payload'],
                            text=text
                        )

                    elif text:
                        response = get_response(
                            recipient_id, self.platform, text=text, nlp=nlp,
                            sticker_id=sticker_id
                        )

                    elif attachments:
                        response = get_response(
                            recipient_id, self.platform,
                            attachments=attachments)

                elif message.get('postback'):
                    payload = message['postback']['payload']
                    text = message['postback']['title']

                    response = get_response(
                        recipient_id, self.platform, payload=payload, text=text,
                        is_postback=True)

                if response is not None:
                    if to_send_response(response):
                        for reply in response:
                            set_typing_on(recipient_id)
                            time.sleep(get_typing_duration(*reply))
                            send_message(recipient_id, reply)

                    save_message(response)

        return "Message Processed"


mappings = [
    ('/facebook', FacebookBotHandler, 'facebook'),
]


for url in mappings:
    path, view, name = url

    bots_blueprint.add_url_rule(path, view_func=view.as_view(name))
