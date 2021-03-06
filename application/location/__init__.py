from json import dumps, loads

from flask import g
import requests

from application.core.models import Location
from application.blocs import create_default_blocs_for_location


API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'


def get_user_state_locale(user):
    return Location.get(country=None, state=user.location.state, town=None)


def save_new_location(title, coordinates):
    location_details = loads(
        requests.get(
            API_URL,
            params={
                'latlng': '{},{}'.format(
                    coordinates['lat'], coordinates['long']),
                'sensor': 'true'
            }
        ).content
    )

    print('LOCATION DETAILS: %s'%location_details)

    location = Location(
        title=title,
        coordinates=dumps(coordinates),
        user_id=g.user.id
    )

    location.save()

    try:
        details = location_details['results'][0]
        address = details['formatted_address']
        country = details['address_components'][-2]['long_name']
        state = details['address_components'][-3]['long_name']
        town = details['address_components'][-4]['long_name']

        location.update(
            address=address,
            country=country,
            state=state,
            town=town
        )

    except IndexError:
        return

    for locale in [
        {'country': country, 'state': None, 'town': None},
        {'country': None, 'state': state, 'town': None},
        {'country': None, 'state': None, 'town': town}
    ]:

        existing_locale_orm = Location.get(**locale)
        if existing_locale_orm is not None:
            return

        locale_orm = Location()

        locale_orm.save()

        locale_orm.update(**locale)

    create_default_blocs_for_location(Location.get(state=state))

    return location
