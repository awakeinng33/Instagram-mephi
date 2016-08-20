var appFollowers;

appFollowers = angular.module('appFollowers', ['appApi','authApp']);

appFollowers.config(['$httpProvider', function($httpProvider){
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      //  $httpProvider.defaults.headers.get['Accept']='application/json'
    }]);

appFollowers.controller('followersController',['$scope','ShowFollowers','ShowFollowing','AuthUser','api',
    function($scope,ShowFollowers,ShowFollowing,AuthUser,api) {
        window.onload = function() {
            var username = document.getElementById("title_user").innerText;
            $scope.auth_user = AuthUser.get();
            if (location.pathname.indexOf('/following')!= -1) {
                $scope.following = ShowFollowing.get({username: username});
            }
            else {
                $scope.followers = ShowFollowers.get({username:username});
            }
        };

         $scope.logout = function(){
            api.auth_logout.logout(function(){
                $scope.user = undefined;
                document.location.href ='/';
            });
        };
}]);

