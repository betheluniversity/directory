from flask import Flask, session, make_response, redirect
from flask_caching import Cache

import datetime

app = Flask(__name__)
app.config.from_object('config')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
# TODO: Production cache

# Shows the year for the template
app.jinja_env.globals.update(now=datetime.datetime.now())

from app.db import db_functions as db
from directory_controller import DirectoryController

from app.views.home import HomeView

HomeView.register(app, route_base='/')


@app.before_request
def before_request():
    base = DirectoryController()
    base.before_request()


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    resp = make_response(redirect(app.config['LOGOUT_URL']))
    resp.set_cookie('MOD_AUTH_CAS_S', '', expires=0)
    resp.set_cookie('MOD_AUTH_CAS', '', expires=0)
    return resp
