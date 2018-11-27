from flask import Flask, render_template, request, session
from flask_classy import FlaskView, route

from fuzzywuzzy import fuzz
from werkzeug.exceptions import BadRequestKeyError

from app.db.db_functions import directory_search


class View(FlaskView):
    def __init__(self):
        pass

    def index(self):
        return render_template('index.html', **locals())

    @route('/profile', methods=['GET'])
    def make_profile(self):
        # profile is in the session keys
        return render_template('profile.html', **locals())

    @route('/', methods=['POST'])
    def passage(self):
        data = self.encode_data(request.form.to_dict())

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

            result = self.fl_search(data['first_name'], data['last_name'], option)

        elif data['username'] != '':
            result = self.username_search(data['username'])

        elif data['email'] != '':
            result = self.email_search(data['email'])

        elif data['department'] != '':
            result = self.dept_search(data['department'])

        elif data['bu_id'] != '':
            group = True
            result = self.id_search(data['bu_id'])

        return render_template('results.html', **locals())

    def encode_data(self, data):  # method to encode unicode to standard utf-8 charset
        # Bruteforcing this because I HAVE to try/except every. single. line.
        # If BadRequestKeyErrors can be mass checked, I don't know how
        try:
            data['home'] = data['home'].encode('utf-8')
        except (BadRequestKeyError, KeyError):
            data['home'] = ''
            pass
        try:
            data['group'] = data['group'].encode('utf-8')
        except (BadRequestKeyError, KeyError):
            data['group'] = ''
            pass
        try:
            data['student'] = data['student'].encode('utf-8')
        except (BadRequestKeyError, KeyError):
            data['student'] = ''
        try:
            data['faculty'] = data['faculty'].encode('utf-8')
        except (BadRequestKeyError, KeyError):
            data['faculty'] = ''

        # second part is the fields from the forms
        try:
            data['first_name'] = data['first_name'].encode('utf-8')
        except (BadRequestKeyError, KeyError):
            pass
        try:
            data['last_name'] = data['last_name'].encode('utf-8')
        except (BadRequestKeyError, KeyError):
            pass
        try:
            data['username'] = data['username'].encode('utf-8')
        except (BadRequestKeyError, KeyError):
            pass
        try:
            data['email'] = data['email'].encode('utf-8')
        except (BadRequestKeyError, KeyError):
            pass
        try:
            data['department'] = data['department'].encode('utf-8')
        except (BadRequestKeyError, KeyError):
            pass
        try:
            data['bu_id'] = data['bu_id'].encode('utf-8')
        except (BadRequestKeyError, KeyError):
            pass

        return data

    # first and last name search. Holds the details and logic surrounding the first and last name searches
    def fl_search(self, first_name, last_name, option):  # option is the advanced settings for student/staff
        people = directory_search()
        result = []

        if first_name != '' and last_name != '':  # If both boxes are filled out, this will be the loop that is checked
            for row in people:
                check = False
                if option == 'both':
                    check = True
                else:
                    for role in row['role']:
                        if role == option:
                            check = True
                if check:
                    ratio = (self.fl_fuzzy(row['first_name'], row['last_name'], True, first_name) +
                             self.fl_fuzzy(row['first_name'], row['last_name'], False, last_name))

                    if ratio >= 75:
                        self.make_results(row, result, ratio)

        elif first_name != '' and last_name == '':  # called if first name and NOT last name are filled out
            for row in people:
                check = False
                if option == 'both':
                    check = True
                else:
                    for role in row['role']:
                        if role == option:
                            check = True
                if check:
                    ratio = self.fl_fuzzy(row['first_name'], row['last_name'], True, first_name)
                    if ratio >= 75:
                        self.make_results(row, result, ratio)

        elif last_name != '' and first_name == '':  # called if last name and NOT first name are filled out
            for row in people:
                check = False
                if option == 'both':
                    check = True
                else:
                    for role in row['role']:
                        if role == option:
                            check = True
                if check:
                    ratio = self.fl_fuzzy(row['first_name'], row['last_name'], False, last_name)
                    if ratio >= 75:
                        self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    # Username search executes, creates, and formats the username searches
    def username_search(self, username):
        people = directory_search()
        result = []

        if username != '':
            for row in people:
                ratio = self.other_fuzzy(username, row['username'])
                if ratio > 75:
                    self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    # Email search, executes, creates, and formats the email search and results
    def email_search(self, email):
        people = directory_search()
        result = []

        if email != '':
            for row in people:
                ratio = self.other_fuzzy(email, row['email'])
                if ratio > 75:
                    self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    # department search, subject to change
    def dept_search(self, department):
        people = directory_search()
        result = []

        if department != '':
            for row in people:
                ratio = self.other_fuzzy(department, row['department'])
                if ratio > 75:
                    self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    # id search, only visible to those whose roles allow it
    # does the same as the other search functions
    def id_search(self, bu_id):
        people = directory_search()
        result = []

        if bu_id != '':
            for row in people:
                ratio = self.other_fuzzy(bu_id, row['id'])
                if ratio > 75:
                    self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    # Fuzzy method for first and last names, contains some extra logic
    def fl_fuzzy(self, first_name, last_name, fl, search):
        if fl:  # simpler logic to decide which name is being searched, first or last
            name = first_name
        else:
            name = last_name

        if len(search.decode('utf-8')) <= 3:  # above logic is so this can blanket the rest of the fuzzy comparison
            ratio = fuzz.partial_ratio(name, search)  # also utilizes partial ratio instead of just fuzz.ratio
        else:
            ratio = fuzz.ratio(name, search)

        if search in name:
            ratio = 101
        if search == name:
            ratio = 102

        return ratio

    def other_fuzzy(self, search, key):  # much simpler fuzz method to use for things other than first or last name
        ratio = fuzz.ratio(search, key)
        if search in key:
            ratio = 101
        if search == key:
            ratio = 102

        return ratio

    # only called if the fuzz ratio surpasses a certain threshold
    def make_results(self, row, result, ratio):  # just creates a dictionary for ratio
        row['ratio'] = ratio
        result.append(row)
