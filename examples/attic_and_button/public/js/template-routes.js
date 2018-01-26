var currentTab = null;
var currentUser = null;

function loadTab(data) {
    $('#content').html(templateFunc[currentTab](data));
}

$( "#loginForm" ).submit(function( event ) {
    event.preventDefault();
    var param = "userId="+$("#exampleInputEmail1").val();
    if(loginUserRequest(param)){
        var user = getCurrentUserRequest()
        currentUser = {"userName": ((user == 'null') ? null : user)};
        loadTemplate(
            layoutTemplates['profile'], 
            currentUser, $('#profileContent')
        );
        $('#exampleModal').modal('hide');
    }else{
        alert("Invalida email!");
    }
});

function logoutSession() {
    if(logoutUserRequest()){
        currentTab = Object.keys(templateFunc)[0];
        $( "a[data-key="+currentTab+"]" ).click();
        loadTemplate(
            layoutTemplates['profile'], 
            null, $('#profileContent')
        );
    }else{
        alert("Failed!");
    }
};

function addToCart(product_id, qty) {
    var params = "productId="+product_id+"&num="+qty,
    jsonResponse = addToCartRequest(params);
    var message = {"message": (jsonResponse ? "Product added to cart!" : "Failed to add product into cart!")};
    loadTemplate(
        layoutTemplates['flash-message'], 
        message, $('#flashMessage')
    );
};

function clearCart() {
  if (confirm("Are you sure? want to delete all items!")){
    clearCartRequest()
    loadTab(getCartDataRequest());
  }
};

function checkout(){
    currentTab = Object.keys(templateFunc)[2];
    $( "a[data-key="+currentTab+"]" ).click();
};

function clearMessages() {
  if (confirm("Click OK to continue?")){
    clearMessagesRequest()
    var messages = {"messages": getMessagesRequest()}
    loadTab(messages);
  }
};

$(window).on('load', function() {
    
    // Load Profile Section
    var user = getCurrentUserRequest()
    currentUser = {"userName": ((user == 'null') ? null : user)};
    loadTemplate(
        layoutTemplates['profile'], 
        currentUser, $('#profileContent')
    );
    currentTab = Object.keys(templateFunc)[0];
    loadTab(getProductsRequest());

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        $('#flashMessage').html("");
        var target = $(e.target).attr("data-key"); // activated tab
        currentTab = target
        switch (currentTab) {
            case "home":
                loadTab(getProductsRequest());
                break;
            case "cart":
                loadTab(getCartDataRequest());
                break;
            case "checkout":
                loadTab(checkoutCartRequest());
                break;      
            case "messages":
                var messages = {"messages": getMessagesRequest()}
                loadTab(messages);
                break;
        }
    });
});