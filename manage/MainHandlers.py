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
import json

import webapp2
from IssuesServiceHandlers import AddIssueServiceHandler
from IssuesServiceHandlers import ResolveIssueServiceHandler
from IssuesServiceHandlers import ShowAllIssuesServiceHandler
from ManageCardServiceHandlers import AddCardServiceHandler
from ManageCardServiceHandlers import EditCardServiceHandler
from ManageCardServiceHandlers import RemoveCardServiceHandler
from ManageHouseServiceHandlers import CreateHouseServiceHandler
from ManageHouseServiceHandlers import RemoveHouseServiceHandler
from ManageHouseServiceHandlers import GetPostForUserHandler
from ManageHouseServiceHandlers import GetHouseNumberForCato
from ManageSubscriptionServiceHandlers import CreateSubscriptionServiceHandler
from ManageSubscriptionServiceHandlers import DeleteSubscriptionServiceHandler
from ManageSubscriptionServiceHandlers import CheckSubscriptionServiceHandler
from PostServiceHandlers import AddNewPostServiceHandler
from PostServiceHandlers import GetPostServiceHandler
from PullRequestsServiceHandlers import CreatePullRequestServiceHandler
from PullRequestsServiceHandlers import ResolvePullRequestServiceHandler
from PullRequestsServiceHandlers import ShowAllPullRequestServiceHandler
from TrendingServiceHandlers import GetCategoryServiceHandler
from TrendingServiceHandlers import GetTrendingSubServiceHandler
from TrendingServiceHandlers import GetTrendingViewServiceHandler
from ViewHouseServiceHandler import ViewAllHousesServiceHandler
from ViewHouseServiceHandler import ViewSingleHouseServiceHandler
from SearchServiceHandlers import SearchHouseServiceHandler
from SearchServiceHandlers import SearchCardServiceHandler

import ops
import study
import random

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('manage: Hello world!')


class ManageProfileServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        owned_house_list = []
        subed_house_list = []

        if not ops.pigeon_exists(user_id):  # if no such user, return two empty lists
            avater_list = ['bee.png','bull.png','dolphin.png','duck.png','falcon.png','pigeon.png','rabbit.png','unicorn.png']
            ops.create_pigeon(user_id,avater_list[random.randint(0,7)])
        else:
            owned_house_list = ops.get_self_house(user_id)
            subed_house_list = ops.get_sub_house(user_id)

        avatar = ops.get_avatar(user_id)
        return_info = {
            'owned_house_list': owned_house_list,
            'subed_house_list': subed_house_list,
            'avatar':avatar
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
    ('/service-getpost', GetPostServiceHandler),
    ('/service-trendingsub',GetTrendingSubServiceHandler),
    ('/service-trendingview',GetTrendingViewServiceHandler),
    ('/service-category',GetCategoryServiceHandler),
    ('/service-checksubscription', CheckSubscriptionServiceHandler),
    ('/service-searchhouse',SearchHouseServiceHandler),
    ('/service-searchcard',SearchCardServiceHandler),
    ('/service-getpostforuser', GetPostForUserHandler),
    ('/service-gethousenumberforCato', GetHouseNumberForCato),
    #
    ('/getmultiplequiz', study.GetMultipleQuizHandler),
    ('/gettruefalsequiz', study.GetTrueFalseQuizHandler),
    ('/makeschedule', study.MakeScheduleHandler),
    ('/showprogress', study.ShowProgressHandler),
    ('/gettodaytask', study.GetTodayTaskHandler),
    ('/setschedule', study.SetScheduleHandler),
    ('/checkschedulefinish', study.CheckScheduleFinishHandler),
    ('/checkstudyornot', study.CheckStudyOrNotHandler),
    ('/getschedule', study.GetScheduleHandler),
    ('/fortest', study.ForTest),
    ('/gethousesize', study.GetHouseSizeHandler)
], debug=True)
