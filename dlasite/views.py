from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.template import RequestContext
from django.http import HttpResponse
from collections import Counter, namedtuple
#For making complex queries
from django.db.models import Q, Count

import json, operator #operator is used for sorting

from oaiharvests.models import Community, Collection, Record, MetadataElement

""" A namedtuple to construct unique points to plot """
Plot = namedtuple('Plot',['lat', 'lng']) 

def make_map_plot(coordinates_metadata):
    # create a two-item array from metaelement data e.g. [u'7.4278', u'134.5495']
    position = json.loads(coordinates_metadata)
    try: 
        return Plot(position[0], position[1])
    except:
        # No plots to create -- empty metadata
        return None

def make_json_map_plots(plots):
    # Create a dictionary for each plot to encode as json string.
    try:
        plots = [ plot._asdict() for plot in list(plots) ]
        return json.dumps( plots ) # jsonify for google maps js client.
    except:
        return []   

class HomeView(TemplateView):
        template_name = 'home.html'

        def get_context_data(self, **kwargs):
            mapped_records = []
                       
            #Query and variables for the needed MetadataElments
            metadata = MetadataElement.objects.all()   
            
            # Create dictionary with language frequency counts using Counter
            language_frequencies = Counter()
            for metaelement in metadata.filter(element_type='language'):
                language_frequencies.update( json.loads(metaelement.element_data) )           

            # Create dictionary with contributor frequency counts using Counter
            contributor_frequencies = Counter()
            for metaelement in metadata.filter(element_type='contributor'):
                contributor_frequencies.update( json.loads(metaelement.element_data) )
            
            
            mapped_plots = set()    # unique coords in mapped records 
            mapped_languages = set() # unique languages in mapped records         

            # Only retrieve metadata items that have data values set for coverage       
            for metaelement in metadata.filter(element_type='coverage').exclude(element_data=[]):                       
                mapped_plots.add( make_map_plot(metaelement.element_data) )
                record_dict = metaelement.record.as_dict()            
                
                mapped_languages |= set(record_dict['language'])
                mapped_records.append(record_dict)

            
            mapped_plots=make_json_map_plots(mapped_plots) 

            ######################## Preparing context to render in template ########################################################     
            context = super(HomeView, self).get_context_data(**kwargs)
            context['communities'] = Community.objects.all()
            context['collections'] = Collection.objects.all().order_by('name')
            context['languages'] = sorted(language_frequencies.iteritems(), key=operator.itemgetter(1),reverse=True)
            context['contributors'] = sorted(contributor_frequencies.iteritems(), key=operator.itemgetter(1),reverse=True)
            context['default'] = get_object_or_404(Community, identifier='com_10125_4250')

            context['mapped_records'] = sorted(mapped_records, key=operator.itemgetter('collection'))
            context['mapped_plots'] = unicode(mapped_plots)
            context['mapped_languages'] = sorted(mapped_languages)

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
            records = self.get_object().list_records()
            mapped_plots = set()
            mapped_languages = set()
            mapped_records = []

            for record in records:
                record_dict = record.as_dict()
                mapped_data = MetadataElement.objects.filter(record=record).filter(element_type='coverage').exclude(element_data=[])                
                if mapped_data:
                    mapped_plots.add( make_map_plot( mapped_data[0].element_data ) )
                    mapped_languages |= set(record_dict['language'])
                    mapped_records.append(record_dict)

            mapped_plots = make_json_map_plots(mapped_plots)

            # Context for the template
            context = super(CollectionView, self).get_context_data(**kwargs)
            context['items'] = records
            context['size'] = len(records)
            context['mapped_records'] = sorted(mapped_records)
            context['mapped_languages'] = sorted(mapped_languages)
            context['mapped_plots']=unicode(mapped_plots)
            return context


class ItemView(DetailView):
    model = Record
    template_name = 'item_view.html'

    def get_context_data(self, **kwargs):
            context = super(ItemView, self).get_context_data(**kwargs)
            context['item_data'] = self.get_object().as_dict()
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


class RecordSearchMixin(object):

    def get_queryset(self):
        queryset = super(RecordSearchMixin, self).get_queryset()

        key = self.request.GET.get('key')
        filteropt = self.request.GET.get('filteropts')

        if key:
            return queryset.filter(metadataelement__element_type=filteropt).filter(metadataelement__element_data__icontains=key)
        
        return None

class SearchPage(RecordSearchMixin, ListView):
    model = Record
    template_name = 'searchtest.html'

    # def get_context_data(self, **kwargs):
    #         context = super(SearchPage, self).get_context_data(**kwargs)
    #         context ['results'] = self.results
    #         return context


