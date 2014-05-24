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

                       url(r'^oaiharvester/communities/(?P<pk>\w+)$',
                           RepositoryCommunityListView.as_view(
                           ), name='community_list'),
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

                       url(r'^oaiharvester/collection/(?P<pk>\w+)$',
                           CollectionView.as_view(), name='collection'),
                       url(r'^oaiharvester/collection/add$',
                           CollectionCreateView.as_view(
                           ), name='collection_create'),
                       url(r'^oaiharvester/collection/edit/(?P<pk>\w+)$',
                           CollectionUpdateView.as_view(
                           ), name='collection_edit'),
                       url(r'^oaiharvester/collection/delete/(?P<pk>\w+)$',
                           CollectionDeleteView.as_view(
                           ), name='collection_delete'),




                       url(r'^harvest/repositories/$',
                           HarvesterCommunityListView.as_view(
                           ), name='repo_list'),
                       url(r'^harvest/register/(?P<pk>\w+)$',
                           HarvesterRegistrationView.as_view(
                           ), name='register_comm'),
                       # url(r'^harvest/community/(?P<pk>\w+)$', HarvesterCommunityView.as_view(), name='community'),
                       # url(r'^harvest/collection/(?P<pk>\w+)$', HarvesterCollectionView.as_view(), name='collection'),
                       url(r'^harvest/collection/(?P<pk>\w+)$',
                           HarvestRecordsView.as_view(), name='harvest'),

                       url(r'^admin/', include(admin.site.urls)),
                       )
