from google.appengine.api import users
import webapp2

import config.config as cfg


class LoginPage(webapp2.RequestHandler):
    def get(self):
        login_url = users.create_login_url("/")

        template_values = {
            "login_url": login_url
        }

        template = cfg.JINJA_ENVIRONMENT.get_template("login.html")
        self.response.write(template.render(template_values))
