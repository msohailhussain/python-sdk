/**
* This file exposes a handlebar template function for each template
*/

 // Object to hold all template functions
 
 var templateTabs = {
 	home:  {
 		title: "Home", 
 		template_url: "templates/home-content.hbs",
 		tab: true
 	},
 	cart: {
 		title: "Cart",
 		template_url: "templates/cart-content.hbs",
 		tab: true
 	},
 	checkout: {
 		title: "Payment",
 		template_url: "templates/checkout-content.hbs",
 		tab: true
 	}, 
 	messages: {
 		title: "Messages",
 		template_url: "templates/logs-tab-content.hbs",
 		tab: true
 	}
 }; 

 var templateFunc = {};
 var elements = $();


// Append dynamic tabs and generates associated template functions

$.each( templateTabs, function( key, value ) {
	$.ajax({
	  url: value['template_url'],
	  success: function (tpl){
	    templateFunc[key]=Handlebars.compile(tpl);},
	    async:false
	});
	
	if(value['tab']){
		elements = elements.add("<li class='nav-item'><a class='nav-link' data-key="+key+" data-toggle='tab' href=#"+key+">"+value['title']+"</a></li>");
	}
});

$("#demo-tabs").html(elements);
$('#demo-tabs li:first a').addClass('active');


Handlebars.registerHelper('ifIsBuyNow', function(value, options) {
  if(value === 'buy_now') {
    return true
  }
  return false
});