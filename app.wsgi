activate_this = '/opt/directory/env/bin/activate_this.py'
exec(open(activate_this).read())

import sys
import os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, path)

from app import app as application