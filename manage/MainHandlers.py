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


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('manage: Hello world!')


class ManageProfileServiceHandler(webapp2.RequestHandler):
    def get(self):
        pass


service = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/service-manageprofile',ManageProfileServiceHandler),
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
