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
#
import os
import csv
from operator import itemgetter

from constants import Constants


class Products(object):

    __items = []

    def __init__(self):
        self.__build()

    def __build(self):
        reader = csv.reader(open('products.csv', 'r'))
        for idx, line in enumerate(reader):
            self.__items.append({
                'id': idx,
                'name': line[0],
                'color': line[1],
                'category': line[2],
                'price': int(line[3][1:]),
                'image_url': Constants.IMAGES_DIR_PATH_FROM_UI_DIR + line[4]})

    def getAll(self):
        return self.__items

    def getAllSorted(self, variation_key):
        items = self.getAll()

        # sort by ID
        if variation_key == Constants.VARIATIONS['id']:
            return sorted(items, key=itemgetter('id'))

        # sort by name
        if variation_key == Constants.VARIATIONS['name']:
            return sorted(items, key=itemgetter('name'))

        # sort by price
        if variation_key == Constants.VARIATIONS['price']:
            return sorted(items, key=itemgetter('price'))

        # sort by category
        if variation_key == Constants.VARIATIONS['category']:
            return sorted(items, key=itemgetter('category'))

        # return products on default ordering
        return items
