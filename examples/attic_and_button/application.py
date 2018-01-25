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
import uuid

from flask import Flask, redirect, url_for, session, send_from_directory, request

from application_controller import ApplicationController
from constants import Constants
from helpers import Helpers

app = Flask(__name__, static_folder=Constants.UI_DIR)

appController = ApplicationController(app.logger)


@app.before_request
def configure_guest_user():
    if ('userId' not in session) or (not session['userId']):
        session['userId'] = str(uuid.uuid4())
        session['isGuestUser'] = True
        session['cart'] = {}
        session['isActivatedForSortingExperiment'] = False

# API routes


@app.route("/")
def index():
    return redirect(url_for('shop'))


@app.route('/login', methods=['POST'])
def login():
    return appController.handle_login()


@app.route("/logout", methods=['POST'])
def logout():
    return appController.handle_logout()


@app.route("/user")
def user():
    return appController.handle_user()


@app.route("/shop")
def shop():
    return appController.handle_shop()


@app.route("/products")
def products():
    return appController.handle_products()


@app.route("/cart/product", methods=['POST', 'DELETE'])
def cart_product():
    return appController.handle_cart_product()


@app.route("/cart", methods=['GET', 'DELETE'])
def cart():
    return appController.handle_cart()


@app.route("/checkout")
def checkout():
    return appController.handle_checkout()


@app.route("/placeorder", methods=['POST'])
def placeorder():
    return appController.handle_placeorder()


@app.route("/messages", methods=['GET', 'DELETE'])
def messages():
    return appController.handle_messages()


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


app.secret_key = '55ef285d-a1a8-430f-ab31-fde621e354a5'
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3001)
