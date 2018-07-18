from application.core.models import Bloc, Project, User
from application.projects import create_bloc_project
from . import render_template, request, web_blueprint


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
