import os
import jinja2
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)

LOG_OUT_URL = users.create_logout_url("/")
LOG_IN_URL = users.create_login_url("/")
SERVICE_URL = "https://manage-dot-pigeoncard.appspot.com"

categories = [
    "Arts", "Geography", "History",
    "Languages", "Literature","Philosophy",
    "Theology", "Anthropology", "Economics",
    "Law", "Politics", "Psychology",
    "Sociology", "Biology", "Chemistry",
    "Earth Sciences", "Space Science", "Physics",
    "Computer Sciences", "Mathematics", "Statistics",
    "Engineering", "Health sciences", "Others"
]

categories_key = [
    "art", "geo", "his",
    "lan", "lit", "phi",
    "the", "ant", "eco",
    "law", "pol", "psy",
    "soc", "bio", "che",
    "ear", "spa", "phy",
    "com", "mat", "sta",
    "eng", "hea", "oth"
]

categories_dict = dict(zip(categories_key, categories))
