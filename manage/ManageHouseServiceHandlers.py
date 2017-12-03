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
                ops.remove_all_sub(str(house))
                ops.remove_house(str(house))

class GetPostForUserHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        post_list = []
        house_list = ops.get_self_house(user_id)   # list of dic
        for house in house_list:
            post_list = post_list + ops.get_all_post( house['house_name'] )    # house is a dic

        sorted_list = sorted(post_list, key=lambda h: h['date'], reverse=True)
        if len(sorted_list)>5:
            return_info = {
                'posts': sorted_list[0:5]
            }
            self.response.write(json.dumps(return_info))
        else:
            return_info = {
                'posts': sorted_list
            }
            self.response.write(json.dumps(return_info))

class GetHouseNumberForCato(webapp2.RequestHandler):
    def get(self):
        categories_key = [
            "art", "geo", "his",
            "lan", "lit", "phi",
            "the", "ant", "eco",
            "law", "pol", "psy",
            "soc", "bio", "che",
            "ear", "spa", "phy",
            "com", "mat", "sta",
            "eng", "hea", "oth"
        ]
        res = {}
        for key in categories_key:
            res[key] = len(ops.get_category(key))

        return_info = {
            'Catogory': res
        }
        self.response.write(json.dumps(return_info))