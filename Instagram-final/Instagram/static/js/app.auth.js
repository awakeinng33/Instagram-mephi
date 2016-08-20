angular.module('authApp', ['ngResource','ngRoute','appApi']).
    config(['$httpProvider', function($httpProvider){

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.headers.common['Accept']= 'application/json';
      //  $httpProvider.defaults.headers.common['Allow']='GET, POST, DELETE, PUT';

    }]).
    factory('api', function($resource){
        function add_auth_header(data, headersGetter){
            // логин и пароль должны быть закодированы в base64 в по правилам HTTP
            var headers = headersGetter();
            headers['Authorization'] = ('Basic ' + btoa(data.username +
                                        ':' + data.password));
        }

        return {
            auth_login: $resource('/api/auth/login', {}, {
                login: {method: 'POST', transformRequest: add_auth_header}
            }),
            auth_logout: $resource('/api/auth/logout', {}, {
                logout: {method: 'DELETE'}
            }),
            users: $resource('/register/res', {}, {
                create: {method: 'POST'}
            })
        };
    }).
    controller('authController', function($scope,User,api) {

        $('#id_auth_form input').checkAndTriggerAutoFillEvent();


        $scope.getCredentials = function(){
            return {username: $scope.username, password: $scope.password};
        };

        $scope.getCredentialsForRegister = function(){
            return {username: $scope.username, password: $scope.password, email:$scope.email};
        };

        $scope.login = function(){
            api.auth_login.login($scope.getCredentials()).
                $promise.
                    then(function(data){
                        document.location.href ='/users/'+data.username;
                    }).
                    catch(function(data){
                        alert(data.data.detail);
                    });
        };

        $scope.register = function($event){
            $event.preventDefault();
            api.users.create($scope.getCredentialsForRegister()).
                $promise.
                    then(function(){
                    document.location.href = '/success';
                }).
                    catch(function(data){
                        alert(data.data.username);
                    });
            };
    });
