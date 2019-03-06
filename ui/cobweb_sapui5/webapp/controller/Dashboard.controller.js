sap.ui.define([
	"thingkathon/cobweb_sapui5/controller/BaseController"
], function (Controller) {
	"use strict";

	return Controller.extend("thingkathon.cobweb_sapui5.controller.Dashboard", {
		onInit: function () {
			var oChart = this.byId("idVizFrame");
			
			oChart.setVizProperties({ 'title':{ 'text': 'Energy Consumption'}});
			oChart.setVizProperties({"valueAxis": { "title": {"text": "Consumption in kWh"}}});
			oChart.setVizProperties({"timeAxis": { "title": {"text": "Date"}}});
		},
		
		onTilePress: function(oEvent) {
			var sId = oEvent.getParameter("id");
			
			if (sId.indexOf("profit") !== -1) {
				this.getRouter().navTo("ProfitRoute");
			} else if (sId.indexOf("apartmentConsumption") !== -1) {
				this.getRouter().navTo("ApartmentConsumptionRoute");
			} else if (sId.indexOf("storageChargeStatus") !== -1) {
				this.getRouter().navTo("ChargeStatusStorageRoute");
			}
		},
		
		
	});
});