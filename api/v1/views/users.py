#!/usr/bin/python3

"""This module defines users api"""


from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def get_all_users():
    if request.method == 'GET':
        all_user = [user.to_dict() for user in storage.all(User).values()]

        return jsonify(all_user)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        if not data.get('email', None):
            abort(400, 'Missing email')
        if not data.get('password', None):
            abort(400, 'Missing password')

        new_user = User(**data)
        new_user.save()

        return new_user.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_delete_put_users(user_id: str):
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if request.method == 'GET':
        return user.to_dict()
    elif request.method == 'DELETE':
        user.delete()
        storage.save()
        return {}
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        data.pop('email', None)

        for key, value in data.items():
            setattr(user, key, value)

        user.save()
        return user.to_dict()
