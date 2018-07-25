from apscheduler.schedulers.blocking import BlockingScheduler

from wsgi import application
from application.core.models import BlocFeed, Feed, User
from application.gateways.facebook_client import (
    get_user_feed,
    get_live_videos
)


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=5)
def pull_feeds_from_users():
    with application.app_context():
        for user in User.query.order_by(User.id.desc()).all():

            if user.access_token is not None:
                users_feed = get_user_feed(
                    user.access_token)['feed']['data']

                for feed in users_feed:

                    if '#Blocs' in feed.get('message', ''):
                        if Feed.get(external_app_uid=feed['id']) is not None:
                            continue

                        feed = Feed(
                            message=feed['message'],
                            external_app_uid=feed['id'],
                            created_by_id=user.id
                        )

                        feed.save()

                        for bloc in user.blocs:
                            bloc_feed = BlocFeed(
                                bloc_id=bloc.id,
                                user_id=user.id
                            )

                            bloc_feed.save()


@sched.scheduled_job('interval', minutes=15)
def pull_course_videos_from_user():
    with application.app_context():
        for user in User.query.all():

            if user.access_token is not None:
                users_live_videos = get_live_videos(user.access_token)

                print(users_live_videos)


sched.start()
