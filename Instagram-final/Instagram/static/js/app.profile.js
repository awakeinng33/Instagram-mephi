
var appPhoto;

appPhoto = angular.module('appProfile', ['appApi','angularFileUpload','authApp']);

appPhoto.config(['$httpProvider', function($httpProvider){
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      //  $httpProvider.defaults.headers.get['Accept']='application/json'
    }]);

  appPhoto.controller('profileController', [
    '$scope','$upload','$http','UserDetail','UserList', 'UserPhoto','AddComment','AddPhoto','GetNewPhoto','DeletePhoto','Follow','DeleteFollow','AuthUser','GetAllCommentsSinglePhoto','GetNewComment','AllPhotos','api',
      function($scope,$upload,$http,UserDetail,UserList, UserPhoto,AddComment,AddPhoto,GetNewPhoto,DeletePhoto,Follow,DeleteFollow,AuthUser,GetAllCommentsSinglePhoto,GetNewComment,AllPhotos,api) {

            window.onfocus = goSlide;
            window.onblur = stopSlide;

            $scope.photos_length;
            $scope.photo_likes = [];
            $scope.photo_comments = [];
            $scope.photo_dislikes = [];
            $scope.new_photos = [];
            $scope.new_comments = [];
            $scope.likecount=[];
            $scope.dislikecount=[];
            $scope.likename=[];
            $scope.dislikename=[];
            var int1,int2,int3,int4,int5,int6,int7;
            var flag1 = true, flag2 = true, flag3 = true, flag4 = true, flag5 = true, flag6 = true, flag7 = true;

            window.onload = function () {
                goSlide();
                if (location.pathname == '/allphotos'){
                    $scope.all_photos = AllPhotos.get();
                }
                else if (location.pathname== '/search'){
                    $scope.all_users = UserList.get();
                }
                else {
                    var user = document.getElementById("username").innerText;
                    $scope.user = UserDetail.get({username: user});
                    $scope.photos = UserPhoto.get()
                .$promise
                    .then(function(results){
                        $scope.photos = results.results;
                        $scope.photos_length = $scope.photos.length;
                  });
                }
                 AuthUser.get().$promise.then(function(data){
                     $scope.auth_user = data;
                 })
            };

            $scope.getDataForComment = function () {
                return {comment: $scope.comment};
            };

            $scope.refresh = function() {
                $scope.all_photos = AllPhotos.get();
            };

            $scope.AddFollowing = function () {
                Follow.put();
                document.getElementById("followerscount").innerText = (parseInt(document.getElementById("followerscount").innerText)+1);
                $("#signinclass").replaceWith('<a id="signoutclassref"><div class="buttonchange" id="signoutclass"><span id="signout">Отписаться</span></div></a>');
                $("#signoutclassref").bind('click',$scope.DeleteFollowing);
            };

            $scope.DeleteFollowing = function () {
                DeleteFollow.delete();
                document.getElementById("followerscount").innerText = (parseInt(document.getElementById("followerscount").innerText)-1);
                $("#signoutclassref").replaceWith('<a id="signinclass" ><div class="buttonchange" ><span id="follow">Подписаться</span> </div></a>');
                $("#signinclass").bind('click',$scope.AddFollowing);
            };

            $scope.delete = function(photo_id){
                for (var i = 0; i < $scope.new_photos.length; i++) {
                    if ($scope.new_photos[i].id == photo_id)
                        $scope.new_photos.splice(i, 1);
                }
                DeletePhoto.delete({image_id: photo_id});
                document.getElementById(photo_id).parentNode.remove();
                document.getElementById("fotocount").innerText = (parseInt(document.getElementById("fotocount").innerText)-1);
            };


            $scope.modalPhotoDelete = function(photo_id) {
                $(document).ready(function(){

                    $(".infog3").css("left", $(window).width() / 2-175);
                    $(".infog3").css("top", $(window).height() / 2-75);
                    $(".fog3").css("height", $(document).height());
                    $(".fog3").fadeIn("fast");
                    $(".body3").fadeIn("fast");

                    $(".body3,.button-close3,#input-close").click(function () {
                        $(".body3").fadeOut();
                        $(".fog3").fadeOut();
                    });

                    $scope.getPhotoId = function(){
                       return photo_id;
                    };

                    $("#input-delete").click(function () {
                        var id = $scope.getPhotoId();
                        $scope.delete(id);
                        $scope.photos_length--;
                        $(".body3").fadeOut();
                        $(".fog3").fadeOut();
                    });

                    $(".infog3").click(function () {
                        return false;
                  });
              })};

            $scope.RedirectToUserProfile = function(username){
                document.location.href = '/users/' +username;
            };

            $scope.logout = function(){
                api.auth_logout.logout(function(){
                    $scope.user = undefined;
                    document.location.href ='/';
                });
            };

            $scope.addAvatar = function(file){
                $scope.upload = $upload.upload({
                    url:'/api/users/addavatar',
                    method:'POST',
                    headers:{'Content-Type': file.type},
                    file:file
                }).progress(function (evt) {
                    console.log('percent: ' + parseInt(100.0 * evt.loaded / evt.total));
                }).success(function (data) {
                    $scope.user = data;
                    $scope.auth_user=data;
                }).error(function () {
                    alert("Файл не должен превышать 10Мб");
                });
            };

            function goSlide()
            {
                int1 = setInterval(function() {
                    if (flag1 === true) {
                        $("#blockLeftTopTop").fadeOut(500);
                        $("#blockLeftTopBottom").fadeIn(500);
                        flag1 = false;
                    }
                    else {
                        $("#blockLeftTopBottom").fadeOut(500);
                        $("#blockLeftTopTop").fadeIn(500);
                        flag1 = true;
                    }
                },32000);

                int2 = setInterval(function() {
                    if (flag2 === true)
                    {
                        $("#blockLeftBottomTop").fadeOut(500);
                        $("#blockLeftBottomBottom").fadeIn(500);
                        flag2 = false;
                    }
                    else {
                        $("#blockLeftBottomBottom").fadeOut(500);
                        $("#blockLeftBottomTop").fadeIn(500);
                        flag2 = true;
                    }
                },8000);

                int3 = setInterval(function() {
                    if (flag3 === true)
                    {
                        $("#blockLeftCenterTopTop").fadeOut(500);
                        $("#blockLeftCenterTopBottom").fadeIn(500);
                        flag3 = false;
                    }
                    else {
                        $("#blockLeftCenterTopBottom").fadeOut(500);
                        $("#blockLeftCenterTopTop").fadeIn(500);
                        flag3 = true;
                    }
                },12000);

                int4 = setInterval(function() {
                    if (flag4 === true)
                    {
                        $("#blockLeftCenterBottomTop").fadeOut(500);
                        $("#blockLeftCenterBottomBottom").fadeIn(500);
                        flag4 = false;
                    }
                    else {
                        $("#blockLeftCenterBottomBottom").fadeOut(500);
                        $("#blockLeftCenterBottomTop").fadeIn(500);
                        flag4 = true;
                    }
                },27000);

                int5 = setInterval(function() {
                    if (flag5 === true) {
                        $("#blockCenterTop").fadeOut(500);
                        $("#blockCenterBottom").fadeIn(500);
                        flag5 = false;
                    }
                    else {
                        $("#blockCenterBottom").fadeOut(500);
                        $("#blockCenterTop").fadeIn(500);
                        flag5 = true;
                    }
                },44000);

                int6 = setInterval(function() {
                    if (flag6 === true) {
                        $("#blockRightTopTop").fadeOut(500);
                        $("#blockRightTopBottom").fadeIn(500);
                        flag6 = false;
                    }
                    else {
                        $("#blockRightTopBottom").fadeOut(500);
                        $("#blockRightTopTop").fadeIn(500);
                        flag6 = true;
                    }
                },15000);

                int7 = setInterval(function() {
                    if (flag7 === true) {
                        $("#blockRightBottomTop").fadeOut(500);
                        $("#blockRightBottomBottom").fadeIn(500);
                        flag7 = false;
                    }
                    else {
                        $("#blockRightBottomBottom").fadeOut(500);
                        $("#blockRightBottomTop").fadeIn(500);
                        flag7 = true;
                    }
                },51000);
            }

            function stopSlide()
            {
                window.clearInterval(int1);
                window.clearInterval(int2);
                window.clearInterval(int3);
                window.clearInterval(int4);
                window.clearInterval(int5);
                window.clearInterval(int6);
                window.clearInterval(int7);
            }


            $scope.onFileSelect = function($files,avatar,id){
                var user_id = document.getElementById("user_id").innerText;
                if ($scope.auth_user.id != user_id){
                    return 1;
                }
                for (var i = 0;i < $files.length; i++) {
                    var file = $files[i];
                    if ((file.type == 'image/jpeg') || (file.type == 'image/png')) {
                        if (avatar) {
                            $scope.addAvatar(file);
                        }
                        else {
                                $scope.upload = $upload.upload({
                                    url: '/api/photos/addphoto/' + user_id,
                                    method: 'POST',
                                    headers: {'Content-Type': file.type},
                                    file: file
                                }).progress(function (evt) {
                                    console.log('percent: ' + parseInt(100.0 * evt.loaded / evt.total));
                                }).success(function (id) {
                                    $scope.new_photo = GetNewPhoto.get({id:id});
                                    $scope.new_photos.unshift($scope.new_photo);
                                    document.getElementById("fotocount").innerText = (parseInt(document.getElementById("fotocount").innerText) + 1);
                                    $scope.photos_length++;
                                    $scope.photo_dislikes[id] = 0;
                                    $scope.photo_likes[id] = 0;
                                    $scope.photo_comments[id] = 0;
                                }).error(function () {
                                    alert("Файл не должен превышать 5Мб");
                                });
                        }
                    }
                    else {
                        alert('Некорректный файл!');
                    }
                }
            };

            $scope.modal = function(image, likes, dislikes){
                $scope.bigPhoto = image;

                $(document).ready(function(){
                    $scope.all_comments_photo = GetAllCommentsSinglePhoto.get({id:image.id});
                    $(".fog").css("height", $(document).height());
                    $(".fog").fadeIn("slow");
                    $("html").css("overflow-y","hidden");
                    $("html").css("overflow-x","hidden");
                    $(".body2").fadeIn("slow");
                    $scope.likecount[image.id]=likes;
                    $scope.dislikecount[image.id]=dislikes;
                    $('#bigFotoUserInfoData').text(image.data);

                    $(".body2,.button-close").click(function(){
                        $(".body2").fadeOut();
                        $(".fog").fadeOut();
                        $("html").css("overflow-y","auto");
                        $("html").css("overflow-x","auto");
                        $(".alllikes").css("display","none");
                    });

                    $(".infog").click(function(){
                        return false;
                    });

                });
            };

            $scope.addLike = function(photo_id,state){
                var code=0;

                $http.post('/api/photos/addlike/'+photo_id+'/'+state).then(function(request){
                    code = request.data;
                    $scope.likecount[photo_id]=code[0];
                    $scope.photo_likes[photo_id] = code[0];
                    $scope.dislikecount[photo_id]=code[1];
                    $scope.photo_dislikes[photo_id] = code[1];

                    $http.get('/api/photos/show/userliked/' + photo_id ).success(function (data) {
                        $scope.likename[photo_id] = data.results;
                        $http.get('/api/photos/show/userdisliked/' + photo_id ).success(function (data) {
                            $scope.dislikename[photo_id] = data.results;
                        });
                    });
                });
            };

            $scope.openmore = function(photo_id) {
                var block;
                $(".bigFotoLikes").each(function () {
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
            };

            $scope.addComment = function (photo_id,comment,auth_user) {
                document.getElementById('commentform').reset();
                var today = new Date();
                $scope.added_comment = AddComment.post({id:photo_id,user_id:auth_user.id},
                       {comment:comment,username:auth_user.username, data:today})
                .$promise
                  .then(function(comment){
                    $scope.new_comment_id = comment.id;
                    $scope.new_comment = GetNewComment.get({id:$scope.new_comment_id});
                    $scope.new_comments.push($scope.new_comment);
                    $scope.photo_comments[photo_id]++;
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

      }]);



