
/**
 * Get homepage data.
 */
function getHomePageRequest() {
    return jQuery.parseJSON($.ajax({
        type: 'GET',
        url: '/home',
        async: false
    }).responseText);
}

function getCurrentUser(){
    return $.ajax({
        type: 'GET',
        url: '/user',
        async: false
    }).responseText; 
}

/**
 * User login request
 */

function loginUserRequest(request) {
    return jQuery.parseJSON($.ajax({
        type: 'POST',
        url: '/login',
        data: request,
        async: false
    }).responseText);
}


function logoutUserRequest() {
    return jQuery.parseJSON($.ajax({
        type: 'POST',
        url: '/logout',
        async: false
    }).responseText);
}

/**
 * Get products.
 */
function getProductsRequest() {
    return jQuery.parseJSON($.ajax({
        type: 'GET',
        url: '/shop',
        async: false
    }).responseText);
}

function getCartDataRequest() {
   return {"next": "buy_now", "sub_total": 0, "discount":0,"total":0, "products": [{"category": "Shorts", "name": "Bo Henry", "color": "Khaki", "price": 37, "image_url": "images/item_2.png","qty": 1, "id": 1}, {"category": "Shirts", "name": "Long Sleeve Swing Shirt", "color": "Baby Blue", "price": 54, "image_url": "images/item_7.png","qty": 1,"id": 0}, {"category": "Shirts", "name": "Long Sleever Tee", "color": "Baby Blue", "price": 62, "image_url": "images/item_8.png","qty": 1,"id": 7}]}
}

