#this file include handler that manage user houses

import webapp2
import random
import json
import ops

class CreateHouseServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        house_name = self.request.get('house_name')
        category = self.request.get('category')
        cover_url = self.request.get('cover_url')

        if cover_url == "":
            num = int(random.random() * 5)
            cover_url = "https://storage.googleapis.com/pigeonhole-apt.appspot.com/" \
                        "defaultcoverimagefolderyaohuazhao/" + str(num) + ".jpg"
        #self.response.write('manage: Hello world!')
        if ops.house_exists(house_name):
            return_info = {
                'status': False,
            }
            self.response.write(json.dumps(return_info))
            return

        ops.create_house(user_id, house_name, cover_url, category)
        return_info = {
            'status': True,
        }
        self.response.write(json.dumps(return_info))

class RemoveHouseServiceHandler(webapp2.RequestHandler):
    def get(self):
        delete_house_string = self.request.get('delete_house_string')
        delete_house_list = delete_house_string.split(',')

        for house in delete_house_list:
            if ops.house_exists(house):
                ops.remove_house(str(house))
                ops.remove_all_sub(str(house))

