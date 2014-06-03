from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from oaiharvests.models import Community, Collection, Record

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['communities'] = Community.objects.all()
        return context

class CommunityView(DetailView):
	model = Community
	template_name = 'community_view.html'

	def get_context_data(self, **kwargs):
	    context = super(CommunityView, self).get_context_data(**kwargs)
	    context['collections'] = self.get_object().list_collections()
	    return context

class CollectionListView(ListView):
	model = Collection
	template_name = 'collection_list.html'

	def get_context_data(self, **kwargs):
	    context = super(CollectionListView, self).get_context_data(**kwargs)
	    return context

class CollectionView(DetailView):
	model = Collection
	template_name = 'collection_view.html'

	def get_context_data(self, **kwargs):
	    context = super(CollectionView, self).get_context_data(**kwargs)
	    context['items'] = self.get_object().list_records()
	    return context


class ItemView(DetailView):
	model = Record
	template_name = 'item_view.html'

	def get_context_data(self, **kwargs):
	    context = super(ItemView, self).get_context_data(**kwargs)
	    context['item_data'] = self.get_object().metadata_items()
	    return context
