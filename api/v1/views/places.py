#!/usr/bin/python3

"""This module defines places api actions"""


from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def get_all_places_by_city(city_id: str):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        places = list(map(lambda place: place.to_dict(), city.places))
        return jsonify(places)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        try:
            user_id = data['user_id']
        except:
            abort(400, 'Missing user_id')
        if storage.get(User, user_id) is None:
            abort(404)
        if not data.get('name', None):
            abort(400, 'Missing name')

        new_place = Place(city_id=city_id, **data)
        new_place.save()

        return new_place.to_dict(), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_put_places(place_id: str):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return place.to_dict()
    elif request.method == 'DELETE':
        place.delete()
        storage.save()
        return {}
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        data.pop('user_id', None)
        data.pop('city_id', None)

        for key, value in data.items():
            setattr(place, key, value)
        place.save()

        return place.to_dict()
