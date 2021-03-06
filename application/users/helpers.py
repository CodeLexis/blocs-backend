from json import dumps, loads

from flask import g

from application.wrappers.facebook.helpers import PAGE_ACCESS_TOKEN
from application.core.models import SoftwareBranch, User, UserSoftwareBranch


def add_course_to_offered(course_id):
    user = User.get(id=g.user.id)

    courses_offered = loads(user.courses_offered)
    courses_offered.append(course_id)

    user.update(courses_offered=dumps(courses_offered))


def add_user_software_branch(branch_id):
    UserSoftwareBranch(
        user_id=g.user.id,
        software_branch_id=branch_id
    ).save()


def create_new_user(first_name, last_name, uid, blocs_platform_id, avatar_url):
    user = User(
        first_name=first_name,
        last_name=last_name,
        external_app_uid=uid,
        blocs_platform_id=blocs_platform_id,
        avatar_url=avatar_url
    )

    user.save()

    g.user = user

    return user


def get_user_access_token(app, external_app_uid):
    user = User.get(external_app_uid=external_app_uid)

    return user.access_token
