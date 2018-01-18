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

import requests

from optimizely import optimizely

from application_logger import ApplicationLogger
from constants import Constants


class OptimizelyClientManager(object):

    __obj = None  # optimizely instance
    __project_id = None
    __datafile = None
    __logger = None  # application logger

    def __init__(self, project_id):
        self.__project_id = project_id
        self.__logger = ApplicationLogger()

    def get_obj(self):
        if not self.__obj:
            self.set_obj()
        return self.__obj

    def set_obj(self):
        datafile = self.retrieve_datafile_text()
        if datafile is None:
            self.__obj = None
            return

        self.__obj = optimizely.Optimizely(datafile, None, self.__logger)

    def __retrieve_datafile(self):
        if self.__datafile:
            return self.__datafile

        url = Constants.CDN_URL.format(self.__project_id)

        r = requests.get(url)
        if r.status_code == 200:
            self.__datafile = r

    def retrieve_datafile_text(self):
        self.__retrieve_datafile()
        if self.__datafile:
            return self.__datafile.text

        return None

    def retrieve_datafile_json(self):
        self.__retrieve_datafile()
        if self.__datafile:
            return self.__datafile.json()

        return None

    def getAllLogs(self):
        return self.__logger.getAllLogs()

    def clearAllLogs(self):
        self.__logger.clearAllLogs()
