from google.appengine.api import users
from google.appengine.api import urlfetch
import webapp2

import config.config as cfg
import json
import urllib
import random


class QuizPage(webapp2.RequestHandler):

    def get(self, name):

        user = users.get_current_user()
        if user:
            template_value = {}
            template_value['myself'] = user.email()
            template_value['logout_url'] = cfg.LOG_OUT_URL
            template_value['sign'] = True
            data = self.rpc(user.email())
            template_value['name'] = name
            all_house = data['subed_house_list']
            template_value['quiz_house'] = None
            template_value['subed_houses'] = []
            for house in all_house:
                if house['house_name'] == name:
                    template_value['quiz_house'] = house
                else:
                    template_value['subed_houses'].append(house)

            size = self.size_rpc(name)
            data = self.tf_rpc(name, min(size, 5))
            template_value['questions'] = dict(
                map(
                    lambda d: (d["key"], d["possible_answer"]),
                    data['list_of_question']
                )
            )
            template_value['answer'] = dict(
                map(
                    lambda d: (d["key"], d["value"]),
                    data['list_of_answer']
                )
            )

            data = self.mc_rpc(name, min(size, 5))
            template_value['m_answer'] = dict(
                map(
                    lambda d: (d["key"], d["value"]),
                    data['list_of_answer']
                )
            )
            template_value['m_questions'] = dict(
                map(
                    lambda d: (d["key"], d["list_of_possible_answer"]),
                    data['list_of_question']
                )
            )

            template = cfg.JINJA_ENVIRONMENT.get_template("study.html")
            self.response.write(template.render(template_value))
        else:
            self.redirect("/login")

    def rpc(self, user_id):
        rpc = urlfetch.create_rpc()
        request = {}
        request['user_id'] = user_id
        url = cfg.SERVICE_URL + "/service-manageprofile?" + urllib.urlencode(request)
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        data = json.loads(response.content)
        return data

    def tf_rpc(self, name, num):
        rpc = urlfetch.create_rpc()
        request = {
            'number_of_quiz': num,
            'house_id': name
        }
        url = cfg.SERVICE_URL + "/gettruefalsequiz?" + urllib.urlencode(request)
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        data = json.loads(response.content)
        return data

    def mc_rpc(self, name, num):
        rpc = urlfetch.create_rpc()
        request = {
            'number_of_quiz': num,
            'house_id': name
        }
        url = cfg.SERVICE_URL + "/getmultiplequiz?" + urllib.urlencode(request)
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        data = json.loads(response.content)
        return data

    def size_rpc(self, name):
        rpc = urlfetch.create_rpc()
        request = {
            'house_id': name
        }
        url = cfg.SERVICE_URL + "/gethousesize?" + urllib.urlencode(request)
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        data = json.loads(response.content)
        return data['size_of_house']


class StudyPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            data = self.rpc(user.email())
            houses = data['subed_house_list']
            if not houses:
                self.redirect('/')
            idx = random.randint(0, len(houses) - 1)
            print idx
            name = houses[idx].get('house_name')
            self.redirect("/study/" + name)
        else:
            self.redirect("/login")

    def rpc(self, user_id):
        rpc = urlfetch.create_rpc()
        request = {}
        request['user_id'] = user_id
        url = cfg.SERVICE_URL + "/service-manageprofile?" + urllib.urlencode(request)
        print url
        urlfetch.make_fetch_call(rpc, url)
        response = rpc.get_result()
        data = json.loads(response.content)
        return data