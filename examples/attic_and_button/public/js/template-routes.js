var currentTab = null;

var demo = new DemoController();

function loadTab(data) {
    $('#content').html(templateFunc[currentTab](data));
}

function buyNow(product_id){
    var response = true
    // $.ajax({
    //     type: "POST",
    //     url: "http://localhost:3001/cart/product",
    //     data: "productId="+product_id+"&num="+1,
    //     success: function(msg){
    //       alert( "Data Saved: " + msg );
    //     }
    // });
    if(response == true){
        alert( "Product added to cart!");
    }else{
        alert( "Some error;");
    }

};

$(window).on('load', function() {
    currentTab = Object.keys(templateFunc)[0];
    var productsData = demo.getProducts()
    loadTab(productsData);

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var target = $(e.target).attr("data-key"); // activated tab
        currentTab = target
        switch (currentTab) {
            case "home":
                var productsData = demo.getProducts()
                loadTab(productsData);
                // $('#content').prepend(templateFunc.visitor_tab(visitors));
                break;
            case "cart":
                var cartData = demo.getCartData()
                loadTab(cartData);
                break;
            case "checkout":
                var variation = {"variation": "two_step"}
                loadTab(variation);
                break;      
            case "messages":
                var messages = {"messages": demo.getMessages()}
                loadTab(messages);
                break;
        }
    });
});