#this file include handlers that manage user posts

import webapp2
import ops

class AddNewPostServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get("user_id")
        house_name = self.request.get("house_name")
        content = self.request.get("content")
        ops.add_post(house_name, user_id, content)


