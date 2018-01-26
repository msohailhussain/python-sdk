

function getCurrentUserRequest(){
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
    // return jQuery.parseJSON($.ajax({
    //     type: 'GET',
    //     url: '/shop',
    //     async: false
    // }).responseText);
   return {"next": "checkout", "sub_total": 0, "discount":0, "total":0, "products": [{"category": "Shorts", "name": "Bo Henry", "color": "Khaki", "price": 37, "image_url": "images/item_2.png","qty": 1, "total": 62,"id": 1}, {"category": "Shirts", "name": "Long Sleeve Swing Shirt", "color": "Baby Blue", "price": 54, "image_url": "images/item_7.png","qty": 1, "total": 54, "id": 0}, {"category": "Shirts", "name": "Long Sleever Tee", "color": "Baby Blue", "price": 62, "image_url": "images/item_8.png","qty": 1,"total": 37,"id": 7}]}
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

/**
 * Remove cart items
 */
function removeCartItemRequest(request) {
    console.log(request);
    return jQuery.parseJSON($.ajax({
        type: "DELETE",
        url:"/cart/product",
        data: request,
        async: false
    }).responseText);
}

/**
 * Remove all cart items.
 */
function clearCartRequest() {
    return jQuery.parseJSON($.ajax({
        type: 'DELETE',
        url: '/cart',
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
