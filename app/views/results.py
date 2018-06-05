from flask import Flask, render_template, request, session
from flask.ext.classy import FlaskView, route

from fuzzywuzzy import fuzz, process

from app.db.db_functions import directory_search


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
            for row in people:
                l_name = row['last_name']
                f_name = row['first_name']
                ratio = fuzz.partial_ratio(l_name, last_name) + fuzz.partial_ratio(f_name, first_name)
                # the line above gets the total ratio between both partial ratios
                if ratio > 100:
                    result.append({'last_name': row['last_name'],
                                   'first_name': row['first_name'],
                                   'ratio': ratio})

        elif first_name != '' and last_name == '':  # will only be called if first name and NOT last name are filled out
            for row in people:
                f_name = row['first_name']
                ratio = fuzz.partial_ratio(f_name, first_name)
                if ratio > 50:
                    result.append({'first_name': first_name,
                                   'last_name': row['last_name'],
                                   'ratio': ratio})

        elif last_name != '' and first_name == '':  # called if last name and NOT first name are filled out
            for row in people:
                l_name = row['last_name']
                ratio = fuzz.partial_ratio(l_name, last_name)
                if ratio > 50:
                    result.append({'last_name': l_name,
                                   'first_name': row['first_name'],
                                   'ratio': ratio})
            # process.extract(last_name, people['last_name'], limit=25)

        result.sort(key=lambda i: i['ratio'], reverse=True)

        return render_template('results.html', **locals())
