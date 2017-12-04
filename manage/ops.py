from google.appengine.ext import ndb

from models import Pigeon, House, Card, Subscription, Progress, PullRequest, Issue, Post


'''
account = Account(username='Sandy', userid=1234, email='sandy@example.com')
account.key =  ndb.Key('Revision', '1', parent=ndb.Key(
    'Account', 'sandy@example.com', 'Message', 123))
account.put()
'''

def pigeon_exists(pigeon_id):
    pigeon_list = Pigeon.query(Pigeon.pigeon_id == pigeon_id).fetch()
    if pigeon_list:
        return True
    else:
        return False

def create_pigeon(pigeon_id, avatar):
    pigeon = Pigeon(pigeon_id = pigeon_id, avatar = avatar)
    pigeon.key = ndb.Key(Pigeon,pigeon_id)
    pigeon.put()

def get_avatar( pigeon_id ):
    pigeon_list = Pigeon.query(Pigeon.pigeon_id == pigeon_id).fetch()
    if pigeon_list:
        return pigeon_list[0].avatar
    else:
        return


def create_house(pigeon_id,name,cover_url,category):
    house = House( cover_url=cover_url,name=name,category=category,view=1,num_of_subed=0 )
    house.key = ndb.Key(House,name,parent = ndb.Key(Pigeon,pigeon_id) )
    house.put()

def house_exists(house_name):
    house_list = House.query(House.name==house_name).fetch()
    if(house_list):
        return True
    else:
        return False

def add_card(house_name,key,value):
    house_list = House.query(House.name==house_name).fetch()
    if house_list:
        card = Card( card_key=key, value=value )
        house = house_list[0]
        card.key = ndb.Key(Card,key,parent = house.key)
        card.put()
    return

def _get_all_cards(house_name):
    house_list = House.query(House.name==house_name).fetch()
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


def create_subscription(pigeon_id, house_name):
    pigeon_key = ndb.Key(Pigeon,pigeon_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    subscription = Subscription( pigeon_key=pigeon_key, house_key=house_key,num_per_day=0 )
    subscription.put()

    card_list = Card.query(ancestor=house_key).fetch()
    for card in card_list:
        _initailize_progress(pigeon_key,card.key)

    house = house_list[0]
    house.num_of_subed = house.num_of_subed+1
    house.put()
    return

def delete_subscription(pigeon_id, house_name):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    house_list = House.query(House.name==house_name).fetch()
    house = house_list[0]
    house.num_of_subed = house.num_of_subed -1
    house.put()
    house_key = house.key
    sublist = Subscription.query( Subscription.pigeon_key==pigeon_key,Subscription.house_key==house_key ).fetch()
    if sublist:
        sub = sublist[0]
        sub.key.delete()
        card_list = _get_all_cards(house_name)
        for card in card_list:
            _delete_progress(pigeon_key, card.key)
        return
    else:
        return

def get_sub_house(pigeon_id):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    sub_list = Subscription.query( Subscription.pigeon_key==pigeon_key ).fetch()
    house_list = []
    if sub_list:
        for sub in sub_list:
            house_list.append( sub.house_key.get() )
        return map(lambda s: {"house_name": s.name, "cover_url": s.cover_url,
                              "category": s.category , "view": s.view,
                              "num_of_subed": s.num_of_subed},
                   house_list)
    else:
        return house_list

def get_all_house():
    house_list = House.query().fetch()
    return map(lambda s: {"house_name": s.name, "cover_url": s.cover_url,
                          "category": s.category , "view": s.view,
                          "num_of_subed": s.num_of_subed},
               house_list)

def get_single_house(house_name):
    house_list = House.query(House.name == house_name).fetch()
    if house_list:
        house = house_list[0]
        house.view = house.view+1
        house.put()
        card_list = Card.query(ancestor=house.key).fetch()
        return map(lambda s: {"key": s.card_key, "value": s.value},
                   card_list)
    else:
        return

def get_single_house_info(house_name):
    house_list = House.query(House.name == house_name).fetch()
    if house_list:
        s = house_list[0]
        return {"house_name": s.name, "cover_url": s.cover_url,
         "category": s.category, "view": s.view,
         "num_of_subed": s.num_of_subed}


def get_house_owner(house_name):
    house_list = House.query(House.name == house_name).fetch()
    if house_list:
        house = house_list[0]
        id = house.key.parent().get().pigeon_id
    return id



def is_subscribed(house_name, pigeon_id):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    sub_list = Subscription.query( Subscription.pigeon_key==pigeon_key,Subscription.house_key==house_key ).fetch()
    if sub_list:
        return True
    else:
        return False

def remove_house(house_name):
    house_list = House.query(House.name==house_name).fetch()
    if house_list:
        house_list[0].key.delete()
    return

def remove_all_sub(house_name):
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    sub_list = Subscription.query(Subscription.house_key==house_key).fetch()
    for sub in sub_list:
        sub.key.delete()
    return

def card_exists(house_name, card_key_str):
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key_str, parent=house_key)
    card = card_key.get()
    if card:
        return True
    else:
        return False

