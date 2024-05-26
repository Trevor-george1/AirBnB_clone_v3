#!/usr/bin/python3
"""creates routes and returns a Json response"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status_check():
    """creates a status route that shows status AIDEN"""
    return jsonify({"status": "OK"})
