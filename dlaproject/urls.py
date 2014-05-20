from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dlasite.views import HomeView, CollectionListView, CollectionView, ItemView
from oaiharvests.views import HarvesterView, HarvesterAddRepoView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^collections/$', CollectionListView.as_view(), name='collection_list'),
    url(r'^collection/(?P<pk>\d+)$', CollectionView.as_view(), name='collection'),
    url(r'^item/(?P<pk>\d+)$', ItemView.as_view(), name='item'),

    url(r'^harvester/collector/$', HarvesterAddRepoView.as_view(), name='collector'),
    url(r'^harvester/(?P<set>\w+)$', HarvesterView.as_view(), name='harvester'),
    
    url(r'^admin/', include(admin.site.urls)),
)
