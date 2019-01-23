from flask import Flask, render_template, request, session
from flask_classy import FlaskView, route

from fuzzywuzzy import fuzz
from werkzeug.exceptions import BadRequestKeyError

from app.db.db_functions import directory_search, departments


class View(FlaskView):
    def __init__(self):
        pass

    def index(self):
        depts = departments()
        return render_template('index.html', **locals())

    @route('/profile', methods=['GET'])
    def make_profile(self):
        # profile is in the session keys
        return render_template('profile.html', **locals())

    @route('/', methods=['POST'])
    def passage(self):
        data = self._get_data(request.form.to_dict())

        if data['home'] == 'home':
            home = True
        if data['group'] == 'group':
            group = True

        if data['first_name'] != '' or data['last_name'] != '':  # checking which people to show for name search
            if data['faculty'] != '' and data['student'] == '':
                option = 'faculty'  # showing just staff/faculty results
            elif data['student'] != '' and data['faculty'] == '':
                option = 'student'  # showing just student results
            else:
                option = 'both'  # showing all results

            result = self._fl_search(data['first_name'], data['last_name'], option)

        elif data['username'] != '':
            result = self._username_search(data['username'])

        elif data['email'] != '':
            result = self._email_search(data['email'])

        elif data['department'] != '':
            group = True
            result = self._dept_search(data['department'])

        elif data['bu_id'] != '':
            group = True
            result = self._id_search(data['bu_id'])

        depts = departments() # so we can use the autocompleter in the department search after reloading the page
        return render_template('results.html', **locals())

    def _get_data(self, data):  # method to ensure we have data in all variables
        # Bruteforcing this because I HAVE to try/except every. single. line.
        # If BadRequestKeyErrors can be mass checked, I don't know how
        try:
            data['home'] = data['home']
        except (BadRequestKeyError, KeyError):
            data['home'] = ''
        try:
            data['group'] = data['group']
        except (BadRequestKeyError, KeyError):
            data['group'] = ''
        try:
            data['student'] = data['student']
        except (BadRequestKeyError, KeyError):
            data['student'] = ''
        try:
            data['faculty'] = data['faculty']
        except (BadRequestKeyError, KeyError):
            data['faculty'] = ''

        # second part is the fields from the forms
        try:
            data['first_name'] = data['first_name']
        except (BadRequestKeyError, KeyError):
            data['first_name'] = ''
        try:
            data['last_name'] = data['last_name']
        except (BadRequestKeyError, KeyError):
            data['last_name'] = ''
        try:
            data['username'] = data['username']
        except (BadRequestKeyError, KeyError):
            data['username'] = ''
        try:
            data['email'] = data['email']
        except (BadRequestKeyError, KeyError):
            data['email'] = ''
        try:
            data['department'] = data['department']
        except (BadRequestKeyError, KeyError):
            data['department'] = ''
        try:
            data['bu_id'] = data['bu_id']
        except (BadRequestKeyError, KeyError):
            data['bu_id'] = ''

        return data

    # first and last name search. Holds the details and logic surrounding the first and last name searches
    def _fl_search(self, first_name, last_name, option):  # option is the advanced settings for student/staff
        people = directory_search()
        result = []

        if first_name != '' and last_name != '':  # If both boxes are filled out, this will be the loop that is checked
            for person in people:
                check = False
                if option == 'both':
                    check = True
                else:
                    for role in person['role']:
                        if role == option:
                            check = True
                if check:
                    ratio = (self._fl_fuzzy(person['first_name'], person['last_name'], True, first_name) +
                             self._fl_fuzzy(person['first_name'], person['last_name'], False, last_name))

                    if ratio >= 75:
                        self._make_results(person, result, ratio)

        elif first_name != '' and last_name == '':  # called if first name and NOT last name are filled out
            for person in people:
                check = False
                if option == 'both':
                    check = True
                else:
                    for role in person['role']:
                        if role == option:
                            check = True
                if check:
                    ratio = self._fl_fuzzy(person['first_name'], person['last_name'], True, first_name)
                    if ratio >= 75:
                        self._make_results(person, result, ratio)

        elif last_name != '' and first_name == '':  # called if last name and NOT first name are filled out
            for person in people:
                check = False
                if option == 'both':
                    check = True
                else:
                    for role in person['role']:
                        if role == option:
                            check = True
                if check:
                    ratio = self._fl_fuzzy(person['first_name'], person['last_name'], False, last_name)
                    if ratio >= 75:
                        self._make_results(person, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    # Username search executes, creates, and formats the username searches
    def _username_search(self, username):
        people = directory_search()
        result = []

        if username != '':
            for person in people:
                ratio = self._other_fuzzy(username, person['username'])
                if ratio > 75:
                    self._make_results(person, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    # Email search, executes, creates, and formats the email search and results
    def _email_search(self, email):
        people = directory_search()
        result = []

        if email != '':
            for person in people:
                ratio = self._other_fuzzy(email, person['email'])
                if ratio > 75:
                    self._make_results(person, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    # department search, subject to change
    def _dept_search(self, department):
        people = directory_search()
        result = []

        if department != '':
            for person in people:
                for item in person['department']:
                    if department in item:
                        result.append(person)
                        break

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['id'])

        return result

    # id search, only visible to those whose roles allow it
    # does the same as the other search functions
    def _id_search(self, bu_id):
        people = directory_search()
        result = []

        if bu_id != '':
            for person in people:
                if bu_id in person['id']:
                    result.append(person)

        return result

    # Fuzzy method for first and last names, contains some extra logic
    def _fl_fuzzy(self, first_name, last_name, fl, search):
        if fl:  # simpler logic to decide which name is being searched, first or last
            name = first_name
        else:
            name = last_name

        # if len(search.decode('utf-8')) <= 3:  # above logic is so this can blanket the rest of the fuzzy comparison
        if len(search) <= 3:  # above logic is so this can blanket the rest of the fuzzy comparison
            ratio = fuzz.partial_ratio(name, search)  # also utilizes partial ratio instead of just fuzz.ratio
        else:
            ratio = fuzz.ratio(name, search)

        if search in name:
            ratio = 101
        if search == name:
            ratio = 102

        return ratio

    def _other_fuzzy(self, search, key):  # much simpler fuzz method to use for things other than first or last name
        ratio = fuzz.ratio(search, key)
        if search in key:
            ratio = 101
        if search == key:
            ratio = 102

        return ratio

    # only called if the fuzz ratio surpasses a certain threshold
    def _make_results(self, row, result, ratio):  # just creates a dictionary for ratio
        row['ratio'] = ratio
        result.append(row)
