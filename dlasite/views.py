from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from oaiharvests.models import Community, Collection, Record

import json

#For debugging purposes
import pdb

class HomeView(TemplateView):
		template_name = 'home.html'

		def get_context_data(self, **kwargs):
			#Element Queries
			records = Record.objects.all()
			creator_array = []
			record_array = []
			language_array = []
			#pdb.set_trace()
			for record in records:
				#Get languages in an array
				language_array.append(record.get_metadata_item('language')[0].element_data)
				#pdb.set_trace()
				creator_array.append(record.get_metadata_item('contributor')[0].element_data)
				#Get the coordinates for objects with dc_coverage
				if record.get_coordinates()['North'] != 'none':
					record_array.append(record.get_coordinates())
			#Create a language array without duplicates
			language_array=list(set(language_array))
			#Encode output to json format
			jsonStr=json.dumps(record_array)
			context = super(HomeView, self).get_context_data(**kwargs)
			context['communities'] = Community.objects.all()
			context['collections'] = Collection.objects.all()
			context['jsonStr']=unicode(jsonStr)
			context['language_array']=language_array
			context['creator_array']=creator_array
			context['default'] = get_object_or_404(Community, identifier='com_10125_4250') #Community.objects.filter(identifier='com_10125_4250')
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
