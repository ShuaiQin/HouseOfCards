from google.appengine.ext import ndb

from models import *


'''
account = Account(username='Sandy', userid=1234, email='sandy@example.com')
account.key =  ndb.Key('Revision', '1', parent=ndb.Key(
    'Account', 'sandy@example.com', 'Message', 123))
account.put()
'''

def pigeon_exists(pigeon_id):
    pigeon_list = Pigeon.query(pigeon_id = pigeon_id).fetch()
    if pigeon_list:
        return True
    else:
        return False

def create_pigeon(pigeon_id):
    pigeon = Pigeon(pigeon_id = pigeon_id)
    pigeon.key = ndb.Key(Pigeon,pigeon_id)
    pigeon.put()

def create_house(cover_url,name,category,pigeon_id):
    house = House( cover_url=cover_url,name=name,category=category )
    house.key = ndb.key(House,name,parent = ndb.Key(Pigeon,pigeon_id) )
    house.put()

def house_exists(house_name):
    house_list = House.query(name=house_name).fetch()
    if(house_list):
        return True
    else:
        return False

def add_card(key,value,house_name):
    house_list = House.query(name=house_name).fetch()
    if house_list:
        card = Card(key=key, value=value)
        house = house_list[0]
        card.key = ndb.Key(Card,key,parent = house.key)
        card.put()
    return

def get_all_cards(house_name):
    house_list = House.query(name=house_name).fetch()
    if house_list:
        house = house_list[0]
        return Card.query(ancestor=house.key).fetch()
    return

def get_self_house(pigeon_id):
    house_list = House.query(ancestor=ndb.Key(Pigeon,pigeon_id)).fetch()
    return map(lambda s: {"house_name": s.name, "cover_url": s.cover_url,
                          "category": s.category , "view": s.view,
                          "num_of_subed": s.num_of_subed},
               house_list)




def create_subscription(pigeon_id, house_name,num_per_day):
    pigeon_key = ndb.Key(Pigeon,pigeon_id)
    house_list = House.query(name=house_name).fetch()
    house_key = house_list[0].key
    subscription = Subscription( pigeon_key=pigeon_key, house_key=house_key,num_per_day=num_per_day )
    subscription.put()

def delete_subscription(pigeon_id, house_name):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    house_list = House.query(name=house_name).fetch()
    house_key = house_list[0].key
    sublist = Subscription.query( pigeon_key=pigeon_key,house_key=house_key ).fetch()
    if sublist:
        sublist[0].key.delete()
    else:
        return

def get_sub_house(pigeon_id):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    house_list = House.query( pigeon_key=pigeon_key ).fetch()
    return map(lambda s: {"house_name": s.name, "cover_url": s.cover_url,
                          "category": s.category , "view": s.view,
                          "num_of_subed": s.num_of_subed},
               house_list)

def get_all_house():
    house_list = House.query().fetch()
    return map(lambda s: {"house_name": s.name, "cover_url": s.cover_url,
                          "category": s.category , "view": s.view,
                          "num_of_subed": s.num_of_subed},
               house_list)

def get_single_house(house_name):
    house_list = House.query(name = house_name).fetch()
    if house_list:
        return house_list[0]
    else:
        return

def get_house_owner(house_name):
    house_list = House.query(name = house_name).fetch()
    if house_list:
        house = house_list[0]
        id = house.key().parent().get().pigeon_id
    return id



def is_subscribed(house_name, pigeon_id):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    house_list = House.query(name=house_name).fetch()
    house_key = house_list[0].key
    sub_list = Subscription.query( pigeon_key=pigeon_key,house_key=house_key ).fetch()
    if sub_list:
        return True
    else:
        return False

def remove_house(house_name):
    house_list = House.query(name=house_name).fetch()
    if house_list:
        house_list[0].key.delete()
    return

def remove_all_sub(house_name):
    house_list = House.query(name=house_name).fetch()
    house_key = house_list[0].key
    sub_list = Subscription.query(house_key=house_key).fetch()
    for sub in sub_list:
        sub.key.delete()
    return

def card_exists(house_name, card_key):
    house_list = House.query(name=house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key, parent=house_key)
    card = card_key.get()
    if card:
        return True
    else:
        return False

def remove_card(house_name, card_key):
    house_list = House.query(name=house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key, parent=house_key)
    card_key.delete()
    return

def edit_card_key (house_name, card_key, new_card_key):
    house_list = House.query(name=house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key, parent=house_key)
    card = card_key.get()
    value = card.value

    remove_card(house_name, card_key)
    add_card(card_key, value, house_name)
    return

def edit_card_content (house_name, card_key, new_card_content):
    house_list = House.query(name=house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key, parent=house_key)
    card = card_key.get()

    card.value = new_card_content
    card.put()
    return

# def send_pull_request(user_id, house_name, mode, card_key, new_key, new_value)





