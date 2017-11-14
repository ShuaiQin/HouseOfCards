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
1. Get user scheduling input and make a plan for user
(the input could be: "Complete within XX days", "Complete XX words a day")

(this plan probably needs consider the Ebbinghaus Forgetting Curve)

2. User daily progress -> compare with planned progress
(daily progress includes: known words, unknown words)

if exceed
    re schedule based on the Ebbinghaus Forgetting Curve
if behind
    re schedule based on the Ebbinghaus Forgetting Curve

Another Function:

3. Show Known Words and Unknown Words (How many unknown words left)

4. Show How many days left to complete

5. Show progress bar

[Done] 6. Generate a quiz (for all repo)

"""

import webapp2
import json
import random


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

        # TODO: get_all_cards needs to be implemented (Database Operation)
        # all_cards is a list of dictionary
        list_of_all_cards = get_all_cards(house_id)

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

        # TODO: get_all_cards needs to be implemented (Database Operation)
        # all_cards is a list of dictionary
        # TODO: [{Key: Value},{Key: Value},{Key: Value},{Key: Value},....,{Key: Value}]
        list_of_all_cards = get_all_cards(house_id)

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
    def get(self):
        pass


service = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getmultiplequiz', GetMultipleQuizHandler),
    ('/gettruefalsequiz', GetTrueFalseQuizHandler),
    ('/makeschedule', MakeScheduleHandler)
], debug=True)
