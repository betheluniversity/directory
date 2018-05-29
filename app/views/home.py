import jinja2

from flask import Flask, render_template, request, session
from flask.ext.classy import FlaskView, route
import datetime

from app import person, query


class HomeView(FlaskView):
    def __init__(self):
        pass

    def index(self):
        return render_template('index.html', **locals())