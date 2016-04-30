(function () {
    'use strict';

    function portfolioCardCtrl() {

    }

    angular.module('app.main')
        .component("portfolioCard", {
            templateUrl: 'views/_components/portfolioCard.html',
            controller: portfolioCardCtrl,
            bindings: {
                portfolios:  '='
            }
        });

})();