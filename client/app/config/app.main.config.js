(function () {
    'use strict';

    var sampleAppModuleName = "app.main";

    angular.module(sampleAppModuleName).config(appConfig);

    /* @ngInject */
    function appConfig($httpProvider) {

        var headers = $httpProvider.defaults.headers;

        headers.common = {};
        headers.post = {};
        headers.put = {};
        headers.patch = {};
    }

})();