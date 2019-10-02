import time

from flask import render_template, session, request

from app import app, sentry_sdk
from sentry_sdk import configure_scope

def error_render_template(error, code=None):
    if 'username' in session:
        username = session['username']
    else:
        username = ''

    with configure_scope() as scope:
        scope.set_tag("time", time.strftime("%c"))
        scope.set_tag("username", username)

    # Means that it's a handled error/exception
    if code is not None:
        # As of 11/16/2017, we're only logging 403s and 500 errors.
        if code == 403 or code > 499:
            sentry_sdk.capture_exception()
            app.logger.error("%s -- %s" % (username, str(error)))

    else:  # Means it's an unhandled exception
        sentry_sdk.capture_exception()
        app.logger.error('Unhandled Exception: %s', str(error))
        code = 500  # To make sure that the return statement doesn't break

    return render_template('error.html', code=code), code


@app.errorhandler(403)
def permission_denied(e):
    return error_render_template(e, 403)


@app.errorhandler(404)
def page_not_found(e):
    return error_render_template(e, 404)


@app.errorhandler(500)
def server_error(e):
    return error_render_template(e, 500)


@app.errorhandler(503)
def server_error(e):
    return error_render_template(e, 503)


@app.errorhandler(Exception)
def other_error(e):
    return error_render_template(e, 500)
