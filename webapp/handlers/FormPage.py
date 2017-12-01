from google.appengine.api import users
from google.appengine.api import urlfetch
import webapp2

import config.config as cfg

import json
import urllib


class PrFormHandler(webapp2.RequestHandler):
    def post(self, name):
        form_fields = {
            'user_id': users.get_current_user().email(),
            'house_name': name,
            'card_key': self.request.get('card_key'),
            'mode': self.request.get('mode'),
            'new_key': self.request.get('new_key'),
            'new_value': self.request.get('new_value')
        }

        form_data = urllib.urlencode(form_fields)

        rpc = urlfetch.create_rpc()
        url = cfg.SERVICE_URL + "/service-createpullrequest?" + form_data
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        self.redirect('/house/' + name)


class PrResolveHandler(webapp2.RequestHandler):
    def get(self, name, date, decision, user_id):
        form_fields = {
            'user_id': user_id,
            'house_name': name,
            'date': date,
            'decision': decision
        }

        form_data = urllib.urlencode(form_fields)

        rpc = urlfetch.create_rpc()
        url = cfg.SERVICE_URL + "/service-resolvepullrequest?" + form_data
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        self.redirect('/house/' + name)


class PostFormHandler(webapp2.RequestHandler):
    def post(self, name):
        form_fields = {
            'user_id': users.get_current_user().email(),
            'house_name': name,
            'content': self.request.get('content')
        }

        form_data = urllib.urlencode(form_fields)

        rpc = urlfetch.create_rpc()
        url = cfg.SERVICE_URL + "/service-addpost?" + form_data
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        self.redirect('/house/' + name)


class IssueFormHandler(webapp2.RequestHandler):
    def post(self, name):
        form_fields = {
            'user_id': users.get_current_user().email(),
            'house_name': name,
            'card_key': self.request.get('card_key'),
            'content': self.request.get('content')
        }

        form_data = urllib.urlencode(form_fields)

        rpc = urlfetch.create_rpc()
        url = cfg.SERVICE_URL + "/service-addissue?" + form_data
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        self.redirect('/house/' + name)


class IssueResolveHandler(webapp2.RequestHandler):
    def get(self, name, date, user_id):
        form_fields = {
            'user_id': user_id,
            'house_name': name,
            'date': date,
        }

        form_data = urllib.urlencode(form_fields)

        rpc = urlfetch.create_rpc()
        url = cfg.SERVICE_URL + "/service-resolveissue?" + form_data
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        self.redirect('/house/' + name)