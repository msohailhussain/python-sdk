var currentTab = null;

var demo = new DemoController();

var visitors = {
    "visitors": [{id: 1, name: "John"}, {id: 2, name: "Ross"}]
};

function loadTab(data) {
    $('#content').html(templateFunc[currentTab](data));
}

function sumitConfig(){
    currentTab = Object.keys(templateFunc)[0];
    var data = $("#new_config").serialize();
    demo = new DemoController(data);
    var configdata = demo.postDemoConfig();
    loadTab(configdata);
};

function selectVisitor(){
    var selectedVisitor = {user_id: $("#select_visitor option:selected").val()};
    var configdata = demo.selectVisitor(selectedVisitor);
    loadTab(configdata);
    $('#content').prepend(templateFunc.visitor_tab(visitors));
}

$(window).on('load', function() {
    currentTab = Object.keys(templateFunc)[0];
    var configdata = demo.getDemoConfig();
    loadTab(configdata);
    
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var target = $(e.target).attr("data-key"); // activated tab
        currentTab = target
        switch (currentTab) {
            case "config_tab":
                var configdata = demo.getDemoConfig();
                loadTab(configdata);
                break;
            case "shop_tab":
                var products = {"products": demo.getProducts()};
                loadTab(products);
                $('#content').prepend(templateFunc.visitor_tab(visitors));
                break;
            case "messages_tab":
                outmsg = "no ink";
                genmsg = true;
                mailmsg = true;
                phonemsg = false;
                break;
        }
    });

    sumitConfig();

});