#!/usr/bin/python3

"""This module defines app instance of Flask"""

import os
from flask import Flask
from models import storage
from views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_conn(exception):
    storage.close()


if __name__ == '__main__':
    api_host = os.getenv('HBNB_API_HOST') if os.getenv(
        'HBNB_API_HOST') else '0.0.0.0'
    api_port = int(os.getenv('HBNB_API_PORT')) if os.getenv(
        'HBNB_API_PORT') else 5000

    app.run(host=api_host, port=api_port, threaded=True)
