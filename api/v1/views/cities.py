#!/usr/bin/python3

"""This module defines cities api actions"""


from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def get_all_cities_by_state(state_id: str):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        cities = list(map(lambda city: city.to_dict(), state.cities))
        return jsonify(cities)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        try:
            city_name = data['name']
        except:
            abort(400, 'Missing name')

        new_city = City(state_id=state_id, name=city_name)
        new_city.save()

        return new_city.to_dict(), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_put_cities(city_id: str):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return city.to_dict()
    elif request.method == 'DELETE':
        city.delete()
        storage.save()
        return {}
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        data.pop('state_id', None)

        for key, value in data.items():
            setattr(city, key, value)
        city.save()

        return city.to_dict()
