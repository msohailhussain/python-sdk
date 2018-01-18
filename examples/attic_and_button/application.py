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
import os

from flask import Flask, request, send_from_directory

from application_controller import ApplicationController
from constants import Constants
from helpers import Helpers

app = Flask(__name__, static_folder=Constants.UI_DIR)

appController = ApplicationController()

# API routes

@app.route("/shop")


@app.route("/products")
def products():
    return appController.handleProducts()

@app.route("/cart/product")

@app.route("/cart/products")

@app.route("/cart")

@app.route("/checkout")

@app.route("/placeorder")


@app.route("/buy", methods=['POST'])
def buy():
    return appController.handleBuy(request)


@app.route("/messages", methods=['GET', 'POST'])
def logs():
    return appController.handleLogs(request)

@app.route("/login")

@app.route("/logout")


# Static Files Routes

@app.route('/')
@app.route('/<path:filename>')
def serve_file(filename=Constants.HOME_PAGE_URL):
    return send_from_directory(Helpers.getStaticFolderPath(), filename)


@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(Helpers.getStaticFolderPath(), 'images'), filename)


@app.route('/templates/<path:filename>')
def serve_template(filename):
    return send_from_directory(os.path.join(Helpers.getStaticFolderPath(), 'templates'), filename)


@app.route('/fonts/<path:filename>')
def serve_font(filename):
    return send_from_directory(os.path.join(Helpers.getStaticFolderPath(), 'fonts'), filename)


if __name__ == '__main__':
    app.debug = True
    app.run(port=3001)
