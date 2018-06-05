class Person:

    def __init__(self, first_name=None, last_name=None, email=None, living=None, po=None, role=None, picture=None, home=None, groups=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.living = living
        self.po = po
        self.role = role
        self.home = home
        self.picture = picture
        self.groups = groups

    @property
    def first_name(self):
        return self.first_name

    @first_name.setter
    def first_name(self, value):
        self.first_name = value

    @property
    def last_name(self):
        return self.last_name

    @last_name.setter
    def last_name(self, value):
        self.last_name = value

    @property
    def email(self):
        return self.email

    @email.setter
    def email(self, value):
        self.email = value

    @property
    def living(self):
        return self.living

    @living.setter
    def living(self, value):
        self.living = value

    @property
    def po(self):
        return self.po

    @po.setter
    def po(self, value):
        self.po = value

    @property
    def home(self):
        return self.home

    @home.setter
    def home(self, value):
        self.home = value

    @property
    def picture(self):
        return self.picture

    @picture.setter
    def picture(self, value):
        self.picture = value

    @property
    def groups(self):
        return self.groups

    @groups.setter
    def groups(self, value):
        self.groups = value
