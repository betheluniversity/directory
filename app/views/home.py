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
    def fl_search(self):
        data = request.form
        last_name = data['last_name'].encode('utf-8')
        first_name = data['first_name'].encode('utf-8')
        people = directory_search()
        result = []

        if first_name != '' and last_name != '':  # If both boxes are filled out, this will be the loop that is checked
            for row in people:
                ratio = (self.fuzzy(row['first_name'], row['last_name'], True, first_name) +
                         self.fuzzy(row['first_name'], row['last_name'], False, last_name))

                if ratio >= 75:
                    result.append({'first_name': row['first_name'],
                                   'last_name': row['last_name'],
                                   'ratio': ratio,
                                   'image_path': row['image_path'],
                                   'role': row['role'],
                                   'po': row['po']})

        elif first_name != '' and last_name == '':  # will only be called if first name and NOT last name are filled out
            for row in people:
                ratio = self.fuzzy(row['first_name'], row['last_name'], True, first_name)
                if ratio >= 75:
                    result.append({'first_name': row['first_name'],
                                   'last_name': row['last_name'],
                                   'ratio': ratio,
                                   'image_path': row['image_path'],
                                   'role': row['role'],
                                   'po': row['po']})

        elif last_name != '' and first_name == '':  # called if last name and NOT first name are filled out
            for row in people:
                ratio = self.fuzzy(row['first_name'], row['last_name'], False, last_name)
                if ratio >= 75:
                    result.append({'first_name': row['first_name'],
                                   'last_name': row['last_name'],
                                   'ratio': ratio,
                                   'image_path': row['image_path'],
                                   'role': row['role'],
                                   'po': row['po']})

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'], reverse=True)

        return render_template('results.html', **locals())

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

    @route('/', methods=['POST'])
    def username_search(self):
        data = request.form
        username = data['username'].encode('utf-8')
        people = directory_search()
        result = []

        if username != '':
            for row in people:
                ratio = self.misc_fuzz(username, row['username'])
                if ratio > 75:
                    result.append({'first_name': row['first_name'],
                                   'last_name': row['last_name'],
                                   'ratio': ratio,
                                   'image_path': row['image_path'],
                                   'role': row['role'],
                                   'po': row['po']})

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'])

        return render_template('results.html', **locals())

    def email_search(self):
        data = request.form
        email = data['email'].encode('utf-8')
        people = directory_search()
        result = []

        if email != '':
            for row in people:
                ratio = self.misc_fuzz(email, row['email'])
                if ratio > 75:
                    result.append({'first_name': row['first_name'],
                                   'last_name': row['last_name'],
                                   'ratio': ratio,
                                   'image_path': row['image_path'],
                                   'role': row['role'],
                                   'po': row['po']})

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'])

        return render_template('results.html', **locals())

    def dept_search(self):
        data = request.form
        dept = data['department'].encode('utf-8')
        people = directory_search()
        result = []

        if dept != '':
            for row in people:
                ratio = self.misc_fuzz(dept, row['department'])
                if ratio > 75:
                    result.append({'first_name': row['first_name'],
                                   'last_name': row['last_name'],
                                   'ratio': ratio,
                                   'image_path': row['image_path'],
                                   'role': row['role'],
                                   'po': row['po']})

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'])

        return render_template('results.html', **locals())

    def id_search(self):
        data = request.form
        id = data['id'].encode('utf-8')
        people = directory_search()
        result = []

        if id != '':
            for row in people:
                ratio = self.misc_fuzz(id, row['id'])
                if ratio > 75:
                    result.append({'first_name': row['first_name'],
                                   'last_name': row['last_name'],
                                   'ratio': ratio,
                                   'image_path': row['image_path'],
                                   'role': row['role'],
                                   'po': row['po']})

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'])

        return render_template('results.html', **locals())

    def phone_search(self):
        data = request.form
        phone = data['phone'].encode('utf-8')
        people = directory_search()
        result = []

        if phone != '':
            for row in people:
                ratio = self.misc_fuzz(phone, row['phone'])
                if ratio > 75:
                    result.append({'first_name': row['first_name'],
                                   'last_name': row['last_name'],
                                   'ratio': ratio,
                                   'image_path': row['image_path'],
                                   'role': row['role'],
                                   'po': row['po']})

        result.sort(key=lambda i: i['last_name'])
        result.sort(key=lambda i: i['ratio'])

    def misc_fuzz(self, search, key):
        ratio = fuzz.ratio(search, key)
        if search in key:
            ratio = 101
        if search == key:
            ratio = 102

        return ratio

    @route("/test-this")
    def testing_suite(self):
        # This is the testing suite made for writing the files required to test all the searches for fuzzywuzzy
        people = directory_search()
        names = open('test_names.txt')
        ratio = open('fuzzy_ratio.txt', 'w')
        partial = open('fuzzy_partial_ratio.txt', 'w')
        # opening the db connection and all the files for the tests

        for item in names:
            ratio.write("%s\n\n" % item)
            partial.write("%s\n\n" % item)
            # Writing names into all the files every loop

            for row in people:
                fn = row['first_name']

                ratio_c = 0
                partial_c = 0

                ratio = fuzz.ratio(fn, item)
                if ratio > 50:
                    if ratio_c <= 85:
                        ratio.write("%s, %s, %d" % (row['last_name'], row['first_name'], ratio))
                        ratio_c += 1

                ratio = fuzz.partial_ratio(fn, item)
                if ratio > 50:
                    if partial_c <= 85:
                        partial.write("%s, %s, %d" % (row['last_name'], row['first_name'], ratio))
                        partial_c += 1
