from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dlasite.views import HomeView, CommunityView, CollectionListView, CollectionView, ItemView, LanguageView, AuthorView
from oaiharvests.views import (
    OaiRepositoryListView, 
    OaiRepositoryCreateView, 
    OaiRepositoryUpdateView, 
    OaiRepositoryDeleteView, 
    OaiRepositoryView,
    OaiCommunityView,
    OaiCommunityCreateView,
    OaiCommunityUpdateView,
    OaiCommunityDeleteView,
    OaiCollectionView,
    OaiCollectionCreateView,
    OaiCollectionUpdateView,
    OaiCollectionDeleteView,
    OaiCollectionHarvestView
)

urlpatterns = patterns('',

                       # ---------- SITE VIEWS ------------- #

                       url(r'^$', HomeView.as_view(), name='home'),
                       url(r'^community/(?P<pk>\w+)$',
                           CommunityView.as_view(), name='community'),                       
                       url(r'^collections/$', CollectionListView.as_view(),
                           name='collection_list'),
                       url(r'^collection/(?P<pk>\w+)$',
                           CollectionView.as_view(), name='collection'),
                       url(r'^item/(?P<pk>\w+)$',
                           ItemView.as_view(), name='item'),
                       url(r'^language/(?P<query>\w+)$',
                           LanguageView.as_view(), name='collection'),
                       url(r'^author/(?P<query>\w+)$',
                           AuthorView.as_view(), name='collection'),



                       # ---------- OAI HARVESTER VIEWS ------------- #
                       # Institutional Repositories #
                       url(r'^oaiharvester/$', OaiRepositoryListView.as_view(),
                           name='oai_repository_list'),
                       url(r'^oaiharvester/repository/add/$',
                           OaiRepositoryCreateView.as_view(
                           ), name='oai_repository_add'),
                       url(r'^oaiharvester/repository/edit/(?P<pk>\w+)$',
                           OaiRepositoryUpdateView.as_view(
                           ), name='oai_repository_edit'),
                       url(r'^oaiharvester/repository/delete/(?P<pk>\w+)$',
                           OaiRepositoryDeleteView.as_view(
                           ), name='oai_repository_delete'),
                       url(r'^oaiharvester/repository/(?P<pk>\w+)$',
                           OaiRepositoryView.as_view(), name='oai_repository'),

                       # Community Collections #
                       url(r'^oaiharvester/community/(?P<pk>\w+)$',
                           OaiCommunityView.as_view(), name='oai_community'),
                       url(r'^oaiharvester/community/add/(?P<pk>\w+)$',
                           OaiCommunityCreateView.as_view(
                           ), name='oai_community_add'),
                       url(r'^oaiharvester/community/edit/(?P<pk>\w+)$',
                           OaiCommunityUpdateView.as_view(
                           ), name='oai_community_edit'),
                       url(r'^oaiharvester/community/delete/(?P<pk>\w+)$',
                           OaiCommunityDeleteView.as_view(
                           ), name='oai_community_delete'),

                       # Collections #
                       url(r'^oaiharvester/collection/(?P<pk>\w+)$',
                           OaiCollectionView.as_view(), name='oai_collection'),
                       url(r'^oaiharvester/collection/add/(?P<pk>\w+)$',
                           OaiCollectionCreateView.as_view(
                           ), name='oai_collection_add'),
                       url(r'^oaiharvester/collection/edit/(?P<pk>\w+)$',
                           OaiCollectionUpdateView.as_view(
                           ), name='oai_collection_edit'),
                       url(r'^oaiharvester/collection/delete/(?P<pk>\w+)$',
                           OaiCollectionDeleteView.as_view(
                           ), name='oai_collection_delete'),
                       url(r'^oaiharvester/collection/harvest/(?P<pk>\w+)$',
                           OaiCollectionHarvestView.as_view(
                           ), name='oai_harvest_collection'),


                       url(r'^admin/', include(admin.site.urls)),
                       )
