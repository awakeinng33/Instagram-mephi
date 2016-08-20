
var appFeed;

appFeed = angular.module('appFeed', ['appApi','authApp']);

appFeed.config(['$httpProvider', function($httpProvider){
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      //  $httpProvider.defaults.headers.get['Accept']='application/json'
    }]);

appFeed.controller('feedController',['$scope','$http','Feed','AuthUser','AddComment','GetAllComments','GetNewComment','api',
    function($scope,$http,Feed,AuthUser,AddComment,GetAllComments,GetNewComment,api) {

        $scope.photo_list=[];
        var auth_user;
        var count = 0;
        $scope.buttonload = false;
        $scope.new_comments = [];
        $scope.likecount=[];
        $scope.dislikecount=[];
        $scope.likename=[];
        $scope.dislikename=[];

        window.onload = function() {
            $scope.auth_user = AuthUser.get();
            auth_user = $scope.getAuthUser();
            Feed.get({username:auth_user,page:count})
                .$promise
                  .then(function(results){
                    if(results.results.length == 0){
                        $scope.buttonload = true;
                    }
                    $scope.photo_list = results.results;
                  });
            $scope.all_comments = GetAllComments.get({username:auth_user});
            count++;
        };

        $scope.loadPhoto = function(){
            Feed.get({username:auth_user,page:count})
                .$promise
                  .then(function(results){
                        if(results.results.length == 0){
                            $scope.buttonload = true;
                            }
                        $scope.photo_list = $scope.photo_list.concat(results.results);
                  });
            count++;
        };

        $scope.canShowComment = function(photo_id,comment_photo_id){
            return comment_photo_id==photo_id;
        };

        $scope.getAuthUser = function() {
            return document.getElementById("buttonprofiletext").innerText;
        };


        $scope.addComment = function (photo_id,comment,auth_user) {
            document.getElementById('commentform'+photo_id).reset();
            var today = new Date();
            $scope.added_comment = AddComment.post({id:photo_id,user_id:auth_user.id},
                {comment:comment,username:auth_user.username, data:today})
                .$promise
                    .then(function(comment){
                        $scope.new_comment_id = comment.id;
                        $scope.new_comment = GetNewComment.get({id:$scope.new_comment_id});
                        $scope.new_comments.push($scope.new_comment);
                        setTimeout(shiftScroll,200,photo_id);
                  }).catch(function(data){
                        if (data.data.detail !=null)
                            alert('Запрос можно отправлять не чаще чем 20 раз в день!');
                        else
                            alert('Убедитесь что в этом поле не больше 200 символов.');
                  });

          };

        function shiftScroll(photo_id) {
            var block = document.getElementById('allcomments'+photo_id);
            block.scrollTop = block.scrollHeight;
        }

        $scope.addLike = function(photo_id,state){
            var code=0;

            $http.post('/api/photos/addlike/'+photo_id+'/'+state).then(function(request){
                code = request.data;
                $scope.likecount[photo_id]=code[0];
                $scope.dislikecount[photo_id]=code[1];

            $http.get('/api/photos/show/userliked/' + photo_id ).success(function (data) {
                $scope.likename[photo_id] = data.results;
                $http.get('/api/photos/show/userdisliked/' + photo_id ).success(function (data) {
                    $scope.dislikename[photo_id] = data.results;
                });
            });
        });
        };

        $scope.redirectOnUserProfile = function(username){
            document.location.href = '/users/' + username;
        };

        $scope.logout = function(){
            api.auth_logout.logout(function(){
                $scope.user = undefined;
                document.location.href ='/';
            });
        };

        $scope.openmore = function(photo_id) {
            var block;

            $(".likes").each(function () {
                        if (photo_id == parseInt($(this).attr("id"))) {
                            block = $(this).next();
                        }
                    }
                );
            $http.get('/api/photos/show/userliked/' + photo_id ).success(function (data) {
                $scope.likename[photo_id] = data.results;
                $http.get('/api/photos/show/userdisliked/' + photo_id ).success(function (data) {
                    $scope.dislikename[photo_id] = data.results;
                    block.slideToggle();
                });
            });
        }
}]);


