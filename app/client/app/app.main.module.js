(function () {
    'use strict';

    var sampleAppModuleName = "app.main";

    angular.module(sampleAppModuleName,['ui.router', 'ngAnimate', 'ngTouch',  'ngMessages']);

    angular.element(document).ready(function () {
        angular.bootstrap(document, [sampleAppModuleName]);
    });

})();