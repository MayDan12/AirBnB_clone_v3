#!/usr/bin/python3
"""Imports the Blueprint object from the flask module."""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
<<<<<<< HEAD
=======

>>>>>>> 8055086e65a629a5eba78b8a5bec5cfe8b61594d
