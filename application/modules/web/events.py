from flask import g, redirect, url_for
from dateutil import parser as date_parser
from flask import Response
import requests

from application.core.models import Bloc, Event, User
from application.events import create_event
from . import render_template, request, web_blueprint


@web_blueprint.route('/create-event', methods=['GET', 'POST'])
def render_event_creation_page():
    if request.method == 'GET':
        user_id = request.args.get('user_id')

        user = User.get(id=user_id)

        context = {
            'user_id': user_id,
            'blocs': [bloc.as_json() for bloc in user.blocs]
        }

        return render_template('events/create.html', **context)

    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        venue = request.form['venue']
        day_ = request.form['day']
        month_ = request.form['month']
        year_ = request.form['year']
        time_ = request.form['time']
        bloc_name = request.form['bloc_name']
        user_id = request.form['user_id']

        bloc = Bloc.get(name=bloc_name)

        datetime_ = date_parser.parse(
            '{} {} {} {}'.format(day_, month_, year_, time_)
        )

        create_event(
            bloc=bloc, title=title, description=description,
            venue=venue, datetime=datetime_, created_by_id=user_id
        )

        context = {'scope': 'event for {}'.format(bloc_name)}
        return render_template('success.html', **context)


@web_blueprint.route('/events/<int:id>')
def render_event_details(id):
    event = Event.get(id=id)

    context = event.as_json()

    return render_template('events/details.html', **context)


@web_blueprint.route('/events/<int:event_id>/thubmnail')
def render_event_thumbnail(event_id):
    event = Event.get(id=event_id)

    user_avatar = requests.get(event.created_by.clean_avatar_url).content

    thumbnail_bytes = getattr(event, 'thumbnail', None)

    response = Response(thumbnail_bytes or user_avatar)
    response.mimetype = 'image'

    return response
