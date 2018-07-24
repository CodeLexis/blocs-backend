from flask import redirect, request, url_for
from flask.views import MethodView

from . import web_blueprint
from application.wrappers.facebook.helpers import (
    FACEBOOK_APP_ID, PAGE_ACCESS_TOKEN, REQUIRED_PERMISSIONS)
from application.gateways.facebook_client import facebook


class FacebookOauthLogin(MethodView):
    def get(self):
        graph = facebook.GraphAPI(PAGE_ACCESS_TOKEN)

        redirect_url = url_for(
            'web_blueprint.oauth_facebook', _external=True)

        fb_login_url = graph.get_auth_url(
            FACEBOOK_APP_ID, redirect_url, REQUIRED_PERMISSIONS)

        return redirect(fb_login_url)

    def post(self):
        return


mappings = [
    ('/oauth/facebook', FacebookOauthLogin, 'oauth_facebook'),
]


for url in mappings:
    path, view, name = url

    web_blueprint.add_url_rule(path, view_func=view.as_view(name))
