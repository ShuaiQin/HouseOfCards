from models import *
from google.appengine.ext import ndb

'''
account = Account(username='Sandy', userid=1234, email='sandy@example.com')
account.key =  ndb.Key('Revision', '1', parent=ndb.Key(
    'Account', 'sandy@example.com', 'Message', 123))
account.put()
'''


def create_pigeon(pigeon_id):
    pigeon = Pigeon(pigeon_id = pigeon_id)
    pigeon.key = ndb.Key(Pigeon,pigeon_id)
    pigeon.put()

def create_house(cover_url,name,category,pigeon_id):
    house = House( cover_url=cover_url,name=name,category=category )
    house.key = ndb.key(House,name,parent = ndb.Key(Pigeon,pigeon_id) )
    house.put()

def create_card(key,value,house_name):
    house_list = House.query(name=house_name).fetch()
    if house_list:
        card = Card(key=key, value=value)
        house = house_list[0]
        card.key = ndb.Key(Card,key,parent = house.key)
        card.put()
    return


