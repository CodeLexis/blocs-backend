from application.core import errors
from application.core.models import Bloc, Event
from application.core.models import (prep_paginate_query, get_pagination_meta)


EVENT_CREATION_STEPS = ['title', 'description', 'time', 'venue']


def create_event(bloc_uid, title, description, venue, datetime):
    bloc = Bloc.get(uid=bloc_uid)
    if bloc is None:
        raise errors.ResourceNotFound('Bloc not found')

    event = Event(
        title=title, description=description, venue=venue, datetime=datetime)

    event.save()

    return event


def get_events_for_bloc(bloc_uid, page, per_page):
    bloc = Bloc.get(uid=bloc_uid)
    if bloc is None:
        raise errors.ResourceNotFound('Bloc not found')

    events_query = Event.query_for_active(bloc_id=bloc.id, _desc=True)

    page = prep_paginate_query(events_query, page=page, per_page=per_page)
    meta = get_pagination_meta(page)

    return page.items, meta