def remove_card(house_name, card_key_str):
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key_str, parent=house_key)
    card_key.delete()
    return

def edit_card_key (house_name, card_key_str, new_card_key):
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key_str, parent=house_key)
    card = card_key.get()
    value = card.value

    remove_card(house_name, card_key_str)
    add_card(house_name, new_card_key, value)
    return

def edit_card_content (house_name, card_key_str, new_card_content):
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key_str, parent=house_key)
    card = card_key.get()

    card.value = new_card_content
    card.put()
    return

def send_pull_request(user_id, house_name, mode, card_key_str, new_key, new_value):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key_str, parent=house_key)

    pr = PullRequest(pigeon_key=pigeon_key, house_key=house_key, card_key=card_key,
                     new_key=new_key, new_value=new_value, mode = mode, date_str='')
    pr.put()
    date2str = str(pr.date)
    str_list = date2str.split('.')
    pr.date_str = str_list[0]
    pr.put()

    return

def approve_pull_request(house_name, user_id, date):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key

    pr_list = PullRequest.query( PullRequest.pigeon_key==pigeon_key, PullRequest.house_key==house_key, PullRequest.date_str == date ).fetch()
    if pr_list:
        pr = pr_list[0]
        if pr.mode=='add':
            add_card(pr.house_key.get().name, pr.new_key, pr.new_value)
            pr.key.delete()
            return
        elif pr.mode=='remove':
            remove_card(pr.house_key.get().name, pr.card_key.get().card_key)
            pr.key.delete()
            return
        elif pr.mode=='key':
            edit_card_key(pr.house_key.get().name, pr.card_key.get().card_key, pr.new_key)
            pr.key.delete()
            return
        elif pr.mode=='content':
            edit_card_content(pr.house_key.get().name, pr.card_key.get().card_key, pr.new_value)
            pr.key.delete()
            return
    else:
        return

def reject_pull_request(house_name, user_id, date):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key

    pr_list = PullRequest.query( PullRequest.pigeon_key==pigeon_key, PullRequest.house_key==house_key, PullRequest.date_str == date ).fetch()
    if pr_list:
        pr = pr_list[0]
        pr.key.delete()
        return
    else:
        return

def show_all_pull_request(house_name):
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    pr_list = PullRequest.query(PullRequest.house_key==house_key).order(PullRequest.date).fetch()
    if pr_list:
        #print pr_list
        return map(lambda s: {"user_id": s.pigeon_key.get().pigeon_id, "mode": s.mode,
                              "newkey": s.new_key, "newcontent": s.new_value,
                              "date": s.date_str, "card_key": s.card_key.id()},
                   pr_list)
    else:
        return

def add_issue(user_id, house_name, card_key_str, content):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key_str,parent=house_key)

    issue = Issue(pigeon_key=pigeon_key, house_key=house_key, card_key=card_key, comment=content, date_str='' )
    issue.put()
    date2str = str(issue.date)
    str_list = date2str.split('.')
    issue.date_str = str_list[0]
    issue.put()

    return

def show_all_issues(house_name):
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    issue_list = Issue.query(Issue.house_key==house_key).order(Issue.date).fetch()
    if issue_list:
        return map(lambda s: {"user_id": s.pigeon_key.get().pigeon_id, "content": s.comment,
                              "date": s.date_str},
                   issue_list)
    else:
        return

def resolve_issue(house_name, user_id, date):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    issue_list = Issue.query( Issue.pigeon_key==pigeon_key,Issue.house_key==house_key, Issue.date_str==date ).fetch()
    if issue_list:
        issue = issue_list[0]
        issue.key.delete()
        return
    else:
        return

def add_post(house_name, user_id, content):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    post_list = Post.query( Post.pigeon_key==pigeon_key, Post.house_key==house_key ).fetch()
    if post_list:
        length = len(post_list)
        post = Post(pigeon_key=pigeon_key, house_key=house_key, content=content, number=length+1, date_str='')
        post.put()
        date2str = str(post.date)
        str_list = date2str.split('.')
        post.date_str = str_list[0]
        post.put()
        return
    else:
        post = Post(pigeon_key=pigeon_key, house_key=house_key, content=content, number=1, date_str='' )
        post.put()
        date2str = str(post.date)
        str_list = date2str.split('.')
        post.date_str = str_list[0]
        post.put()
        return


    # pr.put()
    # date2str = str(pr.date)
    # str_list = date2str.split('.')
    # pr.date_str = str_list[0]
    # pr.put()

