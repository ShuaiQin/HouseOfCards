from google.appengine.api import users
import webapp2

import config.config as cfg


class StudyPage(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        if user:
            template_value = {}
            template_value['pigeon'] = user.email()
            template_value['logout_url'] = cfg.LOG_OUT_URL
            template_value['sign'] = True

            template = cfg.JINJA_ENVIRONMENT.get_template("study.html")
            self.response.write(template.render(template_value))
        else:
            self.redirect("/login")
