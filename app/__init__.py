import jinja2

from flask import Flask, render_template, request
import datetime
from app import person, query
app = Flask(__name__)

# Shows the year for the template
app.jinja_env.globals.update(now=datetime.datetime.now())

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/results")
def results():
    repeat = 10
    return render_template('results.html', repeat=repeat)


@app.route("/search", methods=["POST"])
def search():
    data = request.form
    # The Query
    search_for = query.Query(data["firstName"], data['lastName'])

    if "Students" in data:
        search_for.set_student(data['Students'])
    #TODO FIx the following blocks
    if "Pictures" in data:
        search_for.__set__("picture", data['Students'])
    if "Groups" in data:
        search_for.__set__("groups", data['Students'])
    if "Home" in data:
        search_for.__set__("home", data['Students'])
    if "Staff" in data:
        search_for.set_teacher(data['Staff'])

    people = make_dummy()
    students = []
    faculty = []
    for user in people:
        if search_for.student == "Students":
            if user.role == "student":
                students.append(user)
        if search_for.teacher == "Staff":
            if user.role == "faculty":
                faculty.append(user)
    return render_template('results.html', students=students, faculty=faculty, query=search_for)


def make_dummy():
    people = []
    for i in range(3):
        people.append(person.Person("Boston", "Knighton-Johnson", "bak45247@bethel.edu", "Heritage Hall 105A", 1368, "student", "https://bsp-nas-dav.bethel.edu/IDCentre/Photos/51189.jpg"))
        people.append(person.Person("Jay", "Barnes", "j-barnes@bethel.edu", "CLC 234", 2372, "faculty", "https://bsp-nas-dav.bethel.edu/IMAGES/CARS/CARS/20010905/13145000.JPG"))
        people.append(person.Person("Eric", "Jameson", "e-jameson@bethel.edu", "St. Paul", 2355, "faculty", "https://bsp-nas-dav.bethel.edu/IDCentre/Photos/36897.jpg"))
    return people
