from application.users.helpers import get_user_access_token
from application.gateways import facebook


def create_client(external_app_uid):
    user_access_token = (
        get_user_access_token(app='Facebook', external_app_uid=external_app_uid)
    )

    graph = facebook.GraphAPI(access_token=user_access_token)

    return graph


def publish_post(external_app_uid, text, photo=None):
    graph = create_client(external_app_uid=external_app_uid)

    if photo == None:
        return graph.put_object(
            parent_object='me', connection_name='feed', message=text)

    elif photo != None:
        return graph.put_photo(image=photo, message=text)


def get_live_videos(external_app_uid):
    graph = create_client(external_app_uid=external_app_uid)

    return graph.get_object(id='me', connection_name='live_video')


def put_like(external_app_uid, object_id):
    graph = create_client(external_app_uid=external_app_uid)

    return graph.put_like(object_id=object_id)
