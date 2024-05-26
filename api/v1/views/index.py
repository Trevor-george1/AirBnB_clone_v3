#!/usr/bin/python3
"""creates routes"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status_check():
    """creates a status route that shows status AIDEN"""
    return jsonify({"status": "OK"})
