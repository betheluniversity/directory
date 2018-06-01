from flask import Flask, render_template, request, session
from flask.ext.classy import FlaskView, route

from fuzzywuzzy import fuzz

from app.db.db_functions import portal_profile, directory_search


class ResultsView(FlaskView):
    def __init__(self):
        pass

    @route('/search', methods=['POST'])
    def search(self):
        data = request.form
        last_name = data['last_name'].encode('utf-8')
        first_name = data['first_name'].encode('utf-8')
        people = directory_search()
        result = []
        if first_name != '' and last_name != '':  # If both boxes are filled out, this will be the loop that is checked
            for item in people:
                l_name = people[item]['last_name']
                f_name = people[item]['first_name']
                if fuzz.partial_ratio(l_name, last_name) > 90 and fuzz.partial_ratio(f_name, first_name) > 90:
                    result.append(people[item])

        elif first_name != '' and last_name == '':  # will only be called if first name and NOT last name are filled out
            for item in people:
                f_name = people[item]['first_name']
                if f_name == first_name:
                    result.append(people[item])
                elif fuzz.partial_ratio(f_name, first_name) > 80:
                    result.append(people[item])
                elif fuzz.token_set_ratio(f_name, first_name) > 90:
                    result.append(people[item])
                elif fuzz.token_sort_ratio(f_name, first_name) > 90:
                    result.append(people[item])

        elif last_name != '' and first_name == '':  # called if last name and NOT first name are filled out
            for item in people:
                l_name = people[item]['last_name']
                if l_name == last_name:
                    result.append(people[item])
                elif fuzz.partial_ratio(l_name, last_name) > 80:
                    result.append(people[item])
                elif fuzz.token_set_ratio(l_name, last_name) > 100:
                    result.append(people[item])

        return render_template('test.html', **locals())
