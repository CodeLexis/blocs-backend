from json import dumps, loads

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


def create_new_user(first_name, last_name, uid, blocs_platform):
    User(
        first_name=first_name,
        last_name=last_name,
        external_app_uid=uid,
        blocs_platform=blocs_platform
    ).save()
