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
    def get_option(self, data):
        if hasattr(data, 'faculty') and hasattr(data, 'student'):
            return 'both'  # showing all results
        elif hasattr(data, 'faculty'):
            return 'faculty'  # showing just staff/faculty results
        elif hasattr(data, 'student'):
            return 'student'  # showing just student results
        else:
            return 'both'  # defaults to showing all results

    # first and last name search. Holds the details and logic surrounding the first and last name searches
    @route('/', methods=['POST'])
    def fl_search(self):  # option is the advanced settings for student/staff
        data = request.form.to_dict()
        option = self.get_option(data)

        people = directory_search()
        result = []

        if data['first_name'] != '' and data['last_name'] != '':  # If both boxes are filled out, this will be the loop that is checked
            for row in people:
                if self.match_option(row, option):
                    ratio = (self.fl_fuzzy(row['first_name'], row['last_name'], True, data['first_name']) +
                             self.fl_fuzzy(row['first_name'], row['last_name'], False, data['last_name']))

                    if ratio >= 75:
                        self.make_results(row, result, ratio)

        elif data['first_name'] != '' and data['last_name'] == '':  # called if first name and NOT last name are filled out
            for row in people:
                if self.match_option(row, option):
                    ratio = self.fl_fuzzy(row['first_name'], row['last_name'], True, data['first_name'])
                    if ratio >= 75:
                        self.make_results(row, result, ratio)

        elif data['last_name'] != '' and data['first_name'] == '':  # called if last name and NOT first name are filled out
            for row in people:
                if self.match_option(row, option):  # if its true, check the person
                    ratio = self.fl_fuzzy(row['first_name'], row['last_name'], False, data['last_name'])
                    if ratio >= 75:
                        self.make_results(row, result, ratio)

        elif data['last_name'] == '' and data['first_name'] == '':  # if both are empty, return everyone
            result = people
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        depts = departments()  # this will be removed once the ajax is implemented
        return render_template('results.html', **locals())

    # Username search executes, creates, and formats the username searches
    @route('/', methods=['POST'])
    def username_search(self):
        data = request.form.to_dict()
        option = self.get_option(data)

        people = directory_search()
        result = []

        if data['username'] != '':  # put in the student/staff filters
            for row in people:
                if self.match_option(row, option):
                    ratio = self.misc_fuzzy(data['username'], row['username'])
                    if ratio > 75:
                        self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        depts = departments()  # this will be removed once the ajax is implemented
        return render_template('results.html', **locals())

    # Email search, executes, creates, and formats the email search and results
    @route('/', methods=['POST'])
    def email_search(self):
        data = request.form.to_dict()
        option = self.get_option(data)

        people = directory_search()
        result = []

        if data['email'] != '':  # put in the student/staff filters
            for row in people:
                if self.match_option(row, option):
                    ratio = self.misc_fuzzy(data['email'], row['email'])
                    if ratio > 75:
                        self.make_results(row, result, ratio)
        else:
            result = people
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        depts = departments()  # necessary until we build the ajax call for this
        return render_template('results.html', **locals())

    # department search, subject to change
    @route('/', methods=['POST'])
    def dept_search(self):
        data = request.form.to_dict()
        option = self.get_option(data)

        people = directory_search()
        result = []

        if data['department'] != '':
            for row in people:
                if self.match_option(row, option):
                    for item in row['department']:
                        if data['department'] in item:
                            result.append(row)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['id'])

        depts = departments()  # necessary until we build the ajax call for this
        return render_template('results.html', **locals())

    # id search, only visible to those whose roles allow it
    # does the same as the other search functions
    @route('/', methods=['POST'])
    def id_search(self):
        data = request.form.to_dict()
        option = self.get_option(data)

        people = directory_search()
        result = []

        if data['id'] != '':
            for row in people:
                if self.match_option(row, option):
                    ratio = self.misc_fuzzy(data['id'], row['id'])
                    if ratio > 75:
                        self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        depts = departments()  # necessary until we build the ajax call for this
        return render_template('results.html', **locals())

    def match_option(self, row, option, ):
        match_option = False  # does the selected option match the role of the person?
        if option == 'both':
            match_option = True  # if option is both, set to true by default
        else:
            for role in row['role']:
                if role == option:
                    match_option = True  # if the role of the person matches the selected option, set true
        if match_option:  # if its true, check the person
            return True
        return False

    # Fuzzy method for first and last names, contains some extra logic
    def fl_fuzzy(self, first_name, last_name, fl, search):
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

    def misc_fuzzy(self, search, key):  # much simpler fuzz method to use for things other than first or last name
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
