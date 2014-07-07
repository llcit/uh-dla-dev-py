from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from oaiharvests.models import Community, Collection, Record

import json, collections

#For debugging purposes
import pdb #pdb.set_trace()

class HomeView(TemplateView):
		template_name = 'home.html'

		def get_context_data(self, **kwargs):
			#Element Queries
			records = Record.objects.all()
			#arrays to hold values
			creator_array = []
			record_array = []
			language_array = []
			#Dictionary to hold values and times
			language_dict = {}
			creator_dict = {}

			#Get information form the records metadata
			for record in records:
				#Get languages in an array from json string format
				for language in json.loads(record.get_metadata_item('language')[0].element_data):
						language_array.append(language)
				for creator in json.loads(record.get_metadata_item('contributor')[0].element_data):
					creator_array.append(creator)
				#Get the coordinates for objects with dc_coverage
				if record.get_coordinates()['North'] != 'none':
					if record.get_coordinates()['North']!="":
						record_array.append(record.get_coordinates())
			
			#Create a counter for the languages and creators
			language_counter=collections.Counter(language_array)
			creator_counter=collections.Counter(creator_array)
			#Create a language array without duplicates and save it to dictionary
			language_array=list(set(language_array))
			for element in language_array:
				language_dict[element]=language_counter[element]
			#Create a creator array without duplicates and save it to dictionary
			creator_array=list(set(creator_array))
			for element in creator_array:
				creator_dict[element]=creator_counter[element]
			
			#Encode output to json format
			jsonStr=json.dumps(record_array)
			#Context for the template
			context = super(HomeView, self).get_context_data(**kwargs)
			context['communities'] = Community.objects.all()
			context['collections'] = Collection.objects.all()
			context['jsonStr']=unicode(jsonStr)
			context['languages']=language_dict
			context['creators']=creator_dict
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
			#arrays to hold values
			record_array = []
			for record in self.get_object().list_records():
				#Get the coordinates for objects with dc_coverage
				if record.get_coordinates()['North'] != 'none':
					if record.get_coordinates()['North']!="":
						record_array.append(record.get_coordinates())
			#pdb.set_trace()
			#Encode output to json format
			jsonStr=json.dumps(record_array)
			#Context for the template
			context = super(CollectionView, self).get_context_data(**kwargs)
			context['items'] = self.get_object().list_records()
			context['jsonStr']=unicode(jsonStr)
			return context


class ItemView(DetailView):
	model = Record
	template_name = 'item_view.html'

	def get_context_data(self, **kwargs):
			context = super(ItemView, self).get_context_data(**kwargs)
			context['item_data'] = self.get_object().metadata_items()
			return context
