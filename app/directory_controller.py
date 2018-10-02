import time
import requests

from flask import session, request, current_app
from flask import json as fjson

from app.db.db_functions import portal_profile


class DirectoryController(object):
    def __init__(self):
        pass

    def before_request(self):
        def init_user():
            dev = current_app.config['ENVIRON'] != 'prod'

            # reset session if it has been more than 24 hours
            if 'session_time' in session.keys():
                seconds_in_day = 60 * 60 * 24
                day_is_passed = time.time() - session['session_time'] >= seconds_in_day
            else:
                day_is_passed = True
                session['session_time'] = time.time()

            if 'username' not in session.keys():
                get_user()

            if 'roles' not in session.keys():
                get_roles()

            if 'profile' not in session.keys():
                session['profile'] = portal_profile(session['username'])

            if 'all_id' not in session.keys():
                show_all_id()

        def get_user():
            if current_app.config['ENVIRON'] == 'prod':
                username = request.environ.get('REMOTE_USER')
            else:
                username = current_app.config['TEST_USER']

            session['username'] = username

        def get_roles(username=None):
            if not username:
                username = session['username']
            url = current_app.config['API_URL'] + "/username/%s/roles" % username
            r = requests.get(url, auth=(current_app.config['API_USERNAME'], current_app.config['API_PASSWORD']))
            roles = fjson.loads(r.content)
            ret = []
            for key in roles.keys():
                ret.append(roles[key]['userRole'])

            session['roles'] = ret

            if username == 'bam95899':
                session['roles'] = 'admin'

            return ret

        def show_all_id():
            session['all_id'] = 'false'
            for role in session['roles']:
                if role == 'staff' or role == 'faculty':
                    session['all_id'] = 'true'

        init_user()
