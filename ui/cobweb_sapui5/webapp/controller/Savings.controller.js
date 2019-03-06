sap.ui.define([
	"thingkathon/cobweb_sapui5/controller/BaseController"
], function (Controller) {
	"use strict";

	return Controller.extend("thingkathon.cobweb_sapui5.controller.Savings", {
		onInit: function () {
			var oChart = this.byId("idVizFrame");
			
			oChart.setVizProperties({ 'title':{ 'text': 'Savings - Postplatz 1 in 01067'}});
			oChart.setVizProperties({"valueAxis": { "title": {"text": "Savings"}}});
			oChart.setVizProperties({"timeAxis": { "title": {"text": "Month"}}});
		},
		
		onSelectionChange: function(oEvent) {
			
		}
	});
});