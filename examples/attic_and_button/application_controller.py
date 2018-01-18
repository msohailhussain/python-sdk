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

from flask import request
from constants import Constants
from constants import Constants
from helpers import Helpers
from optimizely_client_manager import OptimizelyClientManager
from payloads import Payloads
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

    def __init__(self):
        self.__client_manager = OptimizelyClientManager(Constants.PROJECT_ID)
        self.__products_instance = Products()


    def handleProducts(self):
        return Payloads.getProducts(self.__products_instance.getAll())

    def handleVisitor(self, request):
        user_id = Helpers.parseFormValue(request.form['user_id'])

        if not (isinstance(self.__client_manager, OptimizelyClientManager) and self.__client_manager.get_obj()):
            return Payloads.getVisitor(Payloads.CODES["OPT_INSTANCE_NOT_FOUND"])

        if not self.__experiment_key:
            return Payloads.getVisitor(Payloads.CODES["EMPTY_EXPERIMENT_KEY"])

        if not user_id:
            return Payloads.getVisitor(Payloads.CODES["EMPTY_VISITOR_ID"])

        variation_key = self.__client_manager.get_obj(
        ).activate(self.__experiment_key, user_id)
        products = self.__products_instance.getAllSorted(variation_key)

        return Payloads.getVisitor(Payloads.CODES["SUCCESS"], variation_key, products)

    def handleBuy(self, request):
        user_id = Helpers.parseFormValue(request.form['user_id'])
        product_id = Helpers.parseFormValue(request.form['product_id'])

        if not (isinstance(self.__client_manager, OptimizelyClientManager) and self.__client_manager.get_obj()):
            return Payloads.getBuy(Payloads.CODES["OPT_INSTANCE_NOT_FOUND"])

        self.__client_manager.get_obj().track(self.__event_key, user_id)
        return Payloads.getBuy(Payloads.CODES["SUCCESS"])

    def handleLogs(self, request):
        if not (isinstance(self.__client_manager, OptimizelyClientManager) and self.__client_manager.get_obj()):
            return Payloads.getLogs(Payloads.CODES["OPT_INSTANCE_NOT_FOUND"])

        if request.method == 'GET':
            logs = self.__client_manager.getAllLogs()
            return Payloads.getLogs(Payloads.CODES["SUCCESS"], logs)

        elif request.method == 'POST':
            self.__client_manager.clearAllLogs()
            return Payloads.getLogs(Payloads.CODES["SUCCESS"])
