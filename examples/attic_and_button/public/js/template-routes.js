var currentTab = null;
var currentUser = null;
var demo = new DemoController();

function loadTab(data) {
    $('#content').html(templateFunc[currentTab](data));
}

$( "#loginForm" ).submit(function( event ) {
    event.preventDefault();
    var param = "userId="+$("#exampleInputEmail1").val();
    var demo = new DemoController(param);
    loginResponse = demo.loginUser()
    if(loginResponse){
        var user = getCurrentUser()
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
    logoutResponse = demo.logoutUser()
    if(logoutResponse){
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
    demo = new DemoController(params);
    var response = demo.addToCart()
    var message = {"message": (response ? "Product added to cart!" : "Failed to add product into cart!")};
    loadTemplate(
        layoutTemplates['flash-message'], 
        message, $('#flashMessage')
    );
};

function checkout(){
    currentTab = Object.keys(templateFunc)[2];
    $( "a[data-key="+currentTab+"]" ).click();
}

function clearMessages() {
  if (confirm("Click OK to continue?")){
    demo.clearMessages()
    var messages = {"messages": demo.getMessages()}
    loadTab(messages);
  }
};

$(window).on('load', function() {
    
    // Load Profile Section
    var user = getCurrentUser()
    currentUser = {"userName": ((user == 'null') ? null : user)};
    loadTemplate(
        layoutTemplates['profile'], 
        currentUser, $('#profileContent')
    );
    currentTab = Object.keys(templateFunc)[0];
    var productsData = demo.getProducts()
    loadTab(productsData);

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        $('#flashMessage').html("");
        var target = $(e.target).attr("data-key"); // activated tab
        currentTab = target
        switch (currentTab) {
            case "home":
                var productsData = demo.getProducts()
                loadTab(productsData);
                break;
            case "cart":
                var cartData = demo.getCartData()
                loadTab(cartData);
                break;
            case "checkout":
                loadTab(demo.checkoutCart());
                break;      
            case "messages":
                var messages = {"messages": demo.getMessages()}
                loadTab(messages);
                break;
        }
    });
});