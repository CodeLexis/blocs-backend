from flask import redirect, render_template, request, url_for, session
from flask.views import MethodView
from json import loads
import requests

from . import web_blueprint
from application.core.models import User
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
            user_id = request.args.get('user_id')

            graph = facebook.GraphAPI(PAGE_ACCESS_TOKEN)

            fb_login_url = graph.get_auth_url(
                FACEBOOK_APP_ID, redirect_url, REQUIRED_PERMISSIONS,
                state=user_id
            )

            return redirect(fb_login_url)

        else:
            user_id = request.args.get('state')

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

            # print(response_data)

            access_token = response_data['access_token']

            user = User.get(id=user_id)
            user.update(access_token=access_token)

            destination = session.pop('destination')
            if destination:
                return redirect(destination)

            return redirect(
                url_for('web_blueprint.render_success_page'))


class LoginRequest(MethodView):
    def get(self):
        app = request.args.get('app')
        motive = request.args.get('motive')
        destination = request.args.get('destination')
        login_url = request.args.get('login_url')

        session['destination'] = destination

        return render_template(
            'oauth/login_request.html',
            app=app, motive=motive,
            login_url=login_url
        )


mappings = [
    ('/oauth/facebook', FacebookOauthLogin, 'oauth_facebook'),
    ('/oauth/login-request', LoginRequest, 'oauth_login_request')
]


for url in mappings:
    path, view, name = url

    web_blueprint.add_url_rule(path, view_func=view.as_view(name))
