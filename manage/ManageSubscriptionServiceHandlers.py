#this file include handlers that manage subscriptions

import webapp2
import ops
import json


class CreateSubscriptionServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        house_name = self.request.get('house_name')
        if not ops.is_subscribed(house_name, user_id):
            ops.create_subscription(user_id, house_name)


class DeleteSubscriptionServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        delete_sub_string = self.request.get('delete_sub_string')
        delete_sub_list = delete_sub_string.split(',')
        for house in delete_sub_list:
            if ops.is_subscribed(house, user_id):
                ops.delete_subscription(user_id, str(house))


class CheckSubscriptionServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        house_name = self.request.get('house_name')
        if ops.is_subscribed(house_name, user_id):
            is_subscribed = True
        else:
            is_subscribed = False
        return_info = {
            'is_subscribed': is_subscribed
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))
