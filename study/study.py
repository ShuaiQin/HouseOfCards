#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
[Done] 1. Get user scheduling input and make a plan for user
(the input could be: "Complete within XX days", "Complete XX words a day")
(Complete XX words a day is much more simple and realizable)

(this plan probably needs consider the Ebbinghaus Forgetting Curve)

2. User daily progress -> compare with planned progress
(daily progress includes: known words, unknown words)

if exceed
    re schedule based on the Ebbinghaus Forgetting Curve
if behind
    re schedule based on the Ebbinghaus Forgetting Curve

Another Function:

[Done] 3. Show Known Words and Unknown Words (How many unknown words left)

[Modification] 4. Show How many days left to complete

[Done] 5. Show progress bar

[Done] 6. Generate a quiz (for all repo)

"""

import webapp2
import json
import random
import math
from model import ops


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('study: Hello world!')


class GetMultipleQuizHandler(webapp2.RequestHandler):
    """
    This handler is for generating a multiple choice quiz
    :input_1: house_id (repo id)
    :input_2: number_of_quiz (how many quiz does user want, check legal at web front end)
    :return: json output. two lists:
             1. (correct answer) [{key: value}, ..., {key: value}]
             2. (multiple choices) [{key: [value, value, value, value]}, ..., {key: [value, value, value, value]}]
             the default multiple choices are 4, if number of cards < 4, multiple choices are the number
    """
    def get(self):
        number_of_quiz = self.request.get('number_of_quiz')
        house_id = self.request.get('house_id')

        # all_cards is a list of dictionary
        list_of_all_cards = ops.get_all_cards(house_id)

        # get a list of all values for future convenience
        list_of_all_values = []
        for single_card in list_of_all_cards:
            for key in single_card:
                list_of_all_values.append(single_card[key])

        # get a random list of cards with total number is number_of_quiz
        list_of_random_cards = random.sample(list_of_all_cards, number_of_quiz)

        # construct the list of answer
        list_of_answer = list(list_of_random_cards)

        # construct the list of multiple choice
        list_of_question = []
        for card in list_of_random_cards:
            # construct a random answer list for future use
            list_of_all_random_values = random.sample(list_of_all_values, len(list_of_all_values))
            # construct a single question dict
            single_question = {}
            # get the key of the single card
            for key in card:
                # the choice is a list including 4 answers
                single_question[key] = []
                # include the right answer first
                single_question[key].append(card[key])
                # append three other values in single_question[key]
                count = 0
                while len(single_question[key]) < 4 and count < len(list_of_all_random_values):
                    if list_of_all_random_values[count] != card[key]:
                        single_question[key].append(list_of_all_random_values[count])
                    count = count + 1
                single_question[key] = random.sample(single_question[key], len(single_question[key]))
            list_of_question.append(single_question)

        return_info = {
            'list_of_question': list_of_question,
            'list_of_answer': list_of_answer
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class GetTrueFalseQuizHandler(webapp2.RequestHandler):
    """
    This handler is for generating a True/False quiz
    :input_1: house_id (repo id)
    :input_2: number_of_quiz (how many quiz does user want, check legal at web front end)
    :return: json output. two lists:
             1. (correct answer) [{key: value}, ..., {key: value}]
             2. (True/False choices) [{key: value}, ..., {key: value}], value may be true or false (~50%)
             the true/false probability is ~50% when data is quite large
    """
    def get(self):
        number_of_quiz = self.request.get('number_of_quiz')
        house_id = self.request.get('house_id')

        # all_cards is a list of dictionary
        list_of_all_cards = ops.get_all_cards(house_id)

        # get a list of all values for future convenience
        list_of_all_values = []
        for single_card in list_of_all_cards:
            for key in single_card:
                list_of_all_values.append(single_card[key])

        # get a random list of cards with total number is number_of_quiz
        list_of_random_cards = random.sample(list_of_all_cards, number_of_quiz)

        # construct the list of answer
        list_of_answer = list(list_of_random_cards)

        list_of_question = []
        for single_card in list_of_random_cards:
            # construct a single question with only one true or false answer
            single_question = {}
            # this list should have only two values, true value and false value
            list_of_possible_answer = []
            for key in single_card:
                list_of_possible_answer.append(single_card[key])
                list_of_possible_answer.append(random.choice(list_of_all_values))
                single_question[key] = str(random.choice(list_of_possible_answer))
            list_of_question.append(single_question)

        return_info = {
            'list_of_question': list_of_question,
            'list_of_answer': list_of_answer
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class MakeScheduleHandler(webapp2.RequestHandler):
    """
    This handler is for generating a personal schedule based on user input and Ebbinghaus curve
    :input_1: house_id (repo id)
    :input_2: number_of_key_per_day (how many keys does user want to learn per day)
    :return: json output. one lists:
             1. list_of_schedule: [[new1, review1], [new2, review1, review2], ..., [review]]
             will consider how to store it in database and get back to front-end
    """
    def get(self):
        pigeon_id = self.request.get('pigeon_id')
        number_of_key_per_day = self.request.get('number_of_key_per_day')
        house_id = self.request.get('house_id')

        list_of_all_cards = ops.get_all_cards(house_id)

        # get the total card length
        total_cards = len(list_of_all_cards)

        # calculate the supposed day needed, total number of review blocks
        supposed_day = int(math.ceil(float(total_cards) / float(number_of_key_per_day)))
        # calculate the total day needed based on the Ebbinghaus Curve
        total_day = int(supposed_day + math.pow(2, math.floor(math.log(supposed_day, 2)))) - 1
        # increase factor is to calculate how many extra days needed for review
        increase_factor = int(math.floor(math.log(supposed_day, 2)))

        # construct a schedule list
        list_of_schedule = [None] * total_day
        for i in range(0, len(list_of_schedule)):
            list_of_schedule[i] = []

        # study the new material at the beginning of a day
        for i in range(0, supposed_day):
            list_of_schedule[i].append("new" + str(i))

        # review the old material based on the general memory forgotten curve
        for i in range(0, supposed_day):
            for j in range(0, increase_factor + 1):
                list_of_schedule[int(math.pow(2, j) - 1 + i)].append("review" + str(i))

        # for test
        return_info = {
            'list_of_schedule': list_of_schedule
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class ShowProgressHandler(webapp2.RequestHandler):
    """
    This handler is for showing the progress, need to be estimated by equation
    :input_1: house_id (repo id)
    :input_2: pigeon_id
    :return: json output. two integers
             1. num_of_remain_unlearn_key
             2. approx_day_left (estimation)
    """
    def get(self):
        pigeon_id = self.request.get('pigeon_id')
        house_id = self.request.get('house_id')

        list_of_familiar_factor = ops.get_list_of_familiar_factor(pigeon_id, house_id)
        number_of_key_per_day = ops.get_num_per_day(pigeon_id, house_id)

        # find out how many unlearn words (familiar_factor == 0)
        count = 0
        for i in range(len(list_of_familiar_factor)):
            if list_of_familiar_factor[i] == 0:
                count = count + 1

        # TODO: need to be estimated well
        # calculate how many days left to finish all unlearn words (basic)
        approx_day_left = math.ceil(count / number_of_key_per_day)

        return_info = {
            'num_of_remain_unlearn_key': count,
            'approx_day_left': approx_day_left
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class GetTodayTaskHandler(webapp2.RequestHandler):
    """
        This handler is for returning the words need to be learned and reviewed based on Ebbinghaus equation
        :input_1: house_id (repo id)
        :input_2: pigeon_id
        :return: json output. one list
                 1. [{Key, Value}, {Key, Value},...]
    """
    def get(self):
        # get the pigeon id and the house the pigeon want to learn
        pigeon_id = self.request.get('pigeon_id')
        house_id = self.request.get('house_id')
        # the number of key per day the pigeon want to learn is pre-set by user
        number_of_key_per_day = ops.get_num_per_day(pigeon_id, house_id)
        # get all cards for generation of feed
        list_of_all_cards = ops.get_all_cards(house_id)
        # each pigeon has a special familiar factor to each card, initial is 0
        list_of_familiar_factor = ops.get_list_of_familiar_factor(pigeon_id, house_id)
        # number of times (factor) the pigeon has learned this card
        list_of_learn_factor = ops.get_list_of_learn_time(pigeon_id, house_id)
        # the total number of the cards
        number_of_cards = len(list_of_all_cards)

        # list of feed stores the index rather than content
        list_of_feed = []
        # limit by number of new words the pigeon want to learn
        count_of_new = 0
        # assume review is equal to the new
        count_of_review = 0

        for i in range(number_of_cards):
            # TODO: which should be cron job set by 1 day (modify later)
            # the familiar factor is decreased due to Ebbinghaus forgetting curve equation
            list_of_familiar_factor[i] = list_of_familiar_factor[i] * math.exp(-1 / list_of_learn_factor[i])
            # fetch the words need review first, the number is limited by number of key per day
            if 0.0 < list_of_familiar_factor[i] < 50.0 and count_of_review < number_of_key_per_day:
                list_of_feed.append(i)
                # we assume the user 100% learn that
                # set the familiar factor to 100 (know it very well)
                list_of_familiar_factor[i] = 100.0
                count_of_review = count_of_review + 1
                # learn factor gets increased due to multiple time learning
                list_of_learn_factor[i] = list_of_learn_factor[i] * 2.0
            # fetch the new words
            elif list_of_familiar_factor[i] == 0.0 and count_of_new < number_of_key_per_day:
                list_of_feed.append(i)
                list_of_familiar_factor[i] = 100.0
                count_of_new = count_of_new + 1
                # learn factor gets increased, the more time you review the less chance you forget it
                list_of_learn_factor[i] = list_of_learn_factor[i] * 2.0

        # store the familiar factor and learn factor in db
        ops.set_familiar_factor(pigeon_id, house_id, list_of_familiar_factor)
        ops.set_list_of_learn_factor(pigeon_id, house_id, list_of_learn_factor)

        # construct a list of feed cards
        list_of_feed_cards = []
        for index in list_of_feed:
            # [{Key: Value}, {Key: Value}, ..., {Key: Value}]
            list_of_feed_cards.append(list_of_all_cards[index])

        # [{Key: Value}, {Key: Value}, ..., {Key: Value}]
        return_info = {
            'list_of_feed_cards': list_of_feed_cards
        }

        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class SetScheduleHandler(webapp2.RequestHandler):
    def get(self):
        pigeon_id = self.request.get('pigeon_id')
        house_id = self.request.get('house_id')
        num_per_day = self.request.get('num_per_day')
        ops.set_schedule(pigeon_id, house_id, num_per_day)


class CheckScheduleHandler(webapp2.RequestHandler):
    """
        This handler is for checking if the progress is end
        :input_1: house_id (repo id)
        :input_2: pigeon_id
        :return: json output. Boolean True / False
    """
    def get(self):
        pigeon_id = self.request.get('pigeon_id')
        house_id = self.request.get('house_id')
        list_of_familiar_factor = ops.get_list_of_familiar_factor(pigeon_id, house_id)

        # set the threshhold to 50.0, maybe change later
        count = 0
        for i in range(len(list_of_familiar_factor)):
            if list_of_familiar_factor[i] < 50.0:
                count = count + 1

        if count != 0:
            is_finished = False
        else:
            is_finished = True

        return_info = {
            'is_finished': is_finished
        }

        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


service = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getmultiplequiz', GetMultipleQuizHandler),
    ('/gettruefalsequiz', GetTrueFalseQuizHandler),
    ('/makeschedule', MakeScheduleHandler),
    ('/showprogress', ShowProgressHandler),
    ('/gettodaytask', GetTodayTaskHandler),
    ('/setshedule', SetScheduleHandler),
    ('/checkschedulefinish', CheckScheduleHandler)
], debug=True)
