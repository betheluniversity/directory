class Query:

    def __init__(self, first_name, last_name, student=None, teacher=None, home=None, picture=None, groups=None):
        self.first_name = first_name
        self.last_name = last_name
        self.student = student
        self.teacher = teacher
        self.home = home
        self.picture = picture
        self.groups = groups

    # instance property and setter
    @property
    def instance(self):
        return self.instance

    @instance.setter
    def instance(self, value):
        self.instance = value

    # student property and setter
    @property
    def student(self):
        return self.student

    @student.setter
    def student(self, value):
        self.student = value

    @property
    def teacher(self):
        return self.teacher

    @teacher.setter
    def teacher(self, value):
        self.teacher = value
