from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from oaiharvests.models import Community, Collection, Record, MetadataElement

import json, collections

#For debugging purposes
import pdb #pdb.set_trace()

class HomeView(TemplateView):
		template_name = 'home.html'

		def get_context_data(self, **kwargs):
			#Element Queries
			records = Record.objects.all()
			#arrays to hold values
			contributor_array = []
			contributor_count = []
			language_array = []
			language_count = []
			record_array = []
			#Dictionary to hold values and times
			language_dict = {}
			contributor_dict = {}

			#Get languages element
			records=MetadataElement.objects.filter(element_type='language')
			for record in records:
				languages=json.loads(record.element_data)
				for language in languages:
					if language not in language_array:
						language_array.append(language)
						language_count.append(len(MetadataElement.objects.filter(element_type='language').filter(element_data__contains=language)))
			records=MetadataElement.objects.filter(element_type='contributor')
			for record in records:
				contributors=json.loads(record.element_data)
				for contributor in contributors:
					if contributor not in contributor_array:
						contributor_array.append(contributor)
						contributor_count.append(len(MetadataElement.objects.filter(element_type='contributor').filter(element_data__contains=contributor)))
				#Get the coordinates for objects with dc_coverage
				if record.record.get_coordinates()['North'] != 'none':
						if record.record.get_coordinates()['North']!="":
							record_array.append(record.record.get_coordinates())
			
			#Create dictionary with language values
			count=0
			for element in language_array:
				#pdb.set_trace()
			 	language_dict[element]=language_count[count]
			 	count=count+1

			# Create a dictionary with the contributor values
			count=0
			for element in contributor_array:
				contributor_dict[element]=contributor_count[count]
				count=count+1
			
			#Encode output to json format
			jsonStr=json.dumps(record_array)
			#Context for the template
			context = super(HomeView, self).get_context_data(**kwargs)
			context['communities'] = Community.objects.all()
			context['collections'] = Collection.objects.all()
			context['jsonStr']=unicode(jsonStr)
			context['languages']=language_dict
			#context['languages_count']=language_count
			#context['contributors']=contributor_array
			context['contributors']=contributor_dict
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

class LanguageView(TemplateView):
	template_name = 'collection_view.html'

	def get_context_data(self, **kwargs):
			#arrays to hold values
			items = []
			record_array = []
			Query = self.kwargs['query']
			for element in MetadataElement.objects.filter(element_type='language').filter(element_data__contains=Query):
				items.append(element.record)
				#Get the coordinates for objects with dc_coverage
				if element.record.get_coordinates()['North'] != 'none':
					if element.record.get_coordinates()['North']!="":
						record_array.append(element.record.get_coordinates())
			#Encode output to json format
			jsonStr=json.dumps(record_array)
			context = super(LanguageView, self).get_context_data(**kwargs)
			#Query the db with the language to search and added to the context
			context['items'] =items
			context['object']=Query + ' language'
			context['jsonStr']=unicode(jsonStr) 
			return context

class AuthorView(TemplateView):
	template_name = 'collection_view.html'

	def get_context_data(self, **kwargs):
			#arrays to hold values
			items = []
			record_array = []
			Query = self.kwargs['query']
			for element in MetadataElement.objects.filter(element_type='contributor').filter(element_data__contains=Query):
				items.append(element.record)
				#Get the coordinates for objects with dc_coverage
				if element.record.get_coordinates()['North'] != 'none':
					if element.record.get_coordinates()['North']!="":
						record_array.append(element.record.get_coordinates())
			#Encode output to json format
			jsonStr=json.dumps(record_array)
			context = super(AuthorView, self).get_context_data(**kwargs)
			#Query the db with the language to search and added to the context
			context['items'] =items
			context['object']=Query + ' Depositor'
			context['jsonStr']=unicode(jsonStr) 
			return context


