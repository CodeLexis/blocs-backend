from application.core.models import Feed, FeedLike, FeedComment
from . import render_template, web_blueprint


@web_blueprint.route('/feeds/<int:feed_id>/likes', methods=['GET', 'POST'])
def render_all_feeds_likes(feed_id):
    feed_likes = FeedLike.query_for_active(feed_id=feed_id)

    users = []

    for feed_like in feed_likes:
        users.append(feed_like.user.as_json())

    print('USERS: %s' % users)

    return render_template('users_list.html', title='People who also liked it',
                           users=users)


@web_blueprint.route('/feeds/<int:feed_id>/comments')
def render_feed_comments(feed_id):
    feed = Feed.get(id=feed_id)
    feed_comments = FeedComment.query_for_active(feed_id=feed_id)

    comments = []

    for feed_comment in feed_comments:
        comments.append(feed_comment.comment.as_json())

    comments.reverse()

    return render_template(
        'comment_list.html', title='Comments', comments=comments,
        feed=feed.as_json()
    )
