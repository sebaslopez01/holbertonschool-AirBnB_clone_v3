#!/usr/bin/python3

"""This module defines states api actions"""


from flask import abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.get('/states')
def get_all_states():
    all_states = [state.to_dict() for state in storage.all(State).values()]

    return all_states


@app_views.get('/states/<state_id>')
def get_state(state_id: str):
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    return state.to_dict()


@app_views.delete('/states/<state_id>')
def delete_state(state_id: str):
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)

    return {}


@app_views.post('/states')
def create_state():
    try:
        data = request.get_json()
    except:
        return {'Not a JSON'}, 400
    try:
        state_name = data['name']
    except:
        return {'Missing name'}, 400

    new_state = State(name=state_name)
    storage.new(new_state)

    return new_state.to_dict(), 201


@app_views.put('/states/<state_id>')
def update_state(state_id: str):
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    try:
        data = request.get_json()
    except:
        return {'Not a JSON'}, 400
    try:
        del data['id']
        del data['created_at']
        del data['updated_at']
    except:
        pass

    state.__dict__.update(data)
    storage.save()

    return state.to_dict()
