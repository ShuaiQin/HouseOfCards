from google.appengine.api import users
import webapp2

import config.config as cfg


class HousePage(webapp2.RequestHandler):
    def get(self, name):

        user = users.get_current_user()
        if user:
            template_value = {}
            template_value['myself'] = user.email()
            template_value['logout_url'] = cfg.LOG_OUT_URL
            template_value['sign'] = True
            template_value['house'] = name

            template = cfg.JINJA_ENVIRONMENT.get_template("house.html")
            self.response.write(template.render(template_value))
        else:
            self.redirect("/login")