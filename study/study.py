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
Get user scheduling input and make a plan for user
(the input could be: "Complete within XX days", "Complete XX words a day")

(this plan probably needs consider the Ebbinghaus Forgetting Curve)

User daily progress -> compare with planned progress
(daily progress includes: known words, unknown words)

if exceed
    re schedule based on the Ebbinghaus Forgetting Curve
if behind
    re schedule based on the Ebbinghaus Forgetting Curve

Another Function:

1. Show Known Words and Unknown Words (How many unknown words left)

2. Show How many days left to complete

3. Show progress bar

4. Generate a quiz (for all repo)

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
        for key in list_of_all_cards:
            list_of_all_values.append(list_of_all_cards[key])

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
            list_of_question.append(single_question)

        return_info = {
            'list_of_question': list_of_question,
            'list_of_answer': list_of_answer
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class GetTrueFalseQuizHandler(webapp2.RequestHandler):
    def get(self):
        pass


service = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getmultiplequiz', GetMultipleQuizHandler),
    ('/gettruefalsequiz', GetTrueFalseQuizHandler)
], debug=True)
