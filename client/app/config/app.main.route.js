(function () {
    'use strict';

    angular.module('app.main').config(mainConfig);

    /* @ngInject */
    function mainConfig($stateProvider, $urlRouterProvider) {

        $stateProvider
            .state('main', {
                url: '/',
                templateUrl: 'views/main.html'
            })
            .state('portfolio', {
                url: '/portfolio',
                templateUrl: 'views/pages/portfolio.html'
            })
            .state('whoami', {
                url: '/whoami',
                templateUrl: 'views/pages/whoami.html'
            })
            .state('contact', {
                url: '/contact',
                templateUrl: 'views/pages/contact.html'
            });

        $urlRouterProvider.otherwise('/');

    }
})();