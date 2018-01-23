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

import time
from collections import namedtuple
from operator import itemgetter

from optimizely.logger import BaseLogger


class ApplicationLogger(BaseLogger):

    __data = []

    def log(self, log_level, message):
        self.__data.append({
            'timestamp': time.time(),
            'level': log_level,
            'message': message
        })

    def clearAllLogs(self):
        self.__data = []

    def getAllLogs(self):
        return self.__data
