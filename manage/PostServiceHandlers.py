#this file include handlers that manage user posts

import webapp2
import ops
import json

class AddNewPostServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get("user_id")
        house_name = self.request.get("house_name")
        content = self.request.get("content")
        ops.add_post(house_name, user_id, content)


class GetPostServiceHandler(webapp2.RequestHandler):
    def get(self):
        house_name = self.request.get("house_name")
        posts = ops.get_all_post(house_name)
        return_info = {
            'posts': posts,

        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))

