import os
import jinja2
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)

LOG_OUT_URL = users.create_logout_url("/")
LOG_IN_URL = users.create_login_url("/")
SERVICE_URL = "https://manage-dot-pigeoncard.appspot.com"