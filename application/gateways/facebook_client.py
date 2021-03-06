from flask import current_app

from application.core import errors
from application.users.helpers import get_user_access_token
from . import facebook


def create_client(access_token):
    graph = facebook.GraphAPI(access_token=access_token)

    return graph


def publish_post(access_token, text, photo=None, url=None):
    graph = create_client(access_token=access_token)

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


def get_user_feed(access_token):
    graph = create_client(access_token=access_token)

    return graph.get_object(id='me', connection_name='feed', fields='feed')


def get_live_videos(access_token):
    graph = create_client(access_token=access_token)

    return graph.get_object(id='me', connection_name='live_videos',
                            fields='live_videos')


def put_like(access_token, object_id):
    graph = create_client(access_token=access_token)

    return graph.put_like(object_id=object_id)


def put_comment(access_token, object_id, message):
    graph = create_client(access_token=access_token)

    return graph.put_object(
        parent_object=object_id, connection_name='comments', message=message)
