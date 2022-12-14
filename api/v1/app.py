#!/usr/bin/python3

"""This module defines app instance of Flask"""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_conn(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    return {'error': 'Not found'}, 404


if __name__ == '__main__':
    api_host = os.getenv('HBNB_API_HOST') if os.getenv(
        'HBNB_API_HOST') else '0.0.0.0'
    api_port = int(os.getenv('HBNB_API_PORT')) if os.getenv(
        'HBNB_API_PORT') else 5000

    app.run(host=api_host, port=api_port, threaded=True)
