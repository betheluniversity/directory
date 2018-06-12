from flask import Flask, render_template, request, session
from flask_classy import FlaskView, route


class HomeView(FlaskView):
    def __init__(self):
        pass

    def index(self):
        return render_template('index.html', **locals())
