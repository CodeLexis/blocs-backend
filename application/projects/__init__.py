from flask import g, url_for

from application.core import errors
from application.core.models import Bloc, Project, ProjectLike, User
from application.core.models import prep_paginate_query, get_pagination_meta
from application.gateways.facebook_client import publish_post


PROJECT_CREATION_STEPS = ['title', 'description', 'link']


def create_bloc_project(bloc, user_id, title, description, weblink):
    project = Project(title=title, description=description, weblink=weblink,
        created_by_id=user_id, bloc_id=bloc.id)

    project.save()

    event_creation_text = (
        "Hey everyone! Y'all should checkout {title}!\n\n#Blocs #{bloc}".format(
            title=project.title,
            bloc=project.bloc.name
        )
    )

    return project

    url = url_for('web_blueprint.render_project_details',
                  project_id=project.id,
                  _external=True)

    publish_post(g.user.external_app_uid, event_creation_text, url)

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
    ProjectLike(project_id=project_id, created_by_id=g.user.id).save()
