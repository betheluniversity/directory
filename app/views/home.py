import ldap
import re
import requests
import time

from flask import render_template, request, session, abort, make_response, redirect
from flask import json as fjson
from flask_classy import FlaskView, route

from app import app, sentry
from app.db.db_functions import departments, portal_profile
from app.directory_controller import DirectoryController


class View(FlaskView):
    def __init__(self):
        self.base = DirectoryController()

    def before_request(self, name, **kwargs):
        def init_user():
            if 'session_time' in session.keys():
                seconds_in_12_hours = 60 * 60 * 12  # equates to 12 hours
                reset_session = time.time() - session['session_time'] >= seconds_in_12_hours
            else:
                reset_session = True

            # if not production or 12 hours have past, then clear our session variables on each call
            if reset_session:
                session.clear()
                seconds_in_12_hours = 60 * 60 * 12
                session['session_time'] = time.time() + seconds_in_12_hours

            if 'username' not in session.keys():
                get_user()

            if 'roles' not in session.keys():
                get_roles()

            if 'profile' not in session.keys():
                session['profile'] = get_profile(session['username'])

            if 'ITS_view' not in session.keys():
                get_its_view()

        def get_user():
            if app.config['ENVIRON'] == 'prod':
                username = request.environ.get('REMOTE_USER')
            else:
                username = app.config['TEST_USER']

            session['username'] = username

        def get_roles(username=None):
            if not username:
                username = session['username']
            url = app.config['API_URL'] + "/username/%s/roles" % username
            r = requests.get(url, auth=(app.config['API_USERNAME'], app.config['API_PASSWORD']))
            roles = fjson.loads(r.content)
            ret = []
            for key in roles.keys():
                ret.append(roles[key]['userRole'])

            session['roles'] = ret

            return ret

        def get_profile(username):
            try:
                common_profile = portal_profile(username)
                if len(common_profile) > 0:
                    common_profile = common_profile[0]
                    if 'photo' in common_profile.keys() and common_profile['photo'] == 'https://bsp-nas-dav.bethel.edu':
                        # This way, if the user has a profile but doesn't have a picture, the template will put in a default
                        # picture
                        common_profile.pop('photo')
                else:
                    session['user_common_profile'] = {}
                    return None
            except:
                # API failed to load profile info, continue without it
                session['user_common_profile'] = {}

                sentry.client.extra_context({
                    'time': time.strftime("%c"),
                    'username': session['username'],
                    'user-roles': session['user_roles'],
                    'error-type': 'Failed to load profile',
                })

                sentry.captureException()
                return None

        def get_its_view():
            try:
                session['ITS_view'] = False
                con = ldap.initialize(app.config['LDAP_CONNECTION_INFO'])
                con.simple_bind_s('BU\svc-tinker', app.config['LDAP_SVC_TINKER_PASSWORD'])

                # code to get all users in a group
                results = con.search_s('ou=Bethel Users,dc=bu,dc=ac,dc=bethel,dc=edu', ldap.SCOPE_SUBTREE,
                                       "(|(&(sAMAccountName=%s)))" % session['username'])

                for result in results:
                    for ldap_string in result[1]['memberOf']:
                        user_iam_group = re.search('CN=([^,]*)', str(ldap_string)).group(1)
                        if user_iam_group == 'ITS - Employees':
                            session['ITS_view'] = True
            except:
                session['ITS_view'] = False

        init_user()

    @route('/', methods=['GET'])
    def index(self):
        depts = departments()
        return render_template('index.html', **locals())

    @route('search', methods=['POST'])
    def search(self):
        data = request.form.to_dict()

        # option is the advanced settings for student/staff
        viewing_role = self.base.get_viewing_role(data)

        if data['first_name'] != '' or data['last_name'] != '':
            return self.base.fl_search(data, viewing_role)
        elif data['username'] != '':
            return self.base.username_search(data, viewing_role)
        elif data['email'] != '':
            return self.base.email_search(data, viewing_role)
        elif data['department'] != '':
            return self.base.dept_search(data, viewing_role)
        elif data['bu_id'] != '':
            return self.base.id_search(data, viewing_role)
        else:
            return abort(500)

    def logout(self):
        session.clear()
        resp = make_response(redirect(app.config['LOGOUT_URL']))
        resp.set_cookie('MOD_AUTH_CAS_S', '', expires=0)
        resp.set_cookie('MOD_AUTH_CAS', '', expires=0)
        return resp
