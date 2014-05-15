from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dlasite.views import HomeView, CollectionListView, CollectionView, RecordView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^collections/$', CollectionListView.as_view(), name='collection_list'),
    url(r'^collection/$', CollectionView.as_view(), name='collection'),
    url(r'^record/$', RecordView.as_view(), name='record'),
    url(r'^admin/', include(admin.site.urls)),
)
