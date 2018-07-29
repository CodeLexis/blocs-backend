from flask import g, url_for

from application.core import errors
from application.core.models import Bloc, Event, EventInterest, User
from application.core.models import (prep_paginate_query, get_pagination_meta)
from application.gateways.facebook_client import publish_post


EVENT_CREATION_STEPS = ['title', 'description', 'time', 'venue']


def create_event(bloc, title, description, venue, datetime, created_by_id):
    event = Event(
        title=title,
        description=description,
        venue=venue,
        datetime=datetime,
        created_by_id=created_by_id,
        bloc_id=bloc.id
    )

    event.save()

    event_creation_text = (
        "Hey everyone! Y'all could join me at {venue} on {date}.\nThat's if "
        "you don't want to miss out on {title}, anyways.\n\n#Blocs #{bloc}".format(
            venue=event.venue,
            date=event.humane_date,
            title=event.title,
            bloc=event.bloc.name
        )
    )

    url = url_for('web_blueprint.render_event_details', event_id=event.id,
                  _external=True)

    user = User.get(id=created_by_id)
    # publish_post(user.access_token, event_creation_text, url=url)

    return event


def get_events_for_bloc(bloc_uid, page, per_page):
    bloc = Bloc.get(uid=bloc_uid)
    if bloc is None:
        raise errors.ResourceNotFound('Bloc not found')

    events_query = Event.query_for_active(bloc_id=bloc.id, _desc=True)

    page = prep_paginate_query(events_query, page=page, per_page=per_page)
    meta = get_pagination_meta(page)

    return page.items, meta


def declare_event_interest(event_id):
    event_interest = EventInterest(user_id=g.user.id, event_id=event_id)
    event_interest.save()

    # TODO post event interest to Facebook/Instagram
    event_interest_text = (
        "Hey everyone! Y'all could join me at {venue} on {date}.\nThat's if "
        "you don't want to miss out on {title}, anyways.\n\n#Blocs #{bloc}".format(
            venue=event_interest.event.venue,
            date=event_interest.event.humane_date,
            title=event_interest.event.title,
            bloc=event_interest.event.bloc.name
        )
    )

    url = url_for('web_blueprint.render_event_details', event_id=event_id,
                  _external=True)

    # publish_post(g.user.access_token, event_interest_text, url=url)

    return event_interest
