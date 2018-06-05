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

                ratio = (fuzz.ratio(l_name, last_name) + fuzz.ratio(f_name, first_name)) / 2
                # the line above gets the total ratio between both partial ratios

                if f_name == first_name and l_name == last_name:
                    ratio = 120  # if the search matches exactly, it should be first regardless

                if ratio > 75:
                    result.append({'last_name': row['last_name'],
                                   'first_name': row['first_name'],
                                   'ratio': ratio,
                                   'image_path': row['image_path']})

        elif first_name != '' and last_name == '':  # will only be called if first name and NOT last name are filled out
            for row in people:
                f_name = row['first_name']
                ratio = fuzz.ratio(f_name, first_name)

                if f_name == first_name:
                    ratio = 120  # if the search matches exactly, it should be first regardless

                if ratio > 50:
                    result.append({'first_name': row['first_name'],
                                   'last_name': row['last_name'],
                                   'ratio': ratio,
                                   'image_path': row['image_path']})

        elif last_name != '' and first_name == '':  # called if last name and NOT first name are filled out
            for row in people:
                l_name = row['last_name']
                ratio = fuzz.ratio(l_name, last_name)

                if l_name == last_name:
                    ratio = 120  # if the search matches exactly, it should be first regardless

                if ratio > 75:
                    result.append({'last_name': row['last_name'],
                                   'first_name': row['first_name'],
                                   'ratio': ratio,
                                   'image_path': row['image_path']})
            # process.extract(last_name, people['last_name'], limit=25)

        result.sort(key=lambda i: i['ratio'], reverse=True)

        return render_template('results.html', **locals())

    @route("/test-this")
    def testing_suite(self):
        # This is the testing suite made for writing the files required to test all the searches for fuzzywuzzy
        people = directory_search()
        names = open('test_names.txt')
        ratio = open('fuzzy_ratio.txt', 'w')
        partial = open('fuzzy_partial_ratio.txt', 'w')
        token_set = open('fuzzy_token_set.txt', 'w')
        token_sort = open('fuzzy_token_sort.txt', 'w')
        # opening the db connection and all the files for the tests

        for item in names:
            ratio.write("%s\n\n" % item)
            partial.write("%s\n\n" % item)
            token_set.write("%s\n\n" % item)
            token_sort.write("%s\n\n" % item)
            # Writing names into all the files every loop

            for row in people:
                fn = row['first_name']

                ratio_c = 0
                partial_c = 0
                token_set_c = 0
                token_sort_c = 0

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

                ratio = fuzz.token_set_ratio(fn, item)
                if ratio > 50:
                    if token_set_c <= 85:
                        token_set.write("%s, %s, %d" % (row['last_name'], row['first_name'], ratio))
                        token_set_c += 1

                ratio = fuzz.token_sort_ratio(fn, item)
                if ratio > 50:
                    if token_sort_c <= 85:
                        token_sort.write("%s, %s, %d" % (row['last_name'], row['first_name'], ratio))
                        token_sort_c += 1

