from google.appengine.api import users
from google.appengine.api import urlfetch
import webapp2

import config.config as cfg
import json, urllib

class CreatePage(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        print 1
        if user:
            template_value = {}
            template_value['myself'] = user.email()
            template_value['logout_url'] = cfg.LOG_OUT_URL
            template_value['sign'] = True
            template_value['categories'] = cfg.categories_dict

            template = cfg.JINJA_ENVIRONMENT.get_template("create.html")
            self.response.write(template.render(template_value))
        else:
            self.redirect("/login")

    def post(self):
        current_user = users.get_current_user().email()
        name = self.request.get('name')
        cover_url = self.request.get('cover_url')
        category = self.request.get('category')

        form_fields = {
            'user_id': current_user,
            'house_name': name,
            'cover_url': cover_url,
            'category': category
        }
        print form_fields
        form_data = urllib.urlencode(form_fields)
        print form_data
        rpc = urlfetch.create_rpc()
        url = cfg.SERVICE_URL + "/service-createhouse?" + form_data
        print url
        response = urlfetch.make_fetch_call(rpc, url)
        result = rpc.get_result()
        print result.content
        data = json.loads(result.content)
        if data['status']:
            self.redirect('/house/' + name)
        else:
            self.redirect('/error')
