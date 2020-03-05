from functools import wraps
import math

from flask import render_template, request, Response
from fuzzywuzzy import fuzz

from app import app
from app.db.db_functions import directory_search


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == app.config['CASCADE_LOGIN']['username'] and password == app.config['CASCADE_LOGIN']['password']


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


class DirectoryController(object):
    def __init__(self):
        pass

    # first and last name search. Holds the details and logic surrounding the first and last name searches
    def fl_department_search(self, data, viewing_role):
        people = directory_search()
        result = []
        search_type = []

        # set the search_type options
        # for dept searches, transfer over the dept names
        if data['department'] != '':
            search_type.append('Department: {}'.format(data['department']))
            data['first_name'] = data['dept_first_name']
            data['last_name'] = data['dept_last_name']
        if data['first_name'] != '':
            search_type.append('First name: {}'.format(data['first_name']))
        if data['last_name'] != '':
            search_type.append('Last name: {}'.format(data['last_name']))

        # first and last name search
        if data['first_name'] != '' and data['last_name'] != '':
            for row in people:
                if self.match_option(row, viewing_role):
                    ratio = (self.fl_fuzzy(row['first_name'], row['last_name'], True, data['first_name']) +
                             self.fl_fuzzy(row['first_name'], row['last_name'], False, data['last_name']))/2
                    if data['department'] != '':
                        if ratio >= 60 and data['department'] in row['department']:
                            self.make_results(row, result, ratio)
                    else:
                        if ratio >= 60:
                            self.make_results(row, result, ratio)
            result.sort(key=lambda i: i['first_name'])
            result.sort(key=lambda i: i['last_name'])
        # first name search
        elif data['first_name'] != '' and data['last_name'] == '':
            for row in people:
                if self.match_option(row, viewing_role):
                    ratio = self.fl_fuzzy(row['first_name'], row['last_name'], True, data['first_name'])
                    if data['department'] != '':
                        if ratio >= 75 and data['department'] in row['department']:
                            self.make_results(row, result, ratio)
                    else:
                        if ratio >= 75:
                            self.make_results(row, result, ratio)
            result.sort(key=lambda i: i['last_name'])
            result.sort(key=lambda i: i['first_name'])
        # last name search
        elif data['last_name'] != '' and data['first_name'] == '':
            for row in people:
                if self.match_option(row, viewing_role):  # if its true, check the person
                    ratio = self.fl_fuzzy(row['first_name'], row['last_name'], False, data['last_name'])
                    if data['department'] != '':
                        if ratio >= 75 and data['department'] in row['department']:
                            self.make_results(row, result, ratio)
                    else:
                        if ratio >= 75:
                            self.make_results(row, result, ratio)
            result.sort(key=lambda i: i['first_name'])
            result.sort(key=lambda i: i['last_name'])
        else:
            for row in people:
                if self.match_option(row, viewing_role):  # if its true, check the person
                    ratio = self.fl_fuzzy(row['first_name'], row['last_name'], False, data['last_name'])
                    if data['department'] != '':
                        if data['department'] in row['department']:
                            self.make_results(row, result, ratio)
                    else:
                        self.make_results(row, result, ratio)
            result.sort(key=lambda i: i['first_name'])
            result.sort(key=lambda i: i['last_name'])

        result.sort(key=lambda i: i['ratio'], reverse=True)

        return {
            'results': result,
            'search_type': search_type,
            'total_pages': math.ceil(len(result)/20)
        }

    # Username search executes, creates, and formats the username searches
    def username_search(self, data, viewing_role):
        people = directory_search()
        result = []
        search_type = ['Username: {}'.format(data['username'])]

        if data['username'] != '':  # put in the student/staff filters
            for row in people:
                if self.match_option(row, viewing_role):
                    if row['username'] == data['username']:
                        self.make_results(row, result, 140)
        else:
            result = people
            result.sort(key=lambda i: i['last_name'])
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return {
            'results': result,
            'search_type': search_type,
            'total_pages': math.ceil(len(result)/20)
        }

    # Email search, executes, creates, and formats the email search and results
    def email_search(self, data, viewing_role):
        people = directory_search()
        result = []
        search_type = ['Email: {}'.format(data['email'])]

        if data['email'] != '':  # put in the student/staff filters
            for row in people:
                if self.match_option(row, viewing_role):
                    ratio = self.misc_fuzzy(data['email'], row['email'])
                    if row['email'] == data['email']:
                        self.make_results(row, result, 140)
        else:
            result = people
            result.sort(key=lambda i: i['last_name'])
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return {
            'results': result,
            'search_type': search_type,
            'total_pages': math.ceil(len(result)/20)
        }

    # id search, only visible to those whose roles allow it
    # does the same as the other search functions
    def id_search(self, data, viewing_role):
        people = directory_search()
        result = []
        search_type = ['ID']

        if data['bu_id'] != '':
            for row in people:
                if self.match_option(row, viewing_role):
                    if data['bu_id'] in row['id']:
                        result.append(row)
        else:
            result = people
            result.sort(key=lambda i: i['last_name'])
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])

        return {
            'results': result,
            'search_type': search_type,
            'total_pages': math.ceil(len(result)/20)
        }

    def phone_search(self, data, viewing_role):
        people = directory_search()
        result = []
        data_phone = data['phone_number'].replace('-', '').replace('.', '')
        search_type = ['Phone Number: {}'.format(data_phone)]

        if data_phone != '':
            for row in people:
                if self.match_option(row, viewing_role):
                    if data_phone in row['phone'].replace('.', ''):
                        result.append(row)
            result.sort(key=lambda i: i['last_name'])

        return {
            'results': result,
            'search_type': search_type,
            'total_pages': math.ceil(len(result)/20)
        }

    def get_viewing_role(self, data):
        if data.get('faculty_or_staff') == 'true' and data.get('student') == 'true':
            return 'both'  # showing all results
        elif data.get('faculty_or_staff') == 'true':
            return 'Faculty_or_Staff'  # showing just staff/faculty results
        elif data.get('student') == 'true':
            return 'Student'  # showing just student results
        else:
            return 'both'  # defaults to showing all results

    def match_option(self, row, option):
        if option == 'both':
            return True
        else:
            for role in row['role']:
                if role in option:
                    return True
        return False

    # Fuzzy method for first and last names, contains some extra logic
    def fl_fuzzy(self, first_name, last_name, fl, search):
        if fl:  # simpler logic to decide which name is being searched, first or last
            name = first_name
        else:
            name = last_name

        name = self.clean_search_text(name)
        search = self.clean_search_text(search)

        # if len(search.decode('utf-8')) <= 3:  # above logic is so this can blanket the rest of the fuzzy comparison
        if len(search) <= 3:  # above logic is so this can blanket the rest of the fuzzy comparison
            ratio = fuzz.partial_ratio(name, search)  # also utilizes partial ratio instead of just fuzz.ratio
        else:
            ratio = fuzz.ratio(name, search)

        # if the text is an exact match, prioritize it.
        if search == name:
            ratio = 140
        elif name.startswith(search):
            ratio = 120
        elif search in name:
            ratio = 101

        return ratio

    def misc_fuzzy(self, search, key):  # much simpler fuzz method to use for things other than first or last name
        search = self.clean_search_text(search)
        key = self.clean_search_text(key)

        ratio = fuzz.ratio(search, key)
        # if the text is an exact match, prioritize it.
        if search == key:
            ratio = 140
        elif key.startswith(search):
            ratio = 120
        elif search in key:
            ratio = 101

        return ratio

    # only called if the fuzz ratio surpasses a certain threshold
    def make_results(self, row, result, ratio):  # just creates a dictionary for ratio
        row['ratio'] = ratio
        result.append(row)

    def clean_search_text(self, text):
        return text.lower().strip()
