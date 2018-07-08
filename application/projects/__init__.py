from application.core import errors
from application.core.models import Bloc, Project, User
from application.core.models import prep_paginate_query, get_pagination_meta


PROJECT_CREATION_STEPS = ['title', 'description', 'link']


def create_bloc_project(user_uid, bloc_uid, title, description, url):
    bloc = Bloc.get(uid=bloc_uid)
    if bloc is None:
        raise errors.ResourceNotFound

    user = User.get(uid=user_uid)
    if user is None:
        raise errors.ResourceNotFound

    project = Project(title=title, description=description, url=url,
                      user_id=user.id, bloc_id=bloc.id)

    project.save()

    return project


def get_bloc_projects(bloc_uid, page, per_page):
    bloc = Bloc.get(uid=bloc_uid)
    if bloc is None:
        raise errors.ResourceNotFound

    projects = Project.query_for_active(bloc_id=bloc.id, _desc=True)

    page = prep_paginate_query(projects, page=page, per_page=per_page)
    meta = get_pagination_meta(page)

    return page.items, meta


def like_bloc_project(project_id):
    return
