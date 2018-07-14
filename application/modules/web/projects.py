from application.core.models import Project
from application.blocs import create_bloc
from . import render_template, request, web_blueprint


@web_blueprint.route('/create-project')
def render_project_creation_page():
    if request.method == 'GET':
        return render_template('projects/create.html')

    elif request.method == 'POST':
        name = request.form['name']
        is_private = bool(request.form['is_private'])
        color = request.form['color']

        bloc = create_bloc(name=name, is_private=is_private, color=color)

        context = {'scope': 'Bloc'}
        if is_private:
            context['subtext'] = 'Invite code: <b>{}</b>'.format(
                bloc.invite_code)

        return render_template('success.html', **context)



@web_blueprint.route('/create-bloc', methods=['GET', 'POST'])
def render_bloc_creation_page():
    if request.method == 'GET':
        return render_template('blocs/create.html')

    elif request.method == 'POST':
        name = request.form['name']
        is_private = bool(request.form['is_private'])
        color = request.form['color']

        bloc = create_bloc(name=name, is_private=is_private, color=color)

        context = {'scope': 'Bloc'}
        if is_private:
            context['subtext'] = 'Invite code: <b>{}</b>'.format(
                bloc.invite_code)

        return render_template('success.html', **context)
