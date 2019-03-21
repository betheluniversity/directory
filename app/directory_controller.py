from flask import render_template
from fuzzywuzzy import fuzz

from app import app
from app.db.db_functions import directory_search


class DirectoryController(object):
    def __init__(self):
        pass

    # first and last name search. Holds the details and logic surrounding the first and last name searches
    def fl_search(self, data, viewing_role):
        people = directory_search()
        result = []
        search_type = []

        # first and last name search
        if data['first_name'] != '' and data['last_name'] != '':
            search_type.append('First name')
            search_type.append('Last name')
            for row in people:
                if self.match_option(row, viewing_role):
                    ratio = (self.fl_fuzzy(row['first_name'], row['last_name'], True, data['first_name']) +
                             self.fl_fuzzy(row['first_name'], row['last_name'], False, data['last_name']))
                    if data['department'] != '':
                        if ratio >= 120 and data['department'] in row['department']:
                            self.make_results(row, result, ratio)
                    else:
                        if ratio >= 120:
                            self.make_results(row, result, ratio)
        # first name search
        elif data['first_name'] != '' and data['last_name'] == '':
            search_type.append('First name')
            for row in people:
                if self.match_option(row, viewing_role):
                    ratio = self.fl_fuzzy(row['first_name'], row['last_name'], True, data['first_name'])
                    if data['department'] != '':
                        if ratio >= 75 and data['department'] in row['department']:
                            self.make_results(row, result, ratio)
                    else:
                        if ratio >= 75:
                            self.make_results(row, result, ratio)
        # last name search
        elif data['last_name'] != '' and data['first_name'] == '':
            search_type.append('Last name')
            for row in people:
                if self.match_option(row, viewing_role):  # if its true, check the person
                    ratio = self.fl_fuzzy(row['first_name'], row['last_name'], False, data['last_name'])
                    if data['department'] != '':
                        if ratio >= 75 and data['department'] in row['department']:
                            self.make_results(row, result, ratio)
                    else:
                        if ratio >= 75:
                            self.make_results(row, result, ratio)

        if data['department'] != '':
            search_type.append('Department')

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return render_template('results.html', **locals())

    # Username search executes, creates, and formats the username searches
    def username_search(self, data, viewing_role):
        people = directory_search()
        result = []
        search_type = ['Username']

        if data['username'] != '':  # put in the student/staff filters
            for row in people:
                if self.match_option(row, viewing_role):
                    ratio = self.misc_fuzzy(data['username'], row['username'])
                    if ratio > 75:
                        self.make_results(row, result, ratio)
        else:
            result = people
            result.sort(key=lambda i: i['last_name'])
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return render_template('results.html', **locals())

    # Email search, executes, creates, and formats the email search and results
    def email_search(self, data, viewing_role):
        people = directory_search()
        result = []
        search_type = ['Email']

        if data['email'] != '':  # put in the student/staff filters
            for row in people:
                if self.match_option(row, viewing_role):
                    ratio = self.misc_fuzzy(data['email'], row['email'])
                    if ratio > 75:
                        self.make_results(row, result, ratio)
        else:
            result = people
            result.sort(key=lambda i: i['last_name'])
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return render_template('results.html', **locals())

    # department search, subject to change
    def dept_search(self, data, viewing_role):
        people = directory_search()
        result = []
        search_type = ['Department']

        if data['department'] != '':
            for row in people:
                if self.match_option(row, viewing_role):
                    for item in row['department']:
                        if data['department'] in item:
                            result.append(row)
                            break
        else:
            result = people
            result.sort(key=lambda i: i['last_name'])
            return render_template('results.html', **locals())

        result.sort(key=lambda i: i['last_name'])

        return render_template('results.html', **locals())

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

        return render_template('results.html', **locals())

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
