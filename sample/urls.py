from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'uploader.views.main', name='main'),
    url(r'^login/$', 'uploader.views.login', name='login'),
    url(r'^verify/$', 'uploader.views.verify', name='verify'),
    url(r'^list_videos/$', 'uploader.views.list_videos', name='list_videos'),
    url(r'^addvideo/$', 'uploader.views.addvideo', name='addvideo'),
    url(r'^cache/$', 'uploader.views.cache', name='cache'),
    url(r'^(?P<file2delete>[\w|\W]+)/checking/(?P<id2delete>[\w|\W]+)$', 'uploader.views.listoriginal', name='listoriginal'),
    url(r'^cdndatabase/$', 'uploader.views.cdndatabase', name='cdndatabase'),
    url(r'^logout/$', 'uploader.views.logout', name='logout'),
    url(r'^streamer/$', 'uploader.views.streamer', name='streamer'),
    )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
