import ldap
import re
import requests
import time
from urllib.parse import urlencode

from flask import render_template, request, session, abort, make_response, redirect
from flask import json as fjson
from flask_classy import FlaskView, route

from app import app, sentry_sdk
from sentry_sdk import configure_scope
from app.db.db_functions import portal_profile, reset_directory_data
from app.directory_controller import DirectoryController, requires_auth


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

            if 'ID_view' not in session.keys():
                get_id_view()

            user_has_role = False
            if 'STUDENT' in session['roles'] or 'STAFF' in session['roles'] or 'FACULTY' in session['roles']:
                user_has_role = True

            if user_has_role == False:
                return abort(403)

            log_user(session['username'])

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
                    session['user_common_profile'] = common_profile
                else:
                    session['user_common_profile'] = {}
                    return None
            except:
                # API failed to load profile info, continue without it
                session['user_common_profile'] = {}

                with configure_scope() as scope:
                    scope.set_tag("time", time.strftime("%c"))
                    scope.set_tag("username", session['username'])
                    scope.set_tag("user-roles", session['user_roles'])
                    scope.set_tag("error-type", "Failed to load profile")

                sentry_sdk.capture_exception()
                return None

        def get_id_view():
            try:
                session['ID_view'] = False
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
                con = ldap.initialize(app.config['LDAP_CONNECTION_INFO'])
                con.simple_bind_s('BU\svc-tinker', app.config['LDAP_SVC_TINKER_PASSWORD'])

                # code to get all users in a group
                results = con.search_s('ou=Bethel Users,dc=bu,dc=ac,dc=bethel,dc=edu', ldap.SCOPE_SUBTREE,
                                       "(|(&(sAMAccountName=%s)))" % session['username'])

                for result in results:
                    for ldap_string in result[1]['memberOf']:
                        user_iam_group = re.search('CN=([^,]*)', str(ldap_string)).group(1)
                        if user_iam_group == 'ITS - Employees' or user_iam_group == 'CommMktg - Employees':
                            session['ID_view'] = True
            except:
                session['ID_view'] = False

        def log_user(username):
            if not session.get('user_logged'):
                # split each line, check if username is first.
                # write username, first, last, roles
                with open('{}'.format(app.config['ALL_USERS_CSV_FILE_PATH']), 'r+') as f:
                    file_data = f.read()

                    # if its blank, add the headers
                    if len(file_data) == 0:
                        f.write('Username,Name,Banner Roles')

                    # read the file to see if the user has already been added
                    is_new_user = True
                    for line in file_data.split('\n'):
                        if line.startswith(username):
                            is_new_user = False
                            break

                    if is_new_user:
                        try:
                            name = session['user_common_profile']['pref_first_last_name']
                            banner_roles = '|'.join(session['roles'])
                            user_data = '\n{}, {}, {}'.format(username, name, banner_roles)
                            f.writelines(user_data)
                        except:
                            # don't log a user who doesn't have a pref_first_last_name or roles...
                            pass

                    f.close()
                session['user_logged'] = True

        if '/public/' not in request.url:
            init_user()

    @route('/', methods=['GET'])
    def index(self):
        return render_template('index.html', **locals())

    @requires_auth
    @route('/public/reset-cache', methods=['GET'])
    def reset_cache(self):
        reset_directory_data()
        return 'success'

    @route('/jira-endpoint', methods=['GET'])
    def jira_endpoint(self):
        jira_endpoint = True
        return render_template('index.html', **locals())

    @route('search', methods=['POST'])
    def search(self):
        data = request.form.to_dict()

        # option is the advanced settings for student/staff
        viewing_role = self.base.get_viewing_role(data)

        if data.get('first_name', '') != '' or data.get('last_name', '') != '' or data.get('department', '') != '':  # first and last name search will also factor in department if both are filled out
            results_data = self.base.fl_department_search(data, viewing_role)
        elif data.get('username', '') != '':
            results_data = self.base.username_search(data, viewing_role)
        elif data.get('email', '') != '':
            results_data = self.base.email_search(data, viewing_role)
        elif data.get('bu_id', '') != '':
            results_data = self.base.id_search(data, viewing_role)
        else:
            results_data = {}

        # add the page number to the results
        results_data['page'] = int(data.get('page', 1))
        results = render_template('results.html', **locals())

        # the first page should also load the base
        if results_data['page'] == 1:
            form_data = urlencode(data)
            # user results to build the template?
            return render_template('results_base.html', **locals())
        else:
            return results

    def logout(self):
        session.clear()
        resp = make_response(redirect(app.config['LOGOUT_URL']))
        resp.set_cookie('MOD_AUTH_CAS_S', '', expires=0)
        resp.set_cookie('MOD_AUTH_CAS', '', expires=0)
        return resp
