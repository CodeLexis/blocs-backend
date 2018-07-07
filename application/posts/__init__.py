from application.core import errors
from application.core.models import Bloc, Post, User


def get_bloc_posts(bloc_uid, page, per_page):
    bloc = Bloc.get(uid=bloc_uid)
    if not bloc:
        raise errors.ResourceNotFound


def add_bloc_post(user_uid, bloc_uid, title, body, attachment_uids):
    bloc = Bloc.get(uid=bloc_uid)
    if not bloc:
        raise errors.ResourceNotFound

    user = User.get(uid=user_uid)
    if not bloc:
        raise errors.ResourceNotFound

    post = Post(title=title, body=body, user_id=user.id, bloc_id=bloc.id)

    post.save()

    return post


def like_post(post_uid, user_uid):
    return


def comment_on_post(post_uid, user_uid, text):
    return
