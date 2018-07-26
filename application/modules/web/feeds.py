from flask import g, redirect, url_for
from dateutil import parser as date_parser
from flask import Response
import requests

from application.core.models import FeedLike
from application.core.models import prep_paginate_query, get_pagination_meta
from application.core.utils.request_response_helpers import (
    get_request_pagination_params)
from application.events import create_event, declare_event_interest
from . import render_template, request, web_blueprint


@web_blueprint.route('/feeds/<int:feed_id>/likes', methods=['GET', 'POST'])
def render_all_feeds_likes(feed_id):
    feed_likes = FeedLike.query_for_active(feed_id=feed_id)

    users = []

    for feed_like in feed_likes:
        users.append(feed_like.user.as_json())

    return render_template('users_list.html', users=users)
