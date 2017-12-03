from google.appengine.api import users
from google.appengine.api import urlfetch
import webapp2

import config.config as cfg

import json, csv
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


class DeleteHouseHandler(webapp2.RequestHandler):
    def get(self, name):
        form_fields = {
            'delete_house_string': name
        }

        form_data = urllib.urlencode(form_fields)

        rpc = urlfetch.create_rpc()
        url = cfg.SERVICE_URL + "/service-removehouse?" + form_data
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        self.redirect('/')


class AddCardHandler(webapp2.RequestHandler):
    def uploadCard(self, name, key, content):
        card_fields = {
            'card_key': key,
            'card_value': content,
            'house_name': name
        }

        rpc = urlfetch.create_rpc()
        url = cfg.SERVICE_URL + "/service-addcard?" + urllib.urlencode(card_fields)
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        return


    def post(self, name):

        f = self.request.POST.get('upload_csv')
        print f
        if f != None:
            print 1
            csv_reader = csv.reader(f.file)
            for row in csv_reader:
                self.uploadCard(name, row[0], row[1])
        else:
            key = self.request.get('card_key')
            content = self.request.get('content')
            if key and content:
                self.uploadCard(name, key, content)
        self.redirect('/house/' + name)



