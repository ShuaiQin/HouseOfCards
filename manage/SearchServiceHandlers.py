#this file include handlers that show houses or cards

import json
import ops
import webapp2
import re

class SearchHouseServiceHandler(webapp2.RequestHandler):
    def get(self):
        search_string = self.request.get("search_string")

        all_house_list = ops.get_all_house()
        search_house_list = []
        if (search_string != ""):
            for house in all_house_list:
                if (re.match(".*"+search_string, house['house_name'])):
                    search_house_list.append(house)
        
        return_info = {
            'search_house_list': search_house_list
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class SearchCardServiceHandler(webapp2.RequestHandler):
    def get(self):
        house_name = self.request.get('house_name')
        search_string = self.request.get("search_string")

        search_card_list= []
        all_card_list = ops.get_single_house(house_name)
        if (search_string!= ""):
            for card in all_card_list:
                if (re.match(".*"+search_string, card['key'])):
                    search_card_list.append(card)

        return_info = {
            'search_card_list': search_card_list
        }
        self.response.write(json.dumps(return_info))

