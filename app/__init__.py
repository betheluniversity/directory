import datetime
import re

from flask import Flask
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


# https://stackoverflow.com/questions/919056/case-insensitive-replace
def ireplace(string, findtxt):
    try:
        # find the start of the new string
        index_l = string.lower().index(findtxt.lower())
        # get the string with the correct capitalization
        replacetxt = string[index_l:index_l + len(findtxt)]
        # add in the span to color it properly
        replacetxt = '<span class="search-match-highlight">%s</span>' % replacetxt
    except ValueError:
        return string

    # keep capitalizations, if necessary
    return replacetxt.join(re.compile(findtxt, flags=re.I).split(string, 1))

# try just looping over it manually
# might be super slow, so just do a quick prototype

# Shows the year for the template
app.jinja_env.globals.update(now=datetime.datetime.now())
app.jinja_env.globals.update(ireplace=ireplace)

from app.views.home import View

View.register(app, route_base='/')
