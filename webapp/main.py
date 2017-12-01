#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.api import users

import config.config as cfg

from handlers.LoginPage import *
from handlers.ExplorePage import *
from handlers.StudyPage import *
from handlers.PigeonPage import *
from handlers.HousePage import *
from handlers.CreatePage import *
from handlers.FormPage import *

class MainHandler(webapp2.RequestHandler):
    def get(self):

        template_value = {}

        user = users.get_current_user()
        if user:
            template_value['myself'] = user.email()
            template_value['logout_url'] = cfg.LOG_OUT_URL
            template_value['sign'] = True
            data = self.rpc(user.email())
            template_value['owned_houses'] = data['owned_house_list'][:4]
            template_value['subed_houses'] = data['subed_house_list'][:4]

        else:
            template_value['login_url'] = cfg.LOG_IN_URL
            template_value['sign'] = False

        template = cfg.JINJA_ENVIRONMENT.get_template("index.html")
        self.response.write(template.render(template_value))

    def rpc(self, user_id):
        rpc = urlfetch.create_rpc()
        request = {}
        request['user_id'] = user_id
        url = cfg.SERVICE_URL + "/service-manageprofile?" + urllib.urlencode(request)
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        data = json.loads(response.content)
        return data

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginPage),
    ('/explore', ExplorePage),
    ('/study', StudyPage),
    ('/pigeon/(\w+)', PigeonPage, 'id'),
    ('/house/(\w+)', HousePage, 'name'),
    ('/create', CreatePage),
    ('/create-pr/(\w+)', PrFormHandler, 'name'),
    ('/resolve-pr/(\w+)/(\w+)/(\w+)', PrResolveHandler, ('name', 'date', 'decision'))
], debug=True)
