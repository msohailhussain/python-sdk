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

import os

from constants import Constants


class Helpers(object):

    @staticmethod
    def parseFormValue(inp):
        """ converts 'null' to Python None
        """
        if inp == 'null':
            return None
        return inp

    @staticmethod
    def getStaticFolderPath():
        root_dir = os.path.dirname(os.getcwd())
        root_dir = os.path.join(
            root_dir, Constants.DEMO_APP_DIR, Constants.UI_DIR)
        return root_dir
