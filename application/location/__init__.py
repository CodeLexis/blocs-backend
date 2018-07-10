from flask import g
import requests

from application.core.models import Location
from application.blocs import create_default_blocs_for_location


API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'


def save_new_location(coordinates):
    location_details = requests.get(
        API_URL,
        params={
            'latlng': '{},{}'.format(coordinates['lat'], coordinates['long']),
            'sensor': 'true'
        }
    ).content

    details = location_details['results']

    address = details['formatted_address']
    country = details['address_components'][-2]['long_name']
    state = details['address_components'][-3]['long_name']
    town = details['address_components'][-4]['long_name']

    location = Location(
        coordinates=coordinates,
        address=address,
        country=country,
        state=state,
        town=town,
        user_id=g.user.id
    )

    location.save()

    for locale in [{'country': country}, {'state': state}, {'town': town}]:
        locale_orm = Location()

        locale_orm.save()
        locale_orm.update(**locale)

    create_default_blocs_for_location(Location.get(state=state))

    return location
