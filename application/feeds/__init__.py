from flask import g, url_for

from application.core.models import Feed, FeedComment, FeedLike
from application.wrappers.facebook.helpers import send_message


def like_feed(feed_external_app_uid, feed_id):
    FeedLike(feed_id=feed_id, user_id=g.user.id).save()

    # put_like(g.user.access_token, feed_external_app_uid)


def comment_on_feed(feed, message):
    FeedComment(feed_id=feed.id, user_id=g.user.id, message=message).save()

    send_message(
        feed.created_by.external_app_uid,
        ('text',
         'Hi {}, {} {} just replied to your status! View all {} replies: '
         '{}'.format(
                feed.created_by.first_name,
                g.user.first_name, g.user.last_name,
                feed.replies_count,
                url_for('web_blueprint.render_feed_comments', feed_id=feed.id,
                        _external=True)
            )
        )
    )
    # put_comment(g.user.access_token, feed_external_app_uid, message)
