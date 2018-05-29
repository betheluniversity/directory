import jinja2

from flask import Flask, render_template, request, session
from flask.ext.classy import FlaskView, route
import datetime

from app import query, person
from app.db.db_functions import portal_profile


class ResultsView(FlaskView):
    def __init__(self):
        pass

    def results(self):
        repeat = 10
        return render_template('results.html', repeat=repeat)

    def search(self):
        data = request.form
        # The Query
        search_for = query.Query(data["firstName"], data['lastName'])

        if "Students" in data:
            search_for.student(data['Students'])
        if "Pictures" in data:
            search_for.__set__("picture", data['Students'])
        if "Groups" in data:
            search_for.__set__("groups", data['Students'])
        if "Home" in data:
            search_for.__set__("home", data['Students'])
        if "Staff" in data:
            search_for.teacher(data['Staff'])

        people = self.make_dummy()
        students = []
        faculty = []
        for user in people:
            if search_for.student == "Students":
                if user.role == "student":
                    students.append(user)
            if search_for.teacher == "Staff":
                if user.role == "faculty":
                    faculty.append(user)
        return render_template(self.results(), students=students, faculty=faculty, query=search_for)

    def make_dummy(self):
        people = []
        # for i in range(3):
        #     people.append(person.Person("Boston", "Knighton-Johnson", "bak45247@bethel.edu", "Heritage Hall 105A", 1368, "student", "https://bsp-nas-dav.bethel.edu/IDCentre/Photos/51189.jpg"))
        #     people.append(person.Person("Jay", "Barnes", "j-barnes@bethel.edu", "CLC 234", 2372, "faculty", "https://bsp-nas-dav.bethel.edu/IMAGES/CARS/CARS/20010905/13145000.JPG"))
        #     people.append(person.Person("Eric", "Jameson", "e-jameson@bethel.edu", "St. Paul", 2355, "faculty", "https://bsp-nas-dav.bethel.edu/IDCentre/Photos/36897.jpg"))
        # return people
        people.append(portal_profile('bak45247'))
        return people
