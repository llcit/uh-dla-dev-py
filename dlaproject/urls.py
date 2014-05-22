from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dlasite.views import HomeView, CollectionListView, CollectionView, ItemView
from oaiharvests.views import  (
	HarvesterCommunityListView, 
	HarvesterRegistrationView, 
	HarvesterCollectionView, 
	HarvesterCommunityView,
	HarvestRecordsView)

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^collections/$', CollectionListView.as_view(), name='collection_list'),
    url(r'^collection/(?P<pk>\d+)$', CollectionView.as_view(), name='collection'),
    url(r'^item/(?P<pk>\d+)$', ItemView.as_view(), name='item'),

	url(r'^harvest/repositories/$', HarvesterCommunityListView.as_view(), name='repo_list'),
    url(r'^harvest/register/(?P<pk>\w+)$', HarvesterRegistrationView.as_view(), name='register_comm'),
    url(r'^harvest/community/(?P<pk>\w+)$', HarvesterCommunityView.as_view(), name='community'),
    # url(r'^harvest/collection/(?P<pk>\w+)$', HarvesterCollectionView.as_view(), name='collection'),
    url(r'^harvest/collection/(?P<pk>\w+)$', HarvestRecordsView.as_view(), name='harvest'),
    
    url(r'^admin/', include(admin.site.urls)),
)
