#this file include handlers that manage user issues

import json

import webapp2
import ops

class AddIssueServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get("user_id")
        house_name = self.request.get("house_name")
        card_key = self.request.get("card_key")
        content = self.request.get("content")
        ops.add_issue(user_id, house_name, card_key, content)

class ShowAllIssuesServiceHandler(webapp2.RequestHandler):
    def get(self):
        house_name = self.request.get("house_name")
        issue_list = ops.show_all_issues(house_name)
        return_info = {
            'issue_list': issue_list
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))

class ResolveIssueServiceHandler(webapp2.RequestHandler):
    def get(self):
        house_name = self.request.get("house_name")
        user_id = self.request.get("user_id")
        date = self.request.get("date")
        ops.resolve_issue(house_name, user_id, date)
