from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dlasite.views import HomeView, CollectionListView, CollectionView, ItemView
from oaiharvests.views import *

# (
# 	HarvesterCommunityListView,
# 	HarvesterRegistrationView,
# 	HarvesterCollectionView,
# 	HarvesterCommunityView,
# 	HarvestRecordsView

# )

urlpatterns = patterns('',
                       url(r'^$', HomeView.as_view(), name='home'),
                       url(r'^collections/$', CollectionListView.as_view(),
                           name='collection_list'),
                       url(r'^collection/(?P<pk>\d+)$',
                           CollectionView.as_view(), name='collection'),
                       url(r'^item/(?P<pk>\d+)$',
                           ItemView.as_view(), name='item'),

                    # Institutional Repositories #
                       url(r'^oaiharvester/$', RepositoryListView.as_view(),
                           name='repository_list'),

                       url(r'^oaiharvester/repository/add/$',
                           RepositoryCreateView.as_view(
                           ), name='repository_add'),
                       url(r'^oaiharvester/repository/edit/(?P<pk>\w+)$',
                           RepositoryUpdateView.as_view(
                           ), name='repository_edit'),
                       url(r'^oaiharvester/repository/delete/(?P<pk>\w+)$',
                           RepositoryDeleteView.as_view(
                           ), name='repository_delete'),
                       url(r'^oaiharvester/repository/(?P<pk>\w+)$',
                           RepositoryView.as_view(), name='repository'),

                    # Community Collections #
                       url(r'^oaiharvester/community/(?P<pk>\w+)$',
                           CommunityView.as_view(), name='community'),
                       url(r'^oaiharvester/community/add/(?P<pk>\w+)$',
                           CommunityCreateView.as_view(
                           ), name='community_add'),
                       url(r'^oaiharvester/community/edit/(?P<pk>\w+)$',
                           CommunityUpdateView.as_view(
                           ), name='community_edit'),
                       url(r'^oaiharvester/community/delete/(?P<pk>\w+)$',
                           CommunityDeleteView.as_view(
                           ), name='community_delete'),

                    # Collections #
                       url(r'^oaiharvester/collection/(?P<pk>\w+)$',
                           CollectionView.as_view(), name='collection'),
                       url(r'^oaiharvester/collection/add/(?P<pk>\w+)$',
                           CollectionCreateView.as_view(
                           ), name='collection_add'),
                       url(r'^oaiharvester/collection/edit/(?P<pk>\w+)$',
                           CollectionUpdateView.as_view(
                           ), name='collection_edit'),
                       url(r'^oaiharvester/collection/delete/(?P<pk>\w+)$',
                           CollectionDeleteView.as_view(
                           ), name='collection_delete'),                      
                       url(r'^oaiharvester/collection/harvest/(?P<pk>\w+)$',
                           CollectionHarvestView.as_view(
                           ), name='harvest_collection'),


                       url(r'^admin/', include(admin.site.urls)),
                       )
