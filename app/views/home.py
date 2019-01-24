from flask import Flask, render_template, request, session, abort
from flask_classy import FlaskView, route

from fuzzywuzzy import fuzz

from app.db.db_functions import directory_search, departments


class View(FlaskView):
    def __init__(self):
        pass

    @route('/', methods=['GET'])
    def index(self):
        depts = departments()
        return render_template('index.html', **locals())

    # Todo: someday we can add in a profile view
    # @route('/profile', methods=['GET'])
    # def make_profile(self):
    #     # profile is in the session keys
    #     return render_template('profile.html', **locals())

    # first and last name search. Holds the details and logic surrounding the first and last name searches
    @route('/fl_search', methods=['POST'])
    def fl_search(self):  # option is the advanced settings for student/staff
        data = request.form.to_dict()
        option = self._get_option(data)

        people = directory_search()
        result = []

        if data['first_name'] != '' and data['last_name'] != '':  # If both boxes are filled out, this will be the loop that is checked
            for row in people:
                if self._match_option(row, option):
                    ratio = (self._fl_fuzzy(row['first_name'], row['last_name'], True, data['first_name']) +
                             self._fl_fuzzy(row['first_name'], row['last_name'], False, data['last_name']))
                    if ratio >= 75:
                        self._make_results(row, result, ratio)
        elif data['first_name'] != '' and data['last_name'] == '':  # called if first name and NOT last name are filled out
            for row in people:
                if self._match_option(row, option):
                    ratio = self._fl_fuzzy(row['first_name'], row['last_name'], True, data['first_name'])
                    if ratio >= 75:
                        self._make_results(row, result, ratio)
        elif data['last_name'] != '' and data['first_name'] == '':  # called if last name and NOT first name are filled out
            for row in people:
                if self._match_option(row, option):  # if its true, check the person
                    ratio = self._fl_fuzzy(row['first_name'], row['last_name'], False, data['last_name'])
                    if ratio >= 75:
                        self._make_results(row, result, ratio)

        elif data['last_name'] == '' and data['first_name'] == '':  # if both are empty, return everyone
            result = people
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return render_template('results.html', **locals())

    # Username search executes, creates, and formats the username searches
    @route('/username_search', methods=['POST'])
    def username_search(self):
        data = request.form.to_dict()
        option = self._get_option(data)

        people = directory_search()
        result = []

        if data['username'] != '':  # put in the student/staff filters
            for row in people:
                if self._match_option(row, option):
                    ratio = self._misc_fuzzy(data['username'], row['username'])
                    if ratio > 75:
                        self._make_results(row, result, ratio)
        else:
            result = people
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return render_template('results.html', **locals())

    # Email search, executes, creates, and formats the email search and results
    @route('/email_search', methods=['POST'])
    def email_search(self):
        data = request.form.to_dict()
        option = self._get_option(data)

        people = directory_search()
        result = []

        if data['email'] != '':  # put in the student/staff filters
            for row in people:
                if self._match_option(row, option):
                    ratio = self._misc_fuzzy(data['email'], row['email'])
                    if ratio > 75:
                        self._make_results(row, result, ratio)
        else:
            result = people
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return render_template('results.html', **locals())

    # department search, subject to change
    @route('/dept_search', methods=['POST'])
    def dept_search(self):
        data = request.form.to_dict()
        option = self._get_option(data)

        people = directory_search()
        result = []

        if data['department'] != '':
            for row in people:
                if self._match_option(row, option):
                    for item in row['department']:
                        if data['department'] in item:
                            result.append(row)
                            break
        else:
            result = people
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['id'])

        return render_template('results.html', **locals())

    # id search, only visible to those whose roles allow it
    # does the same as the other search functions
    @route('/id_search', methods=['POST'])
    def id_search(self):
        data = request.form.to_dict()
        option = self._get_option(data)

        people = directory_search()
        result = []

        if data['bu_id'] != '':
            for row in people:
                if self._match_option(row, option):
                    ratio = self._misc_fuzzy(data['bu_id'], row['id'])
                    if ratio > 75:
                        self._make_results(row, result, ratio)
        else:
            result = people
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return render_template('results.html', **locals())

    def _get_option(self, data):
        if data.get('faculty') == 'true' and data.get('student') == 'true':
            return 'both'  # showing all results
        elif data.get('faculty') == 'true':
            return 'faculty'  # showing just staff/faculty results
        elif data.get('student') == 'true':
            return 'student'  # showing just student results
        else:
            return 'both'  # defaults to showing all results

    def _match_option(self, row, option, ):
        if option == 'both':
            return True
        else:
            for role in row['role']:
                if role.lower() == option:
                    return True
        return False

    # Fuzzy method for first and last names, contains some extra logic
    def _fl_fuzzy(self, first_name, last_name, fl, search):
        if fl:  # simpler logic to decide which name is being searched, first or last
            name = first_name
        else:
            name = last_name

        name = self._clean_search_text(name)
        search = self._clean_search_text(search)

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

    def _misc_fuzzy(self, search, key):  # much simpler fuzz method to use for things other than first or last name
        search = self._clean_search_text(search)
        key = self._clean_search_text(key)

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

    def _clean_search_text(self, text):
        return text.lower().strip()