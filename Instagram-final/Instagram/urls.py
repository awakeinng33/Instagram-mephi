from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from api.api import FeedView, FollowersView, FollowingView
from api.api import Register, UserDetail
from api.urls import chat_urls

urlpatterns = patterns('',

    url(r'^api/', include('api.urls')),
    url(r'^messages/', include(chat_urls)),
    url(r'^users/(?P<username>[0-9a-zA-Z_-]+)$', UserDetail.as_view(),),
    url(r'^register/res', Register.as_view()),
    url(r'^register', 'api.api.RegisterView'),
    url(r'^success', 'api.api.register_success'),
    url(r'^confirm/(?P<activation_key>\w+)$', 'api.api.register_confirm'),
    url(r'^search', 'api.api.SearchUsersView'),
    url(r'^allphotos', 'api.api.AllPhotosView'),
    url(r'^feed$', FeedView.as_view()),
    url(r'^followers/(?P<username>[0-9a-zA-Z_-]+)$', FollowersView.as_view()),
    url(r'^following/(?P<username>[0-9a-zA-Z_-]+)$', FollowingView.as_view()),
    url(r'^admin', include(admin.site.urls)),
    url(r'^$', 'api.api.IndexView')
)

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns('',
        url(r'^(?P<path>favicon\..*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:], 'django.contrib.staticfiles.views.serve', dict(insecure=True)),
    )