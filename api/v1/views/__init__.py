#!/usr/bin/python3

"""This module defines the Blueprint for the views"""

from flask import Blueprint


app_views = Blueprint('simple_page', __name__, url_prefix='/api/v1')
