#!/usr/bin/python3

"""This module defines reviews api actions"""


from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def get_all_reviews_by_place(place_id: str):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = list(map(lambda review: review.to_dict(), place.reviews))
        return jsonify(reviews)

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
        if not data.get('text', None):
            abort(400, 'Missing text')

        new_review = Review(place_id=place_id, **data)
        new_review.save()

        return new_review.to_dict(), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_put_reviews(review_id: str):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return review.to_dict()
    elif request.method == 'DELETE':
        review.delete()
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
        data.pop('place_id', None)

        for key, value in data.items():
            setattr(review, key, value)
        review.save()

        return review.to_dict()
