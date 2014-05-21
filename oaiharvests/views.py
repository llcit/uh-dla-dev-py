from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

from .models import Repository, Community, Collection, MetadataElement, Record

class HarvesterCommunityListView(ListView):
    model = Community
    template_name = 'harvester_list_repos.html'

    def get_context_data(self, **kwargs):
        context = super(HarvesterCommunityListView, self).get_context_data(**kwargs)
        # context['communities'] = selt.get_object().set_community.all()
        return context


class HarvesterCommunityView(DetailView):
    """
    Browse an institutional repository community for selective harvesting.  A repo is a
    community collection within the institutional repo.

    Expected model instance is a pk representing a community collection identifier
    """
    model = Community
    template_name = 'harvester_collector.html'
    name_index = dict()

    def get_context_data(self, **kwargs):
        context = super(
            HarvesterCommunityView, self).get_context_data(**kwargs)
        repo = self.get_object()        

        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(repo.repository.base_url, registry)

        """ retrieve the header data for each record in the current community repo """
        try:
            records = client.listIdentifiers(
                metadataPrefix='oai_dc', set=repo.identifier)
        except:
            messages.add_message(
                self.request, messages.ERROR, 'Repository or Collection with id ' + repo_id + ' was not found.')
            return context

        """ Filter collections from records to build list of collections in the SET """
        registered_id_list = repo.collections().values_list(
            'identifier', flat=True)
        remote_collection_identifiers = []
        for i in records:
            for j in i.setSpec():
                if j[:3] == 'col':
                    if j not in registered_id_list and j not in remote_collection_identifiers:
                        remote_collection_identifiers.append(j)

        """ Build dictionary (id, human readable name) of collections for possible harvesting """
        sets = client.listSets()
        collections = dict()
        for i in sets:
            if i[0] in remote_collection_identifiers:
                collections[i[0]] = i[1]

        context['repository'] = repo
        context['registered_collections'] = repo.collections()
        context['unregistered_collections'] = collections
        return context

    def post(self, request, *args, **kwargs):
        try:
            repo = Community.objects.get(pk=request.POST['repoid'])
        except:
            pass
        selected_set = request.POST['set_id']
        selected_set_name = ''

        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(repo.repository.base_url, registry)

        sets = client.listSets()
        
        for i in sets:
            if i[0] == selected_set:
                selected_set_name = i[1]
                break
        try:
            collection = Collection.objects.get(pk=selected_set)
        except:
            collection = Collection()
            collection.identifier = selected_set
            collection.name = selected_set_name
            collection.community = repo

        collection.save()

        """ Harvest each record """
        records = client.listRecords(
            metadataPrefix='oai_dc', set=selected_set)
        for i in records:
            record = Record()
            """ Read Header """
            record.identifier = i[0].identifier()
            record.hdr_datestamp = i[0].datestamp()
            record.save()
            record.hdr_setSpec.add(collection)

            """ Read Metadata """
            for key in i[1].getMap():
                element = MetadataElement()
                element.record = record
                element.element_type = key
                element.element_data = i[1].getField(key) or ' '
                element.save()
        
        return HttpResponseRedirect(reverse('home'))




class HarvesterCollectionView(TemplateView):

    """Harvest records from a given set"""
    template_name = 'harvester_records.html'

    def post(self, request, *args, **kwargs):
        try:
            repo = Community.objects.get(pk=request.POST['repoid'])
        except:
            pass

        selected_set = request.POST['set_id']
    

    
        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(repo.repository.base_url, registry)

        # collection_obj = client.getRecord(identifier=selected_set, metadataPrefix='oai_dc' )
        try:
            collection = Collection.objects.get(pk=selected_set)
        except:
            collection = Collection()
            collection.identifier = selected_set
            # collection.name = request.POST['set_name']
            collection.community = repo

        try:
            pass
            # print collection
            # collection.save()
        except:
            pass

        records = client.listRecords(
            metadataPrefix='oai_dc', set=selected_set)



        for i in records:
            record = Record()
            """ Read Header """
            record.identifier = i[0].identifier()
            record.hdr_datestamp = i[0].datestamp()
            record.save()
            # record.hdr_setSpec = collection

            """ Read Metadata """
            for key in i[1].getMap():
                element = MetadataElement()
                element.element_type = key
                element.element_data = i[1].getField(key) or ' '
                element.save()
                
                record.metadata.add(element)
        
        return HttpResponseRedirect(reverse('home'))


# Sample request for a single collection
# http://scholarspace.manoa.hawaii.edu/dspace-oai/request?verb=ListRecords&metadataPrefix=oai_dc&set=col_10125_7735

# Sample request for a set listRecords
# http://scholarspace.manoa.hawaii.edu/dspace-oai/request?verb=ListIdentifiers&metadataPrefix=oai_dc&set=col_10125_7735
