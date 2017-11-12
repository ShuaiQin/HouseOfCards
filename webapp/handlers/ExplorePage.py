from google.appengine.api import users
import webapp2

import config.config as cfg


class ExplorePage(webapp2.RequestHandler):
    def get(self):

        template_value = {}

        user = users.get_current_user()
        if user:
            template_value['pigeon'] = user.email()
            template_value['logout_url'] = cfg.LOG_OUT_URL
            template_value['sign'] = True
        else:
            template_value['login_url'] = cfg.LOG_IN_URL
            template_value['sign'] = False

        template = cfg.JINJA_ENVIRONMENT.get_template("explore.html")
        self.response.write(template.render(template_value))
