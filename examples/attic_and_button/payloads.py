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


class Payloads(object):

    CODES = {
        "SUCCESS": "0",
        "OPT_INSTANCE_NOT_FOUND": "001",
        "EMPTY_PROJ_ID": "002",
        "DATAFILE_NOT_FOUND": "003",
        "EMPTY_VISITOR_ID": "004",
        "EMPTY_EXPERIMENT_KEY": "005"
    }

    @staticmethod
    def getInfo(title, doc_link):
        return '{"sdk_title": %s, "doc_link": %s}' % (title, doc_link)

    @staticmethod
    def getConfig(status, project_id=None, experiment_key=None, event_key=None, datafile_json=None):
        return json.dumps({
                          'status': status,
                          'project_id': project_id,
                          'experiment_key': experiment_key,
                          'event_key': event_key,
                          'datafile_json': datafile_json
                          })

    @staticmethod
    def getProducts(products):
        return json.dumps(products)

    @staticmethod
    def getVisitor(status, variation_key=None, products=None):
        return json.dumps({
            'status': status,
            'variation_key': variation_key,
            'products': products
        })

    @staticmethod
    def getBuy(status):
        return '{"status": %s}' % (status)

    @staticmethod
    def getLogs(status, logs=None):
        return json.dumps({
                          'status': status,
                          'logs': logs
                          })
