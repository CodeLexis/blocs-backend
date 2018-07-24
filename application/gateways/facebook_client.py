from flask import current_app

from application.core import errors
from application.users.helpers import get_user_access_token
from . import facebook


def create_client(external_app_uid=None, access_token=None):
    if not (external_app_uid or access_token):
        raise ValueError

    user_access_token = None

    if external_app_uid:
        user_access_token = (
            get_user_access_token(
                app='Facebook', external_app_uid=external_app_uid)
        )

        print('EXATAPP %s' % external_app_uid)

        if user_access_token is None:
            return None

    graph = facebook.GraphAPI(access_token=access_token or user_access_token)

    return graph


def publish_post(external_app_uid, text, photo=None, url=None):
    graph = create_client(external_app_uid=external_app_uid)

    print('GRAPH CLIENT IS %s' % graph)

    if graph is None:
        return

    post_type = photo or url

    if post_type is None:
        return graph.put_object(
            parent_object='me', connection_name='feed', message=text)

    elif post_type == photo:
        return graph.put_photo(image=photo, message=text)

    elif post_type == url:
        return graph.put_object(parent_object='me', connection_name='feed',
                                message=text, url=url)


def get_live_videos(external_app_uid):
    graph = create_client(external_app_uid=external_app_uid)

    return graph.get_object(id='me', connection_name='live_videos')


def put_like(external_app_uid, object_id):
    graph = create_client(external_app_uid=external_app_uid)

    return graph.put_like(object_id=object_id)
