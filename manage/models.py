from google.appengine.ext import ndb


class Pigeon(ndb.Model):     # key is user id
    pigeon_id = ndb.StringProperty()  # user's id

class House(ndb.Model):      # key is name of house
    cover_url = ndb.StringProperty()
    name = ndb.StringProperty()
    category = ndb.StringProperty()
    view = ndb.IntegerProperty()
    num_of_subed = ndb.IntegerProperty()

class Card(ndb.Model):      # key is name of card
    card_key = ndb.StringProperty()
    value = ndb.StringProperty()

class Subscription(ndb.Model):
    pigeon_key = ndb.KeyProperty(kind="Pigeon")
    house_key = ndb.KeyProperty(kind="House")
    num_per_day = ndb.IntegerProperty()

class Progress(ndb.Model):
    pigeon_key = ndb.KeyProperty(kind="Pigeon")
    card_key = ndb.KeyProperty(kind="Card")
    familiar_factor = ndb.FloatProperty()
    learn_factor = ndb.IntegerProperty()

class PullRequest(ndb.Model):
    pigeon_key = ndb.KeyProperty(kind="Pigeon")
    house_key = ndb.KeyProperty(kind="House")
    card_key = ndb.KeyProperty(kind="Card")
    new_key = ndb.StringProperty()
    new_value = ndb.StringProperty()
    mode = ndb.StringProperty()  # query,update,insert,delete
    date = ndb.DateTimeProperty(auto_now_add=True)


class Issue(ndb.Model):    #commont for a card
    pigeon_key = ndb.KeyProperty(kind="Pigeon")
    house_key = ndb.KeyProperty(kind="House")
    card_key = ndb.KeyProperty(kind="Card")
    comment = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Post(ndb.Model):   #comment for a house
    pigeon_key = ndb.KeyProperty(kind="Pigeon")
    house_key = ndb.KeyProperty(kind="House")
    content = ndb.StringProperty()
    number = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
