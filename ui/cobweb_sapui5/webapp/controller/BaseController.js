sap.ui.define([
	"sap/ui/core/mvc/Controller",
	"sap/ui/core/UIComponent"
], function (Controller, UIComponent) {
	"use strict";

	return Controller.extend("thingkathon.cobweb_sapui5.controller.BaseController", {

		getRouter: function() {
            //return UIComponent.getRouterFor(this);  
        },
        navBack: function() {
        	//this.getRouter().navTo("DefaultRoute");                         
        }
		
	});
});