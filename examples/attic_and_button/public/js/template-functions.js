/**
* This file exposes a handlebar template function for each template
*/

 // Object to hold all template functions
 
 var templateTabs = {
 	config_tab:  {
 		title: "Configuration", 
 		template_url: "templates/config-tab-content.hbs",
 		tab: true
 	},
 	visitor_tab: {
 		title: "Select Simulated Visitor",
 		template_url: "templates/select-visitor-content.hbs",
 		tab: false
 	},
 	shop_tab: {
 		title: "Shop",
 		template_url: "templates/shop-tab-content.hbs",
 		tab: true
 	}, 
 	messages_tab: {
 		title: "Messages (Log and Errors)",
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
		elements = elements.add("<li><a data-key="+key+" data-toggle='tab' href=#"+key+">"+value['title']+"</a></li>");
	}
});

$("#demo-tabs").html(elements);
$('#demo-tabs li:first').addClass('active');

