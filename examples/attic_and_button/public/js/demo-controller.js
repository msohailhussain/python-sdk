function DemoController (params) {
    this.data = params;
}

DemoController.prototype.getDemoConfig = function() {
    var JsonResponse = ValidateResponse(getConfigRequest()); // Sends GET /config Ajax request
    return JsonResponse;
};


DemoController.prototype.addToCart = function() {
    var JsonResponse = addToCartRequest(this.data); // Sends POST /config Ajax request
    return JsonResponse;
};

DemoController.prototype.loginUser = function(){
	var JsonResponse = loginUserRequest(this.data); // Sends POST /login Ajax request
	return JsonResponse;
}
DemoController.prototype.logoutUser = function(){
	var JsonResponse = logoutUserRequest(); // Sends POST /login Ajax request
	console.log(JsonResponse);
	return JsonResponse;
}

DemoController.prototype.getProducts = function(){
	var JsonResponse = getProductsRequest(); // Sends GET /products Ajax request
	return JsonResponse;
}

DemoController.prototype.getCartData = function(){
	var JsonResponse = getCartDataRequest(); // Sends GET /products Ajax request
	return JsonResponse;
}

DemoController.prototype.checkoutCart = function() {
    var JsonResponse = checkoutCartRequest(); // Sends POST /config Ajax request
    return JsonResponse;
};

DemoController.prototype.getMessages = function(){
	var JsonResponse = getMessagesRequest(); // Sends GET /products Ajax request
	return JsonResponse;
}

DemoController.prototype.clearMessages = function(){
	var JsonResponse = clearMessagesRequest(); // Sends GET /products Ajax request
	return JsonResponse;
}

DemoController.prototype.selectVisitor = function(visitor){
	var JsonResponse = selectVisitorRequest(visitor); // Sends POST /visitor Ajax request
	return JsonResponse;
}


function ValidateResponse(response){
	if (typeof response != 'undefined'){
		response['datafile_json'] = JSON.stringify(response['datafile_json'], null, 4);
		return response;
	}else{
		return this.default;
	}
}
