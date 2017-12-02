from google.appengine.api import users
from google.appengine.api import urlfetch
import webapp2

import config.config as cfg

import json
import urllib


class SearchPage(webapp2.RequestHandler):
    def get(self):

        query = self.request.get('query')
        template_value = {}

        user = users.get_current_user()
        if user:
            template_value['myself'] = user.email()
            template_value['logout_url'] = cfg.LOG_OUT_URL
            template_value['sign'] = True
        else:
            template_value['login_url'] = cfg.LOG_IN_URL
            template_value['sign'] = False
        print type(query)
        template_value['houses'] = self.rpc(query)

        if template_value['houses']:
            template = cfg.JINJA_ENVIRONMENT.get_template("search.html")
            self.response.write(template.render(template_value))
        else:
            self.redirect("/explore")

    def rpc(self, query):
        rpc = urlfetch.create_rpc()
        data = {
            "search_string": query
        }
        url = cfg.SERVICE_URL + "/service-searchhouse?" + urllib.urlencode(data)
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        if response.status_code == 200:
            data = json.loads(response.content)
            return data["search_house_list"]
        else:
            return None
