from apscheduler.schedulers.blocking import BlockingScheduler

from wsgi import application
from application.core.models import User
from application.gateways.facebook_client import (
    get_user_feeds,
    get_live_videos
)


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=2)
def pull_feeds_from_users():
    with application.app_context():
        for user in User.query.order_by(User.id.desc()).all():

            if user.access_token is not None:
                users_feeds = get_user_feeds(user.access_token)

                print(users_feeds)


@sched.scheduled_job('interval', minutes=15)
def pull_course_videos_from_user():
    with application.app_context():
        for user in User.query.all():

            if user.access_token is not None:
                users_live_videos = get_live_videos(user.access_token)

                print(users_live_videos)


sched.start()