def get_trending_subscription():
    house_list = House.query().fetch()
    sorted_list = sorted(house_list,key=lambda h: h.num_of_subed, reverse=True)
    return map(lambda s: {"house_name": s.name, "cover_url": s.cover_url,
                          "category": s.category, "num_of_subed": s.num_of_subed},
               sorted_list)

def get_trending_view():
    house_list = House.query().fetch()
    sorted_list = sorted(house_list, key=lambda h: h.view, reverse=True)
    return map(lambda s: {"house_name": s.name, "cover_url": s.cover_url,
                          "category": s.category, "view": s.view},
               sorted_list)

def get_category(category):
    house_list = House.query(House.category==category).fetch()
    return map(lambda s: {"house_name": s.name, "cover_url": s.cover_url,
                          "num_of_subed": s.num_of_subed, "view": s.view},
               house_list)


def get_num_per_day(user_id, house_name):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    sub_list = Subscription.query(Subscription.pigeon_key==pigeon_key, Subscription.house_key==house_key).fetch()
    if sub_list:
        return sub_list[0].num_per_day
    else:
        return

def _initailize_progress(pigeon_key,card_key):
    progress = Progress(pigeon_key=pigeon_key, card_key=card_key, familiar_factor=0, learn_factor=1)
    progress.put()
    return

def _delete_progress(pigeon_key,card_key):
    progress_list = Progress.query(Progress.pigeon_key==pigeon_key, Progress.card_key==card_key).fetch()
    if progress_list:
        progress = progress_list[0]
        progress.key.delete()
        return
    else:
        return


def set_schedule(user_id, house_name, num_per_day):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    sub_list = Subscription.query(Subscription.pigeon_key==pigeon_key, Subscription.house_key==house_key).fetch()
    if sub_list:
        sub_list[0].num_per_day = num_per_day
        sub_list[0].put()
        return
    else:
        return

def get_familiar_factor(user_id, house_name, card_key_str):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key_str, parent=house_key)
    progress_list = Progress.query(Progress.pigeon_key==pigeon_key,Progress.card_key==card_key).fetch()
    if progress_list:
        return progress_list[0].familiar_factor
    else:
        _initailize_progress(pigeon_key, card_key)
        return 0.0

def set_familiar_factor(user_id, house_name, card_key_str, familiar_factor):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key_str, parent=house_key)
    progress_list = Progress.query(Progress.pigeon_key==pigeon_key,Progress.card_key==card_key).fetch()
    if progress_list:
        progress = progress_list[0]
        progress.familiar_factor = familiar_factor
        progress.put()
        return
    else:
        return

def get_learn_factor(user_id, house_name, card_key_str):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key_str, parent=house_key)
    progress_list = Progress.query(Progress.pigeon_key==pigeon_key,Progress.card_key==card_key).fetch()
    if progress_list:
        return progress_list[0].learn_factor
    else:
        _initailize_progress(pigeon_key, card_key)
        return 1

def set_learn_factor(user_id, house_name, card_key_str, learn_factor):
    pigeon_key = ndb.Key(Pigeon, user_id)
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    card_key = ndb.Key(Card, card_key_str, parent=house_key)
    progress_list = Progress.query(Progress.pigeon_key==pigeon_key,Progress.card_key==card_key).fetch()
    if progress_list:
        progress = progress_list[0]
        progress.learn_factor = learn_factor
        progress.put()
        return
    else:
        return


def get_single_house_2(house_name):
    house_list = House.query(House.name == house_name).fetch()
    if house_list:
        house = house_list[0]
        house.view = house.view+1
        house.put()
        card_list = Card.query(ancestor=house.key).fetch()
        return map(lambda s: {str(s.card_key): str(s.value)},
                   card_list)
    else:
        return

def get_all_post(house_name):
    house_list = House.query(House.name==house_name).fetch()
    house_key = house_list[0].key
    post_list = Post.query( Post.house_key==house_key ).fetch()
    post_list = sorted( post_list, key = lambda p: p.number  )
    return map(lambda p: {"user_id": p.pigeon_key.get().pigeon_id, "house_name": p.house_key.get().name,
                          "number": p.number, "date": p.date_str, "content": p.content, "avatar": p.pigeon_key.get().avatar  },
               post_list)







