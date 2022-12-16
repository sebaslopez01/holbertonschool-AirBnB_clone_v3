#!/usr/bin/python3

"""This module defines amenities api actions"""


from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
def get_all_amenities():
    if request.method == 'GET':
        amenities = [amenity.to_dict()
                     for amenity in storage.all(Amenity).values()]
        return jsonify(amenities)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        try:
            amenity_name = data['name']
        except:
            abort(400, 'Missing name')

        new_amenity = Amenity(name=amenity_name)
        new_amenity.save()

        return new_amenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_put_amenities(amenity_id: str):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return amenity.to_dict()
    elif request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return {}
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)

        for key, value in data.items():
            setattr(amenity, key, value)
        amenity.save()

        return amenity.to_dict()
