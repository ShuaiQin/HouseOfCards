#this file include handlers that manage user pull requests

import json
import ops
import webapp2


class CreatePullRequestServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get("user_id")
        house_name = self.request.get("house_name")
        mode = self.request.get("mode")
        card_key = self.request.get("card_key")
        new_key = self.request.get("new_key")
        new_value = self.request.get("new_value")
        if mode=="add" or ops.card_exists(house_name,card_key):
            ops.send_pull_request(user_id, house_name, mode, card_key, new_key, new_value)
            return_info = {
                'status': True,
            }
            self.response.write(json.dumps(return_info))
        else:
            return_info = {
                'status': False,
            }
            self.response.write(json.dumps(return_info))


class ShowAllPullRequestServiceHandler(webapp2.RequestHandler):
    def get(self):
        house_name = self.request.get("house_name")
        pull_request_list= ops.show_all_pull_request(house_name)
        return_info = {
            'pull_request_list': pull_request_list
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class ResolvePullRequestServiceHandler(webapp2.RequestHandler):
    def get(self):
        house_name = self.request.get("house_name")
        user_id = self.request.get("user_id")
        date = self.request.get("date")
        decision = self.request.get("decision")
        if (decision == "approve"):
            ops.approve_pull_request(house_name, user_id, date)
        elif(decision == "reject"):
            ops.reject_pull_request(house_name, user_id, date)
