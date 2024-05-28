#!/usr/bin/python3
"""Place object RESTFul API actions"""

from flask import jsonify, make_response, request, abort
from models import storage
from models.place import Place
from api.v1.views import app_views
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)  # noqa
def get_places_by_city(city_id):
    """get place by city"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)  # noqa
def get_place(place_id):
    """get place by place_id"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)  # noqa
def delete_place(place_id):
    """delete a place by place id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)  # noqa
def create_place(city_id):
    """creates a place object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user = storage.get("User", data["user_id"])
    if not user:
        abort(400)
    data['city_id'] = city_id
    place = Place(**data)
    # setattr(place, 'city_id', city_id)
    # storage.new(place)
    # storage.save()
    place.save()
    return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)  # noqa
def update_place(place_id):
    """update the place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
