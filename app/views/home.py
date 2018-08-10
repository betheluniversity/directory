from flask import Flask, render_template, request, session
from flask_classy import FlaskView, route

from fuzzywuzzy import fuzz

from app.db.db_functions import directory_search


class HomeView(FlaskView):
    def __init__(self):
        pass

    def index(self):
        return render_template('index.html', **locals())

    @route('/', methods=['POST'])
    def passage(self):
        data = request.form

        first_name = ''
        last_name = ''
        username = ''
        email = ''
        department = ''
        bu_id = ''
        phone = ''

        home = False
        group = False
        student = False
        faculty = False

        # decoding the data from the form to pass into the methods
        # first part is the checkboxes for advanced settings
        try:
            if data['home'].encode('utf-8') == 'home':
                home = True
        except:
            pass

        try:
            if data['group'].encode('utf-8') == 'group':
                group = True
        except:
            pass

        try:
            if data['student'].encode('utf-8') == 'student':
                student = True
        except:
            pass

        try:
            if data['faculty'].encode('utf-8') == 'faculty':
                faculty = True
        except:
            pass

        # second part is the fields from the forms
        try:
            first_name = data['first_name'].encode('utf-8')
        except:
            pass
        try:
            last_name = data['last_name'].encode('utf-8')
        except:
            pass

        try:
            username = data['username'].encode('utf-8')
        except:
            pass

        try:
            email = data['email'].encode('utf-8')
        except:
            pass

        try:
            department = data['department'].encode('utf-8')
        except:
            pass

        try:
            bu_id = data['id'].encode('utf-8')
        except:
            pass

        try:
            phone = data['phone'].encode('utf-8')
        except:
            pass

        if first_name != '' or last_name != '':
            if (faculty and student) or (not faculty and not student):
                option = 'both'
            elif faculty and not student:
                option = 'Faculty'
            elif student and not faculty:
                option = 'Student'

            result = self.fl_search(first_name, last_name, option)
        elif username != '':
            result = self.username_search(username)
        elif email != '':
            result = self.email_search(email)
        elif department != '':
            result = self.dept_search(department)
        elif bu_id != '':
            group = True
            result = self.id_search(bu_id)
        elif phone != '':
            result = self.phone_search(phone)
            home = True

        return render_template('results.html', **locals())

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
                    ratio = (self.fuzzy(row['first_name'], row['last_name'], True, first_name) +
                             self.fuzzy(row['first_name'], row['last_name'], False, last_name))

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
                    ratio = self.fuzzy(row['first_name'], row['last_name'], True, first_name)
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
                    ratio = self.fuzzy(row['first_name'], row['last_name'], False, last_name)
                    if ratio >= 75:
                        self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    def username_search(self, username):
        people = directory_search()
        result = []

        if username != '':
            for row in people:
                ratio = self.misc_fuzz(username, row['username'])
                if ratio > 75:
                    self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    def email_search(self, email):
        people = directory_search()
        result = []

        if email != '':
            for row in people:
                ratio = self.misc_fuzz(email, row['email'])
                if ratio > 75:
                    self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    def dept_search(self, department):
        people = directory_search()
        result = []

        if department != '':
            for row in people:
                ratio = self.misc_fuzz(department, row['department'])
                if ratio > 75:
                    self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    def id_search(self, bu_id):
        people = directory_search()
        result = []

        if bu_id != '':
            for row in people:
                ratio = self.misc_fuzz(bu_id, row['id'])
                if ratio > 75:
                    self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    def phone_search(self, phone):
        people = directory_search()
        result = []

        if phone != '':
            for row in people:
                ratio = self.misc_fuzz(phone, row['phone'])
                if ratio > 75:
                    self.make_results(row, result, ratio)

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return result

    def fuzzy(self, first_name, last_name, fl, search):
        if fl:
            name = first_name
        else:
            name = last_name

        if len(search.decode('utf-8')) <= 3:
            ratio = fuzz.partial_ratio(name, search)
        else:
            ratio = fuzz.ratio(name, search)

        if search in name:
            ratio = 101
        if search == name:
            ratio = 102

        return ratio

    def misc_fuzz(self, search, key):
        ratio = fuzz.ratio(search, key)
        if search in key:
            ratio = 101
        if search == key:
            ratio = 102

        return ratio

    def make_results(self, row, result, ratio):
        row['ratio'] = ratio
        result.append(row)
