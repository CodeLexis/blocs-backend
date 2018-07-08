from flask import g
import requests

from application.core.models import Location


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

    Location(
        coordinates=coordinates,
        address=address,
        country=country,
        state=state,
        user_id=g.user.id
    ).save()
