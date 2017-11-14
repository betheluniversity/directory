class Query:

    def __init__(self, first_name, last_name, student=None, teacher=None, home=None, picture=None, groups=None):
        self.first_name = first_name
        self.last_name = last_name
        self.student = student
        self.teacher = teacher
        self.home = home
        self.picture = picture
        self.groups = groups

    def __set__(self, instance, value):
        self.instance = value
