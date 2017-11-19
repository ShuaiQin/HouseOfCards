from google.appengine.api import users
import webapp2

import config.config as cfg


class PigeonPage(webapp2.RequestHandler):
    def get(self, id):

        user = users.get_current_user()
        if user:
            template_value = {}
            template_value['myself'] = user.email()
            template_value['logout_url'] = cfg.LOG_OUT_URL
            template_value['sign'] = True
            template_value['pigeon'] = id

            template = cfg.JINJA_ENVIRONMENT.get_template("pigeon.html")
            self.response.write(template.render(template_value))
        else:
            self.redirect("/login")
