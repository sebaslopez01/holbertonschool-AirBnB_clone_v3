#!/usr/bin/python3

"""This module defines views"""

from api.v1.views import app_views


@app_views.route('/status')
def status():
    return {'status': 'OK'}
