from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.template import RequestContext
from django.http import HttpResponse
#For making complex queries
from django.db.models import Q, Count
from django.db.models import Count

from oaiharvests.models import Community, Collection, Record, MetadataElement

import json, collections, operator #operator is used for sorting

class HomeView(TemplateView):
        template_name = 'home.html'

        def get_context_data(self, **kwargs):
            #arrays to hold values
            contributor_array = []
            contributor_count = []
            language_array = []
            language_count = []
            record_array = []
            contributor_url = []
            sorted_language = []
            sorted_contributor = []
            sorted_collections = []
            
            #Dictionary to hold values and times
            language_dict = {}
            contributor_dict = {}
            collection_dict = {}
            
            #Query and variables for the needed MetadataElments
            metadata = MetadataElement.objects.all()
            
            languages_meta = metadata.filter(element_type='language')
            contributor_meta = metadata.filter(element_type='contributor')
            coverage_meta = metadata.filter(element_type='coverage')
            
            #Create dicts with frequency counts
            language_dict = {}
            for metaelement in languages_meta:
                language_list=json.loads(metaelement.element_data)              
                for language in language_list:
                    if language in language_dict:
                        language_dict[language] = language_dict[language]+1
                    else:
                        language_dict[language] = 1
            
            contributor_dict = {}
            for metaelement in contributor_meta:
                contributors_list=json.loads(metaelement.element_data)
                for contributor in contributors_list:
                    if contributor in contributor_dict:
                        contributor_dict[contributor] = contributor_dict[contributor]+1
                    else:
                        contributor_dict[contributor] = 1
            
            for metaelement in coverage_meta:
                position = json.loads(metaelement.element_data)
                
                if position:                 
                    record_array.append(metaelement.record.get_coordinates(position))

            #Sort dictionaries to show the ones with more elements first
            sorted_language=sorted(language_dict.iteritems(), key=operator.itemgetter(1),reverse=True)
            sorted_contributor=sorted(contributor_dict.iteritems(), key=operator.itemgetter(1),reverse=True)
            sorted_collections=sorted(collection_dict.iteritems(), key=operator.itemgetter(1),reverse=True)

            ######################## Preparing context to render in template ########################################################
            #Encode output to json format
            jsonStr=json.dumps(record_array)
            context = super(HomeView, self).get_context_data(**kwargs)
            context['communities'] = Community.objects.all()
            context['collections'] = Collection.objects.all().order_by('name')
            context['jsonStr'] = unicode(jsonStr)
            context['languages'] = sorted_language
            context['contributors'] = sorted_contributor
            context['contributor_url'] = contributor_url
            context['default'] = get_object_or_404(Community, identifier='com_10125_4250')

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
                position=json.loads(self.get_object().list_records()[0].get_metadata_item('coverage')[0].element_data)
                if position:
                    if position != 'none':
                        record_array.append(record.get_coordinates(position))
                # #Get the coordinates for objects with dc_coverage
                # if record.get_coordinates()['North'] != 'none':
                #   if record.get_coordinates()['North']!="":
                #       record_array.append(record.get_coordinates())
            #Encode output to json format
            jsonStr=json.dumps(record_array)
            #Context for the template
            context = super(CollectionView, self).get_context_data(**kwargs)
            context['items'] = self.get_object().list_records()
            context['size'] = len(self.get_object().list_records())
            context['jsonStr']=unicode(jsonStr)
            return context


class ItemView(DetailView):
    model = Record
    template_name = 'item_view.html'

    def get_context_data(self, **kwargs):
            context = super(ItemView, self).get_context_data(**kwargs)
            context['item_dict'] = self.get_object().to_dict()
            return context

class LanguageView(TemplateView):
    template_name = 'collection_view.html'

    def get_context_data(self, **kwargs):
            #arrays to hold values
            items = []
            record_array = []
            Query = self.kwargs['query']
            for element in MetadataElement.objects.filter(element_type='language').filter(element_data__icontains=Query):
                items.append(element.record)
                #Get the coordinates for objects with dc_coverage
                # position=json.loads(element.record.get_metadata_item('coverage')[0].element_data)
                # if position:
                #     if position != 'none':
                #         record_array.append(element.record.get_coordinates(position))
            #Encode output to json format
            jsonStr=json.dumps(record_array)
            context = super(LanguageView, self).get_context_data(**kwargs)
            context['len']=len(items)
            context['items'] =items
            context['object']=Query + ' language'
            context['jsonStr']=unicode(jsonStr) 
            return context

class ContributorView(TemplateView):
    template_name = 'collection_view.html'

    def get_context_data(self, **kwargs):
            #arrays to hold values
            items = []
            record_array = []
            Query = self.kwargs['query']
            if len(Query.split('-'))!=1:
                firstQuery=Query.split('-')[0]
                lastQuery=Query.split('-')[1]
                for element in MetadataElement.objects.filter(element_type='contributor').filter(Q(element_data__icontains=firstQuery) & Q(element_data__icontains=lastQuery)):
                    items.append(element.record)
                    #Get the coordinates for objects with dc_coverage
                    # if element.record.get_coordinates()['North'] != 'none':
                    #     if element.record.get_coordinates()['North']!="":
                    #         record_array.append(element.record.get_coordinates())
            else:
                for element in MetadataElement.objects.filter(element_type='contributor').filter(element_data__icontains=Query):
                    items.append(element.record)
                    #Get the coordinates for objects with dc_coverage
                    position=json.loads(element.record.get_metadata_item('coverage')[0].element_data)
                    if position:
                        if position != 'none':
                            record_array.append(element.record.get_coordinates(position))
            #Encode output to json format
            jsonStr=json.dumps(record_array)
            context = super(ContributorView, self).get_context_data(**kwargs)
            #Query the db with the language to search and added to the context
            context['items'] =items
            context['len']=len(items)
            context['object']=Query
            context['jsonStr']=unicode(jsonStr) 
            return context

class SearchView(ListView):
    template_name = 'search.html'

    def post(self, request, *args, **kwargs):
        #arrays to hold values
        self.items = []

        #Grab POST values from the search query
        self.query=self.request.POST.get('query')
        self.key=self.request.POST.get('key')

        self.queryset=MetadataElement.objects.filter(element_type=self.query).filter(element_data__icontains=self.key)

        for element in MetadataElement.objects.filter(element_type=self.query).filter(element_data__icontains=self.key):
                self.items.append(element.record)

        return super(SearchView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
            context = super(SearchView, self).get_context_data(**kwargs)
            context ['items'] = self.items
            context['len'] = len(self.items)
            context['query'] = self.query
            context['key'] = self.key
            # pdb.set_trace()
            return context


