(function () {
    'use strict';

    angular.module('app.main')
        .controller("MainCtrl", MainCtrl);

    /* @ngInject */
    function MainCtrl($scope) {

        $scope.vm = {};

        var vm = $scope.vm;
    }

})();