sap.ui.define([
	"sap/ui/core/UIComponent",
	"sap/ui/Device",
	"thingkathon/cobweb_sapui5/model/models",
	"sap/ui/core/IconPool"
], function (UIComponent, Device, models, IconPool) {
	"use strict";

	return UIComponent.extend("thingkathon.cobweb_sapui5.Component", {

		metadata: {
			manifest: "json"
		},

		/**
		 * The component is initialized by UI5 automatically during the startup of the app and calls the init method once.
		 * @public
		 * @override
		 */
		init: function () {
			this.registerFont();
			// call the base component's init function
			UIComponent.prototype.init.apply(this, arguments);

			// enable routing
			//this.getRouter().initialize();
			
			// set the device model
			this.setModel(models.createDeviceModel(), "device");
		},
		registerFont: function(){
		    var aFontLoaded = [],
		        aFontNames = ["SAP-icons"];
		     
		    var oVersionInfo = sap.ui.getVersionInfo();        
		    var oVersionModel = new sap.ui.model.json.JSONModel({
		        isOpenUI5: oVersionInfo && oVersionInfo.gav && /openui5/i.test(oVersionInfo.gav)
		    });
		    IconPool.registerFont({
		        fontFamily: "SAP-icons-TNT",
		        fontURI: jQuery.sap.getModulePath("sap.tnt.themes.base.fonts")
		    });
		     
		    aFontLoaded.push(IconPool.fontLoaded("SAP-icons-TNT"));
		    aFontNames.push("SAP-icons-TNT");
		     
		    if (!oVersionModel.getProperty("/isOpenUI5")) {
		        // register BusinessSuiteInAppSymbols icon font
		        IconPool.registerFont({
		            fontFamily: "BusinessSuiteInAppSymbols",
		            fontURI: jQuery.sap.getModulePath("sap.ushell.themes.base.fonts")
		        });
		        aFontLoaded.push(IconPool.fontLoaded("BusinessSuiteInAppSymbols"));
		        aFontNames.push("BusinessSuiteInAppSymbols");
		    }
		}
	});
});