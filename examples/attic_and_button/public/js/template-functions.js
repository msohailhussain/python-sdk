/**
* This file exposes a handlebar template function for each template
*/

Handlebars.registerHelper('ifCond', function(v1, v2, options) {
  if(v1 === v2) {
    return options.fn(this);
  }
  return options.inverse(this);
});


function loadTemplate(file, data, element){
    getTemplate(
        file, data
    ).done(function(data){
        element.html(data);
    });
};

function getTemplate( name,data){
  var d=$.Deferred();

  $.get(name,function(response){

    var template = Handlebars.compile(response);
    d.resolve(template(data))
  });

  return d.promise();
}
 

var layoutTemplates = {
	"profile": "templates/profile-content.hbs",
	"flash-message": "templates/flash-message.hbs"
}


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
