#!/usr/bin/python3

"""This module defines users api actions"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def get_all_users():
    if request.method == 'GET':
        list_users = list(map(lambda user: user.to_dict(), storage.all(User)))
        return jsonify(list_users)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        try:
            mail = data['email']
        except:
            abort(400, 'Missing email')
    
        try:
            pswd = data['password']
        except:
            abort(400, 'Missing password')

        new_user = User(**data)
        new_user.save()

        return new_user.to_dict(), 201

@app_views.route('/api/v1/users/<userId>', methods=['PUT'])
def update_user():
    if request.method == 'PUT':
        