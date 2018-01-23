# Copyright 2018, Optimizely
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from flask import request, session
from constants import Constants
from helpers import Helpers
from optimizely_client_manager import OptimizelyClientManager
from products import Products


class ApplicationController(object):

    # configuration data
    __project_id = None
    __experiment_key = None
    __event_key = None

    # optimizely client manager reference
    __client_manager = None

    # products reference
    __products_instance = None

    # flask logger
    __logger = None

    def __init__(self, flask_logger):
        self.__client_manager = OptimizelyClientManager(Constants.PROJECT_ID)
        self.__products_instance = Products()
        self.__logger = flask_logger

    def handle_login(self):
        # Return false if falsy user_id given
        if not Helpers.parseFormValue(request.form['userId']):
            this.__logger.debug('Empty user_id supplied.')
            return json.dumps(False)

        # Return false if another user already logged in
        if session['isGuestUser'] == False:
            this.__logger.debug(
                'Another user already logged in. Please logout first.')
            return json.dumps(False)

        session['userId'] = request.form['userId']
        session['isGuestUser'] = False
        session['cart'] = {}
        session['isActivatedForSortingExperiment'] = False

        return json.dumps(True)

    def handle_logout(self):
        # Return false if no user is logged in
        if session['isGuestUser'] == True:
            this.__logger.debug('No user logged in to log out.')
            return json.dumps(False)

        session['userId'] = None
        session['isGuestUser'] = None
        session['cart'] = {}
        session['isActivatedForSortingExperiment'] = None

        return json.dumps(True)

    def handle_shop(self):
        # Only activate if the user hasn't been activated.
        # For each user session, the user is activated for Sorting Experiment
        # only once
        if session['isActivatedForSortingExperiment'] == True:
            variation_key = self.__client_manager.get_obj().activate(
                Constants.SORTING_EXP_KEY, session['userId'])
        else:
            variation_key = self.__client_manager.get_obj().get_variation(
                Constants.SORTING_EXP_KEY, session['userId'])

        if variation_key is None:
            self.__logger.debug(
                'No variation key returned from Optimizely. Products will be returned in default ordering.')

        return json.dumps(self.__products_instance.getAllSorted(variation_key))

    def handle_products(self):
        return json.dumps(self.__products_instance.getAll())

    def handle_messages(self):
        if request.method == 'GET':
            logs = self.__client_manager.getAllLogs()
            return json.dumps(logs)

        elif request.method == 'DELETE':
            self.__client_manager.clearAllLogs()
            return None

    def handle_cart_product(self):
        num_of_products = 1

        product_id = request.form['productId']
        if 'num' in request.form:
            num_of_products = request.form['num']

        if request.method == 'POST':
            if not product_id in session['cart']:
                session['cart'][product_id] = num_of_products
            else:
                session['cart'][product_id] += num_of_products

            # Call AddtoCart event
            self.__client_manager.get_obj().track(
                Constants.ADD_TO_CART_EVENT_KEY, session['userId'])

            return json.dumps(True)

        if request.method == 'DELETE':
            if product_id in session['cart']:
                session['cart'][product_id] -= num_of_products

            if session['cart'][product_id] < 0:
                session['cart'][product_id] = 0

    def handle_checkout(self):
        variation = self.__client_manager.get_obj().activate(
            Constants.CHECKOUT_EXP_KEY, session['userId'])

        if variation == Constants.CHECKOUT_EXP_VAR_ONE_STEP:
            return json.dumps({'variation': 'one_step'})
        if variation == Constants.CHECKOUT_EXP_VAR_TWO_STEP:
            return json.dumps({'variation': 'two_step'})

    def handle_placeorder(self):
        cart_total = request.form['cartTotal']

        self.__client_manager.get_obj().track(
            Constants.CHECKOUT_COMPLETE_EVENT_KEY, session['userId'])

        session['cart'] = {}

        return None

    def handle_cart(self):
        if request.method == 'DELETE':
            session['cart'] = {}
            return json.dumps(True)

        if request.method == 'GET':
            # fetch cart products
            products = session['cart']

            # fetch discount_percentage
            discount_percentage = None
            domain = session['userId']
            if session['isGuestUser'] == False:
                id, domain = session[userId].split('@')

            if self.__client_manager.get_obj().is_feature_enabled(
                    Constants.DISCOUNT_FEATURE_KEY, session['userId'], {'domain': domain}):

                discount_percentage = self.__client_manager.get_obj().get_feature_variable_integer(
                    Constants.DISCOUNT_FEATURE_KEY, 'discount_percentage', session['userId'], {'domain': domain})

            # fetch buynow_enabled
            # Only check for logged in users
            buynow_enabled = False

            if session['isGuestUser'] == False:
                buynow_enabled = self.__client_manager.get_obj().is_feature_enabled(
                    Constants.BUY_NOW_FEATURE_KEY, session['userId'], {'domain': domain})

            return json.dumps({
                              'products': products,
                              'discount_percentage': discount_percentage,
                              'buynow_enabled': buynow_enabled
                              })

    def handle_user(self):
        if session['isGuestUser']:
            return json.dumps(None)
        return session['userId']
