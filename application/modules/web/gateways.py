from flask import redirect, request, url_for
from flask.views import MethodView
from json import loads
import requests

from . import web_blueprint
from application.wrappers.facebook.helpers import (
    FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, PAGE_ACCESS_TOKEN,
    REQUIRED_PERMISSIONS)
from application.gateways.facebook_client import facebook, create_client


class FacebookOauthLogin(MethodView):
    def get(self):
        code = request.args.get('code')

        redirect_url = url_for(
            'web_blueprint.oauth_facebook', _external=True)

        if code is None:
            graph = facebook.GraphAPI(PAGE_ACCESS_TOKEN)

            fb_login_url = graph.get_auth_url(
                FACEBOOK_APP_ID, redirect_url, REQUIRED_PERMISSIONS,
            )

            return redirect(fb_login_url)

        else:
            params = {
                'client_id': FACEBOOK_APP_ID,
                'redirect_uri': redirect_url,
                'client_secret': FACEBOOK_APP_SECRET,
                'code': code
            }

            response = requests.get(
                'https://graph.facebook.com/v3.0/oauth/access_token',
                params=params
            ).content.decode()

            # {"access_token":
            #      "EAAGTzHZCz6UQBAL4ziJ7zcVbSgsuUeqi5lkgl6cWcCpMBpXD3aScni7O1Wuu"
            #      "7ux5nZC7XCJYox9guGZCijBCZAjsZBHZCNibwZAieaYda7XctcPZBgR9WHFiv"
            #      "EBgcqpwLZAJvtJ3EWCup0nIb0nUbiMBuB5bQqwKuk7KSaViWzVvW1AZDZD",
            #  "token_type": "bearer", "expires_in": 5178778}

            response_data = loads(response)

            print(response_data)

            access_token = response_data['access_token']

            graph = create_client(access_token=access_token)
            print(graph.get_object('me', 'id'))


mappings = [
    ('/oauth/facebook', FacebookOauthLogin, 'oauth_facebook'),
]


for url in mappings:
    path, view, name = url

    web_blueprint.add_url_rule(path, view_func=view.as_view(name))
