/* global QUnit */
QUnit.config.autostart = false;

sap.ui.getCore().attachInit(function () {
	"use strict";

	sap.ui.require([
		"thingkathon/cobweb_sapui5/test/integration/AllJourneys"
	], function () {
		QUnit.start();
	});
});