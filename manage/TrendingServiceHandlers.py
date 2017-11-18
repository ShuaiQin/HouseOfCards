#this file include handlers that manage trending

import webapp2
import json
import model.ops

class GetTrendingSubServiceHandler(webapp2.RequestHandler):
    def get(self):
        trending_list_sub = ops.get_trending_subscription()
        return_info = {
            'trending_list_sub': trending_list_sub
        }
        self.response.write(json.dumps(return_info))

class GetTrendingViewServiceHandler(webapp2.RequestHandler):
    def get(self):
        trending_list_view = ops.get_trending_view()
        return_info = {
            'trending_list_view': trending_list_view
        }
        self.response.write(json.dumps(return_info))

class GetCategoryServiceHandler(webapp2.RequestHandler):
    def get(self):
        category_list = ops.get_catogory()
        return_info = {
            'category_list': category_list
        }
        self.response.write(json.dumps(return_info))