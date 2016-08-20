from django.conf.urls import patterns, url, include
from .api import UserList, UserPhotoList, UserDetailForReturnJson, AuthUser, AddAvatar, FeedPhotoList,\
    AddFollowing, DeleteFollowing, FollowingList, FollowersList
from .api import PhotoDetail, AddPhoto, GetNewPhoto, DeletePhoto, AddLike, AllRandomPhotos
from .api import GetAllCommentsSinglePhoto, GetAllComments, GetNewComment, AddComment, LikesUsername, DislikesUsername
from .api import LogoutView, LoginView, RegisterWithoutMail



user_urls = patterns('',

    url(r'^/getuserdetail/(?P<username>[0-9a-zA-Z_-]+)$', UserDetailForReturnJson.as_view()),
    url(r'^/get_auth_user$', AuthUser.as_view()),
    url(r'^/addavatar$', AddAvatar.as_view()),
    url(r'^/feed/(?P<username>[0-9a-zA-Z_-]+)/(?P<page>\d+)$', FeedPhotoList.as_view()),
    url(r'/add/(?P<username>[0-9a-zA-Z_-]+)$', AddFollowing.as_view()),
    url(r'/delete/(?P<username>[0-9a-zA-Z_-]+)$', DeleteFollowing.as_view()),
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/photos$', UserPhotoList.as_view(), name='userphoto-list'),
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/following$', FollowingList.as_view(),),
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/followers$', FollowersList.as_view(),),
    url(r'^$', UserList.as_view(),)
)


photo_urls = patterns('',
    url(r'^/getallphotos', AllRandomPhotos.as_view()),
    url(r'^/addphoto/(?P<user_id>\d+)$', AddPhoto.as_view()),
    url(r'^/getnewphoto/(?P<pk>\d+)$', GetNewPhoto.as_view()),
    url(r'^/deletephoto/(?P<image_id>\d+)$', DeletePhoto.as_view()),
    url(r'^/addlike/(?P<image_id>\d+)/(?P<state>[0-1]+)$', AddLike.as_view()),
    url(r'/show/userliked/(?P<image>\d+)$', LikesUsername.as_view()),
    url(r'/show/userdisliked/(?P<image>\d+)$', DislikesUsername.as_view()),
    url(r'^/(?P<pk>\d+)$', PhotoDetail.as_view(),),

)
comment_urls = patterns('',
    url(r'^/getallcomments/photo/(?P<id>\d+)$', GetAllCommentsSinglePhoto.as_view()),
    url(r'^/getallcomments/(?P<username>[0-9a-zA-Z_-]+)$', GetAllComments.as_view()),
    url(r'^/getnewcomment/(?P<pk>\d+)$', GetNewComment.as_view()),
    url(r'^/addcomment/(?P<image_id>\d+)/(?P<user_id>\d+)$', AddComment.as_view()),
    )

auth_urls = patterns('',
       url(r'/login$', LoginView.as_view(),),
       url(r'/logout$', LogoutView.as_view(), ),
       url(r'^registerwithoutmail', RegisterWithoutMail.as_view()),
       url(r'^$', 'api.api.AuthView',)
)

chat_urls = patterns('api.views',
    url(r'^send_message/$', 'send_message_view'),
    url(r'^send_message_api/(?P<thread_id>\d+)/$', 'send_message_api_view'),
    url(r'^chat/(?P<thread_id>\d+)/$', 'chat_view'),
    url(r'^$', 'messages_view'),
)

urlpatterns = patterns('',

    url(r'^users', include(user_urls)),
    url(r'^comment', include(comment_urls)),
    url(r'^photos', include(photo_urls)),
    url(r'^auth', include(auth_urls)),
)
