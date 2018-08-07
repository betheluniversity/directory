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
            result = self.fl_search(first_name, last_name)
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

    def fl_search(self, first_name, last_name):
        people = directory_search()
        result = []

        if first_name != '' and last_name != '':  # If both boxes are filled out, this will be the loop that is checked
            for row in people:
                ratio = (self.fuzzy(row['first_name'], row['last_name'], True, first_name) +
                         self.fuzzy(row['first_name'], row['last_name'], False, last_name))

                if ratio >= 75:
                    self.make_results(row, result, ratio)

        elif first_name != '' and last_name == '':  # called if first name and NOT last name are filled out
            for row in people:
                ratio = self.fuzzy(row['first_name'], row['last_name'], True, first_name)
                if ratio >= 75:
                    self.make_results(row, result, ratio)

        elif last_name != '' and first_name == '':  # called if last name and NOT first name are filled out
            for row in people:
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
        result.sort(key=lambda i: i['ratio'])

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
        result.sort(key=lambda i: i['ratio'])

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
        result.sort(key=lambda i: i['ratio'])

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
        result.sort(key=lambda i: i['ratio'])

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
        result.sort(key=lambda i: i['ratio'])

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
