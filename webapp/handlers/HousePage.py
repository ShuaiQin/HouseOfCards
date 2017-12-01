from google.appengine.api import users
from google.appengine.api import urlfetch
import webapp2

import config.config as cfg
import json
import urllib

class HousePage(webapp2.RequestHandler):
    def get(self, name):

        user = users.get_current_user()
        if user:
            template_value = {}
            template_value['myself'] = user.email()
            template_value['logout_url'] = cfg.LOG_OUT_URL
            template_value['sign'] = True
            template_value['house'] = name

            data = self.rpc(user.email(), name)
            if data:
                template_value['cards'] = data['card_list']
                template_value['is_owned'] = data['is_owned']
                template_value['is_subed'] = data['is_subed']
                template_value['house_info'] = data['house_info']

            data = self.pr_rpc(name)
            if data:
                template_value['prs'] = data

            template = cfg.JINJA_ENVIRONMENT.get_template("house.html")
            self.response.write(template.render(template_value))
        else:
            self.redirect("/login")

    def rpc(self, user_id, house_name):
        rpc = urlfetch.create_rpc()
        request = {
            'user_id': user_id,
            'house_name': house_name
        }
        url = cfg.SERVICE_URL + "/service-viewsinglehouse?" + urllib.urlencode(request)
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        data = json.loads(response.content)
        return data

    def pr_rpc(self, house_name):
        rpc = urlfetch.create_rpc()
        request = {
            'house_name': house_name
        }
        url = cfg.SERVICE_URL + "/service-showpullrequest?" + urllib.urlencode(request)
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        data = json.loads(response.content)
        return data["pull_request_list"]