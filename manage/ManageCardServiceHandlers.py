#this file include handlers that manage user cards

import webapp2
import json
import model.ops

class AddCardServiceHandler(webapp2.RequestHandler):
    def get(self):
        house_name = self.response.get('house_name')
        card_key = self.response.get('card_key')
        card_value = self.response.get('card_value')

        if ops.card_exists(house_name, card_key):
            return_info = {
                'status': False,
            }
            self.response.write(json.dumps(return_info))
            return

        ops.add_card(house_name, card_key, card_value)
        return_info = {
            'status': True,
        }
        self.response.write(json.dumps(return_info))


class RemoveCardServiceHandler(webapp2.RequestHandler):
    def get(self):
        house_name = self.response.get('house_name')
        delete_card_string = self.request.get('delete_card_string')
        delete_card_list = delete_card_string.split(',')

        for card in delete_card_list:
            if ops.card_exists(card):
                ops.remove_card(house_name, str(card))
                #ops.remove_all_sub(str(card))

class EditCardServiceHandler(webapp2.RequestHandler):
    def get(self):
        house_name = self.response.get('house_name')
        card_key = self.response.get('card_key')
        mode = self.response.get("mode")
        updated = self.response.get('updated')

        if not ops.card_exists(house_name, card_key):
            return_info = {
                'status': False,
            }
            self.response.write(json.dumps(return_info))
            return

        if (mode == "key"):
            ops.edit_card_key(house_name,card_key,updated)
        elif (mode== "content"):
            ops.edit_card_content(house_name, card_key, updated)

        return_info = {
            'status': True,
        }
        self.response.write(json.dumps(return_info))