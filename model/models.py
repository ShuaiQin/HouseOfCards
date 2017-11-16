from google.appengine.ext import ndb

class Pigeon(ndb.Model):     # key is user id
    pigeon_id = ndb.StringProperty()  # user's id

class House(ndb.Model):      # key is name of house
    cover_url = ndb.StringProperty()
    name = ndb.StringProperty()
    category = ndb.StringProperty()

class Card(ndb.Model):      # key is name of card
    key = ndb.StringProperty()
    value = ndb.StringProperty()

class Subscription(ndb.Model):
    pigeon_key = ndb.KeyProperty(kind="Pigeon")
    house_key = ndb.KeyProperty(kind="House")
    # 日程

class Progress(ndb.Model):
    pigeon_key = ndb.KeyProperty(kind="Pigeon")
    card_key = ndb.KeyProperty(kind="Card")
    # 熟练度

class PullRequest(ndb.Model):
    pigeon_key = ndb.KeyProperty(kind="Pigeon")
    house_key = ndb.KeyProperty(kind="House")
    card_key = ndb.KeyProperty(kind="Card")
    new_key = ndb.StringProperty()
    new_value = ndb.StringProperty()
    mode = ndb.StringProperty()

class Issue(ndb.Model):    #commont for a card
    pigeon_key = ndb.KeyProperty(kind="Pigeon")
    card_key = ndb.KeyProperty(kind="Card")
    comment = ndb.StringProperty()
    date = ndb.DateTimeProperty()

class Post(ndb.Model):   #comment for a house
    pigeon_key = ndb.KeyProperty(kind="Pigeon")
    house_key = ndb.KeyProperty(kind="House")
    content = ndb.StringProperty()
    number = ndb.IntegerProperty()
