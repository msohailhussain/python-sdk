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


class Constants(object):

    # Project ID
    PROJECT_ID = '10111011215'

    # Sorting Experiment
    SORTING_EXP_KEY = 'sorting_experiment'
    SORTING_EXP_VAR_BY_PRICE = 'sort_by_price'
    SORTING_EXP_VAR_BY_NAME = 'sort_by_name'
    ADD_TO_CART_EVENT_KEY = 'add_to_cart'

    # Discount Feature
    DISCOUNT_FEATURE_KEY = 'discount_feature'

    # BuyNow Feature
    BUY_NOW_FEATURE_KEY = 'buynow_feature'

    # Checkout Flow Experiment
    CHECKOUT_EXP_KEY = 'checkout_flow_experiment'
    CHECKOUT_EXP_VAR_ONE_STEP = 'one_step_checkout'
    CHECKOUT_EXP_VAR_TWO_STEP = 'two_step_checkout'
    CHECKOUT_COMPLETE_EVENT_KEY = 'checkout_complete'

    # Audiences
    EMAIL_DOMAIN_ATTRIBUTE_KEY = 'domain'

    # Others
    DEMO_APP_DIR = 'attic_and_button'
    UI_DIR = 'public'
    HOME_PAGE_URL = 'index.html'
    CDN_URL = 'https://cdn.optimizely.com/json/{0}.json'
    IMAGES_DIR_PATH_FROM_UI_DIR = "images/"
