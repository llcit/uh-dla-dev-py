from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dlasite.views import HomeView, CollectionListView, CollectionView, ItemView
from oaiharvests.views import HarvesterCommunityListView, HarvesterCommunityView, HarvesterCollectionView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^collections/$', CollectionListView.as_view(), name='collection_list'),
    url(r'^collection/(?P<pk>\d+)$', CollectionView.as_view(), name='collection'),
    url(r'^item/(?P<pk>\d+)$', ItemView.as_view(), name='item'),

	url(r'^harvest/repositories/$', HarvesterCommunityListView.as_view(), name='repo_list'),
    url(r'^harvest/repository/(?P<pk>\w+)$', HarvesterCommunityView.as_view(), name='repo'),
    url(r'^harvest/collect/$', HarvesterCollectionView.as_view(), name='collect'),
    
    url(r'^admin/', include(admin.site.urls)),
)