// function getMessagesRequest() {
//    return [{"timestamp": 1516811246.53323, "message": "User \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\" is not in the forced variation map.", "level": 10}, {"timestamp": 1516811246.533275, "message": "Assigned bucket 3087.0 to user with bucketing ID \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\".", "level": 10}, {"timestamp": 1516811246.53329, "message": "User \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\" is in variation \"sort_by_name\" of experiment sorting_experiment.", "level": 20}, {"timestamp": 1516811246.533385, "message": "Tracking event \"add_to_cart\" for user \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\".", "level": 20}, {"timestamp": 1516811246.533415, "message": "Dispatching conversion event to URL https://logx.optimizely.com/v1/events with params {'account_id': u'8272261422', 'client_name': 'python-sdk', 'visitors': [{'attributes': [], 'visitor_id': 'be2f36e8-c7e3-48ba-8f82-992a1411ea2e', 'snapshots': [{'decisions': [{'variation_id': u'9996669231', 'experiment_id': u'10112740252', 'campaign_id': u'10037456370'}], 'events': [{'timestamp': 1516811246533, 'entity_id': u'9985098116', 'uuid': '64fa8a24-8146-4186-a71c-b5209bfdd421', 'key': 'add_to_cart'}]}]}], 'anonymize_ip': True, 'project_id': u'10111011215', 'client_version': '1.4.0'}.", "level": 10}, {"timestamp": 1516811257.618548, "message": "User \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\" is not in the forced variation map.", "level": 10}, {"timestamp": 1516811257.618585, "message": "Assigned bucket 3087.0 to user with bucketing ID \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\".", "level": 10}, {"timestamp": 1516811257.618598, "message": "User \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\" is in variation \"sort_by_name\" of experiment sorting_experiment.", "level": 20}, {"timestamp": 1516811257.618691, "message": "Tracking event \"add_to_cart\" for user \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\".", "level": 20}, {"timestamp": 1516811257.618718, "message": "Dispatching conversion event to URL https://logx.optimizely.com/v1/events with params {'account_id': u'8272261422', 'client_name': 'python-sdk', 'visitors': [{'attributes': [], 'visitor_id': 'be2f36e8-c7e3-48ba-8f82-992a1411ea2e', 'snapshots': [{'decisions': [{'variation_id': u'9996669231', 'experiment_id': u'10112740252', 'campaign_id': u'10037456370'}], 'events': [{'timestamp': 1516811257619, 'entity_id': u'9985098116', 'uuid': '62625ec3-3d6a-4b6f-97c2-cdbe12da7473', 'key': 'add_to_cart'}]}]}], 'anonymize_ip': True, 'project_id': u'10111011215', 'client_version': '1.4.0'}.", "level": 10}, {"timestamp": 1516811262.423354, "message": "User \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\" is not in the forced variation map.", "level": 10}, {"timestamp": 1516811262.423419, "message": "Assigned bucket 3087.0 to user with bucketing ID \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\".", "level": 10}, {"timestamp": 1516811262.423432, "message": "User \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\" is in variation \"sort_by_name\" of experiment sorting_experiment.", "level": 20}, {"timestamp": 1516811262.423531, "message": "Tracking event \"add_to_cart\" for user \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\".", "level": 20}, {"timestamp": 1516811262.423566, "message": "Dispatching conversion event to URL https://logx.optimizely.com/v1/events with params {'account_id': u'8272261422', 'client_name': 'python-sdk', 'visitors': [{'attributes': [], 'visitor_id': 'be2f36e8-c7e3-48ba-8f82-992a1411ea2e', 'snapshots': [{'decisions': [{'variation_id': u'9996669231', 'experiment_id': u'10112740252', 'campaign_id': u'10037456370'}], 'events': [{'timestamp': 1516811262423, 'entity_id': u'9985098116', 'uuid': '64610b54-a9e3-4ec7-8385-728390844a4c', 'key': 'add_to_cart'}]}]}], 'anonymize_ip': True, 'project_id': u'10111011215', 'client_version': '1.4.0'}.", "level": 10}, {"timestamp": 1516811495.279775, "message": "User \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\" is not in the forced variation map.", "level": 10}, {"timestamp": 1516811495.279812, "message": "Assigned bucket 3087.0 to user with bucketing ID \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\".", "level": 10}, {"timestamp": 1516811495.279825, "message": "User \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\" is in variation \"sort_by_name\" of experiment sorting_experiment.", "level": 20}, {"timestamp": 1516811495.279974, "message": "Tracking event \"add_to_cart\" for user \"be2f36e8-c7e3-48ba-8f82-992a1411ea2e\".", "level": 20}, {"timestamp": 1516811495.280019, "message": "Dispatching conversion event to URL https://logx.optimizely.com/v1/events with params {'account_id': u'8272261422', 'client_name': 'python-sdk', 'visitors': [{'attributes': [], 'visitor_id': 'be2f36e8-c7e3-48ba-8f82-992a1411ea2e', 'snapshots': [{'decisions': [{'variation_id': u'9996669231', 'experiment_id': u'10112740252', 'campaign_id': u'10037456370'}], 'events': [{'timestamp': 1516811495280, 'entity_id': u'9985098116', 'uuid': 'b49b63ef-bb18-4b85-9083-27dbc975c2c9', 'key': 'add_to_cart'}]}]}], 'anonymize_ip': True, 'project_id': u'10111011215', 'client_version': '1.4.0'}.", "level": 10}]
// }

/**
 * Select visitor.
 */
function selectVisitorRequest(request) {
    return jQuery.parseJSON($.ajax({
        type: 'POST',
        url: '/visitor',
        data: request,
        async: false
    }).responseText);
}

/**
 * Add to cart product
 */
function addToCartRequest(request) {
    return jQuery.parseJSON($.ajax({
        type: "POST",
        url:"/cart/product",
        data: request,
        async: false
    }).responseText);
}

function checkoutCartRequest() {
    return jQuery.parseJSON($.ajax({
        type: "GET",
        url:"/checkout",
        async: false
    }).responseText);
}

/**
 * Get all log messages.
 */
function getMessagesRequest() {
    return jQuery.parseJSON($.ajax({
        type: 'GET',
        url: '/messages',
        async: false
    }).responseText);
}

/**
 * Remove all log messages.
 */
function clearMessagesRequest() {
    return jQuery.parseJSON($.ajax({
        type: 'DELETE',
        url: '/messages',
        async: false
    }).responseText);
}
