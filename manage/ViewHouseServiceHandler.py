#this file include handlers that show houses or cards

import json
import ops
import webapp2


class ViewAllHousesServiceHandler(webapp2.RequestHandler):
    def get(self):
        all_house_list = ops.get_all_house()
        return_info = {
            'all_house_list': all_house_list
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class ViewSingleHouseServiceHandler(webapp2.RequestHandler):
    def get(self):
        house_name = self.request.get('house_name')
        #page_range = self.request.get('page_range')
        user_id = self.request.get('user_id')

        # get all cards in house
        all_card_list = ops.get_single_house(house_name)

        owner = ops.get_house_owner(house_name)
        is_owned = (owner == user_id)

        is_subed = ops.is_subscribed(house_name, user_id)

        return_info = {
            #'page_range': min(int(page_range), len(all_pict_list)),
            'card_list': all_card_list,
            'is_subed': is_subed,
            'is_owned': is_owned
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))

