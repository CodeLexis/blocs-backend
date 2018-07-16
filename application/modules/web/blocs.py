from application.core.models import Bloc, User
from application.blocs import create_bloc
from . import render_template, request, web_blueprint


@web_blueprint.route('/blocs/<bloc_uid>/invite')
def render_bloc_invitation_page(bloc_id):
    bloc = Bloc.get(id=bloc_id)

    return "{} invited you to their Bloc {}".format(
        bloc.created_by.full_name, bloc.name)


@web_blueprint.route('/create-bloc', methods=['GET', 'POST'])
def render_bloc_creation_page():
    if request.method == 'GET':
        user_id = request.args.get('user_id')

        user = User.get(id=user_id)

        context = {
            'user_id': g.user.id,
            'blocs': [bloc.as_json() for bloc in user]
        }
        return render_template('blocs/create.html', **context)

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
