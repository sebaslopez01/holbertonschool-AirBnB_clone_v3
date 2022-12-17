#!/usr/bin/python3

"""This module defines app instance of Flask """

import os
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_conn(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    return {'error': 'Not found'}, 404


if __name__ == '__main__':
    api_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    api_port = os.getenv('HBNB_API_PORT', 5000)

    app.run(host=api_host, port=api_port, threaded=True)
