import datetime

from flask import Flask, session, make_response, redirect
from flask_caching import Cache

app = Flask(__name__)
app.config.from_object('config')

if app.config['SENTRY_URL']:
    from raven import Client
    client = Client(app.config['SENTRY_URL'])

if app.config['ENVIRON'] != 'prod':
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})
else:
    cache = Cache(app, config={
        'CACHE_TYPE': 'redis',
        # The default value for CACHE_REDIS_HOST is localhost/127.0.0.1, but if we ever wanted to make it accessible by
        # another server, say h20, we could change this value to be the IP of h12 itself
        # 'CACHE_REDIS_HOST': 'localhost',

        # Likewise, the default port number is 6379, but we can set it here if we want to make Redis publicly accessible
        # 'CACHE_REDIS_PORT': 6379,

        # Finally, if we make it accessible, this is how we would set it to be password-protected
        # 'CACHE_REDIS_PASSWORD': None,

        # This key is needed in case we want to call cache.clear(); Redis' backend implementation in Flask-Cache is
        # finicky and should have a prefix so that .clear() knows which values to remove.
        'CACHE_KEY_PREFIX': 'directory-'
    })

from raven.contrib.flask import Sentry
sentry = Sentry(app, dsn=app.config['SENTRY_URL'])

from app.views import error

# Shows the year for the template
app.jinja_env.globals.update(now=datetime.datetime.now())

from app.db import db_functions as db
from app.directory_controller import  DirectoryController
from app.views.home import View

View.register(app, route_base='/')


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
