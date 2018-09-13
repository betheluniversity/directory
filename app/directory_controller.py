import time
import requests

from flask import session, request, current_app
from flask import json as fjson


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

            # if not production, then clear our session variables on each call
            if (not session.get('admin_viewer', False)) and (dev or day_is_passed):
                for key in ['username', 'groups', 'roles', 'top_nav', 'user_email', 'name']:
                    if key in session.keys():
                        session.pop(key, None)

            if 'username' not in session.keys():
                get_user()

            if 'roles' not in session.keys():
                get_roles()

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

        init_user()
