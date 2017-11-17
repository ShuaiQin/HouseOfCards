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
import webapp2
import model.ops
import json
from manage.ManageHouseServiceHandlers import CreateHouseServiceHandler
from manage.ManageHouseServiceHandlers import RemoveHouseServiceHandler
from manage.ManageCardServiceHandlers import AddCardServiceHandler
from manage.ManageCardServiceHandlers import RemoveCardServiceHandler
from manage.ManageCardServiceHandlers import EditCardServiceHandler
from manage.ManageSubscriptionServiceHandlers import CreateSubscriptionServiceHandler
from manage.ManageSubscriptionServiceHandlers import DeleteSubscriptionServiceHandler
from manage.PullRequestsServiceHandlers import CreatePullRequestServiceHandler
from manage.PullRequestsServiceHandlers import ShowAllPullRequestServiceHandler
from manage.PullRequestsServiceHandlers import ResolvePullRequestServiceHandler
from manage.IssuesServiceHandlers import AddIssueServiceHandler
from manage.IssuesServiceHandlers import ShowAllIssuesServiceHandler
from manage.IssuesServiceHandlers import ResolveIssueServiceHandler
from manage.PostServiceHandlers import AddNewPostServiceHandler
from manage.TrendingServiceHandlers import GetTrendingSubServiceHandler
from manage.TrendingServiceHandlers import GetTrendingViewServiceHandler
from manage.ViewHouseServiceHandler import ViewAllHousesServiceHandler
from manage.ViewHouseServiceHandler import ViewSingleHouseServiceHandler


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('manage: Hello world!')


class ManageProfileServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        if not ops.pigeon_exists(user_id):  # if no such user, return two empty lists
            ops.create_pigeon(user_id)
            owned_house_list = []
            subed_house_list = []
        else:
            owned_house_list = ops.get_self_house(user_id)
            subed_house_list = ops.get_sub_house(user_id)
        return_info = {
            'owned_house_list': owned_house_list,
            'subed_house_list': subed_house_list
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))



service = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/service-manageprofile',ManageProfileServiceHandler),
    ('/service-viewallhouses',ViewAllHousesServiceHandler),
    ('/service-viewsinglehouse',ViewSingleHouseServiceHandler),
    ('/service-createhouse',CreateHouseServiceHandler),
    ('/service-removehouse',RemoveHouseServiceHandler),
    ('/service-addcard',AddCardServiceHandler),
    ('/service-removecard',RemoveCardServiceHandler),
    ('/service-editcard',EditCardServiceHandler),
    ('/service-createsubscription',CreateSubscriptionServiceHandler),
    ('/service-deletesubscription',DeleteSubscriptionServiceHandler),
    ('/service-createpullrequest',CreatePullRequestServiceHandler),
    ('/service-showpullrequest',ShowAllPullRequestServiceHandler),
    ('/service-resolvepullrequest',ResolvePullRequestServiceHandler),
    ('/service-addissue',AddIssueServiceHandler),
    ('/service-showissues',ShowAllIssuesServiceHandler),
    ('/service-resolveissue',ResolveIssueServiceHandler),
    ('/service-addpost',AddNewPostServiceHandler),
    ('/service-trendingsub',GetTrendingSubServiceHandler),
    ('/service-trendingview',GetTrendingViewServiceHandler)
], debug=True)
