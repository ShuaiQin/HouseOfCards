from google.appengine.api import users
from google.appengine.api import urlfetch
import webapp2

import config.config as cfg

import json, random


class ExplorePage(webapp2.RequestHandler):
    def get(self):

        template_value = {}

        user = users.get_current_user()
        if user:
            template_value['myself'] = user.email()
            template_value['logout_url'] = cfg.LOG_OUT_URL
            template_value['sign'] = True
        else:
            template_value['login_url'] = cfg.LOG_IN_URL
            template_value['sign'] = False
        template_value['houses'] = self.rpc()
        sort_method = self.request.get('sort-method')
        if sort_method == 'sort-view':
            template_value['houses'].sort(key=lambda d: -d['view'])
        elif sort_method == 'sort-sub':
            template_value['houses'].sort(key=lambda d: -d['num_of_subed'])
        else:
            tmp = template_value['houses']
            template_value['houses'] = random.sample(tmp, len(tmp))

        cat_count = self.cat_rpc()
        sort_cat_list = sorted(cat_count.items(), key=lambda x: (-x[1], x[0]))
        template_value['categories_order'] = sort_cat_list
        template_value['categories'] = cfg.categories_dict
        template_value['sort_method'] = sort_method

        template = cfg.JINJA_ENVIRONMENT.get_template("explore.html")
        self.response.write(template.render(template_value))


    def rpc(self):
        rpc = urlfetch.create_rpc()
        url = cfg.SERVICE_URL + "/service-viewallhouses"
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        data = json.loads(response.content)
        return data["all_house_list"]

    def cat_rpc(self):
        rpc = urlfetch.create_rpc()
        url = cfg.SERVICE_URL + "/service-gethousenumberforCato"
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        data = json.loads(response.content)
        return data['Catogory']
