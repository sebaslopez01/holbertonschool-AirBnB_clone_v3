#!/usr/bin/python3

"""This module defines states api actions"""


from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
def get_post_states():
    if request.method == 'GET':
        all_states = [state.to_dict() for state in storage.all(State).values()]

        return jsonify(all_states)
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        try:
            state_name = data['name']
        except:
            abort(400, 'Missing name')

        new_state = State(name=state_name)
        new_state.save()

        return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def get_delete_put_state(state_id: str):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return state.to_dict()
    elif request.method == 'DELETE':
        state.delete()
        del state
        return {}
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        data.pop('__class__', None)

        for key, value in data.items():
            state.__dict__[key] = value
        state.save()

        return state.to_dict()
