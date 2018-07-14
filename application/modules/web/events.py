from application.core.models import Bloc, Event
from application.events import create_event
from . import render_template, request, web_blueprint


@web_blueprint.route('/create-event', methods=['GET', 'POST'])
def render_event_creation_page():
    if request.method == 'GET':
        return render_template('events/create.html')

    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        venue = request.form['venue']
        date_and_time = request.form['date_and_time']
        bloc_name = request.form['bloc_name']

        bloc = Bloc.get(name=bloc_name)

        create_event(
            bloc_uid=bloc.uid, title=title, description=description,
            venue=venue, datetime=date_and_time
        )

        context = {'scope': 'event for {}'.format(bloc_name)}
        return render_template('success.html', **context)


@web_blueprint.route('/events/<int:id>')
def render_event_details(id):
    event = Event.get(id=id)

    context = event.as_json()

    return render_template('events/details.html', **context)


@web_blueprint.route('/events/<int:id>/thumbnail')
def render_event_thumbnail(id):
    # TODO implement event thumbnail get
    event = Event.get(id=id)

    return