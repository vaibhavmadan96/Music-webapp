from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.index,name='index'),

	url(r'^register/$',views.UserFormView.as_view(),name='register'),

	url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

	url(r'^(?P<album_id>[0-9]+)/$',views.detail,name='detail'),

	url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),

	#music/album/add
	url(r'album/add/$',views.create_album,name='album-add'),

	# #music/album/2/
	# url(r'album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name='album-update'),

	url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),	

	#music/album/2/delete
	url(r'album/(?P<album_id>[0-9]+)/delete/$',views.delete_album,name='album-delete'),
]