
var app;

app = angular.module('appApi', ['ngResource']);

 app.factory('User', [
'$resource', function($resource) {
    return $resource('/users/:username',{username:'@username'},{
        get: { method: 'GET', isArray: false}
        });
    }
]);

 app.factory('UserPhoto', [
'$resource','$location', function($resource,$location) {
    return $resource( '/api' +location.pathname +'/photos',{},{
        get: { method: 'GET', isArray: false}
        });
    }
]);

 app.factory('UserList', [
'$resource', function($resource) {
    return $resource('/api/users',{},{
        get: { method: 'GET', isArray: false}
        });
    }
]);

 app.factory('UserDetail', [
'$resource', function($resource) {
    return $resource('/api/users/getuserdetail/:username',{username:'@username'},{
        get: { method: 'GET', isArray: false}
        });
    }
]);


 app.factory('Follow', [
'$resource', function($resource) {
    if ((location.pathname == '/allphotos')||(location.pathname == '/search')) {
        return 0;
    }
    else{
        var username = document.getElementById("username").innerText;
        var uri = '/api/users/add/'+username;
        return $resource(uri,{},{
        put: { method: 'PUT', isArray: false}
        });
    }
    }
]);


 app.factory('DeleteFollow', [
'$resource', function($resource) {
    if ((location.pathname == '/allphotos')||(location.pathname == '/search')) {
        return 0;
    }
    else{
        var username = document.getElementById("username").innerText;
        var uri = '/api/users/delete/'+username;
        return $resource(uri,{},{
            delete: { method: 'DELETE', isArray: false}
        });
    }
    }
]);


app.factory('AddComment',[
    '$resource', function($resource){
        return $resource('/api/comment/addcomment/:id/:user_id',{id:'@id',user_id:'@user_id'},{
            post:{method:'POST',isArray:false}
        })
    }
]);


app.factory('GetAllComments', [
'$resource', function($resource) {
    return $resource('/api/comment/getallcomments/:username',{username:'@username'},{
        get: { method: 'GET', isArray: false}
        });
    }
]);

app.factory('GetAllCommentsSinglePhoto', [
'$resource', function($resource) {
    return $resource('/api/comment/getallcomments/photo/:id',{id:'@id'},{
        get: { method: 'GET', isArray: false}
        });
    }
]);

app.factory('GetNewComment', [
'$resource', function($resource) {
    return $resource('/api/comment/getnewcomment/:id',{id:'@id'},{
        get: { method: 'GET', isArray: false}
        });
    }
]);

app.factory('AddPhoto',[
    '$resource', function($resource){
        return $resource('/api/photos/addphoto/:id',{id:'@id'},{
            post:{method:'POST',isArray:false}
        })
    }
]);

app.factory('GetNewPhoto',[
    '$resource', function($resource){
        return $resource('/api/photos/getnewphoto/:id',{id:'@id'},{
            get:{method:'GET',isArray:false}
        })
    }
]);

app.factory('DeletePhoto',[
    '$resource', function($resource){
        return $resource('/api/photos/deletephoto/:image_id',{image_id:'@image_id'},
            {delete:{method:'DELETE',isArray:false}
        })
    }
]);

app.factory('AllPhotos',[
    '$resource', function($resource){
        return $resource('/api/photos/getallphotos',{},
            {get:{method:'GET',isArray:false}
        })
    }
]);

 app.factory('AuthUser', [
'$resource', function($resource) {
    return $resource('/api/users/get_auth_user',{},{
        get: { method: 'GET', isArray: false}
        });
    }
]);

app.factory('LogoutUser', [
'$resource', function($resource) {
    return $resource('/api/auth/logout',{}, {
        delete: {method: 'DELETE'}
    });
    }
]);

 app.factory('Feed', [
'$resource', function($resource) {
    return $resource('/api/users/feed/:username/:page',{username:'@username',page:'@page'},{
        get: { method: 'GET', isArray: false}
        });
    }
]);

 app.factory('ShowFollowers', [
'$resource', function($resource) {
    return $resource('/api/users/:username/followers',{username:'@username'},{
        get: { method: 'GET', isArray: false}
        });
    }
]);

 app.factory('ShowFollowing', [
'$resource', function($resource) {
    return $resource('/api/users/:username/following',{username:'@username'},{
        get: { method: 'GET', isArray: false}
        });
    }
]);

