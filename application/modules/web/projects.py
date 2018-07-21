from flask import Response
import requests

from application.core.models import (
    Bloc, Project, ProjectLike, ProjectView, User)
from application.core.utils.contexts import get_request_pagination_params
from application.core.models import prep_paginate_query
from application.projects import create_bloc_project
from . import redirect, render_template, request, web_blueprint


@web_blueprint.route('/create-project', methods=['GET', 'POST'])
def render_project_creation_page():
    if request.method == 'GET':
        user_id = request.args.get('user_id')

        user = User.get(id=user_id)

        context = {
            'user_id': user_id,
            'blocs': [bloc.as_json() for bloc in user.blocs]
        }

        return render_template('projects/create.html', **context)

    elif request.method == 'POST':
        user_id = request.form['user_id']
        title = request.form['title']
        description = request.form['description']
        weblink = request.form['weblink']
        bloc_name = request.form['bloc_name']

        bloc = Bloc.get(name=bloc_name)

        create_bloc_project(
            bloc=bloc, user_id=user_id, title=title, description=description,
            weblink=weblink)

        context = {'scope': 'Project'}

        return render_template('success.html', **context)


@web_blueprint.route('/projects/<project_id>', methods=['GET'])
def render_project_details_page(project_id):
    user_id = request.args.get('user_id')

    project = Project.get(id=project_id)

    project_view = ProjectView(project_id=project_id, user_id=user_id)
    project_view.save()

    return redirect(project.weblink)


@web_blueprint.route('/projects/<project_id>/likes', methods=['GET'])
def render_all_project_likes(project_id):

    project_likes = ProjectLike.query.filter_by(project_id=project_id)

    project_likes = prep_paginate_query(
        project_likes, **get_request_pagination_params())

    return render_template(
        'projects/likes.html',
        project_likes=[like.as_json() for like in project_likes]
    )


@web_blueprint.route('/projects/<int:project_id>/thubmnail')
def render_project_thumbnail(project_id):
    project = Project.get(id=project_id)

    user_avatar = requests.get(project.created_by.avatar_url).content

    thumbnail_bytes = getattr(project, 'thumbnail', None)

    response = Response(thumbnail_bytes or user_avatar)
    response.mimetype = 'image'

    return response
