function DemoController (params) {
    this.data = params;
    this.default = {"status": "001", "project_id": null, "event_key": null, "datafile_json": null, "experiment_key": null}
}

DemoController.prototype.getDemoConfig = function() {
    var JsonResponse = ValidateResponse(getConfigRequest()); // Sends GET /config Ajax request
    return JsonResponse;
};


DemoController.prototype.postDemoConfig = function() {
    var JsonResponse = ValidateResponse(setConfigRequest(this.data)); // Sends POST /config Ajax request
    return JsonResponse;
};

DemoController.prototype.getProducts = function(){
	var JsonResponse = getProductsRequest(); // Sends GET /products Ajax request
	return JsonResponse;
}

DemoController.prototype.selectVisitor = function(visitor){
	var JsonResponse = selectVisitorRequest(visitor); // Sends POST /visitor Ajax request
	return JsonResponse;
}

// DemoController.prototype.getProducts = function(){
// 	var JsonResponse = getProductsRequest(); // Sends GET /products Ajax request
// 	return JsonResponse;
// }

function ValidateResponse(response){
	if (typeof response != 'undefined'){
		response['datafile_json'] = JSON.stringify(response['datafile_json'], null, 4);
		return response;
	}else{
		return this.default;
	}
}