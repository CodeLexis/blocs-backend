from flask import g

from application.core.models import FeedComment, FeedLike
from application.gateways.facebook_client import put_comment, put_like


def like_feed(feed_external_app_uid, feed_id):
    FeedLike(feed_id=feed_id, user_id=g.user.id).save()

    put_like(g.user.access_token, feed_external_app_uid)


def reply_feed(feed_external_app_uid, feed_id, message):
    FeedComment(feed_id=feed_id, user_id=g.user.id).save()

    put_comment(g.user.access_token, feed_external_app_uid, message)
