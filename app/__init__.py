import jinja2

from flask import Flask, render_template, session
import datetime

from app import person, query

app = Flask(__name__)
app.config.from_object('config')
from app.db import db_functions as db

# Shows the year for the template
app.jinja_env.globals.update(now=datetime.datetime.now())
