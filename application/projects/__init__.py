from application.core import errors
from application.core.models import Bloc, Project, User
from application.core.models import prep_paginate_query, get_pagination_meta


PROJECT_CREATION_STEPS = ['title', 'description', 'link']


def create_bloc_project(bloc, user_id, title, description, weblink):
    project = Project(title=title, description=description, weblink=weblink,
        created_by_id=user_id, bloc_id=bloc.id)

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
