
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

/**
 * Get configuration.
 */
function getConfigRequest() {
    return jQuery.parseJSON($.ajax({
        type: 'GET',
        url: '/config',
        async: false
    }).responseText);
}

/**
 * Set configuration.
 */
function setConfigRequest(request) {
    return jQuery.parseJSON($.ajax({
        type: 'POST',
        url: '/config',
        data: request,
        async: false
    }).responseText);
}

/**
 * Get products.
 */
function getProductsRequest() {
    return jQuery.parseJSON($.ajax({
        type: 'GET',
        url: '/products',
        async: false
    }).responseText);
}

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
 * Buy a product.
 */
function buyProductRequest(request) {
    return jQuery.parseJSON($.ajax({
        type: 'POST',
        url: '/buy',
        data: request,
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
        type: 'POST',
        url: '/messages',
        async: false
    }).responseText);
}