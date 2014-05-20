from django.shortcuts import render
from django.views.generic.base import TemplateView

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

from .models import Set


class HarvesterAddRepoView(TemplateView):
    """
    Select and add repository to the site. A repository should be seen as 
    a collection of records. A repo can be a full digital library or a 
    community with the library.
    """
    template_name = 'harvester_collector.html'

    def get_context_data(self, **kwargs):
        context = super(HarvesterAddRepoView, self).get_context_data(**kwargs)
        URL = 'http://scholarspace.manoa.hawaii.edu/dspace-oai/request'
        REPO_ID = 'col_10125_7735'
        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(URL, registry)

        records = client.listRecords(
            metadataPrefix='oai_dc', set=REPO_ID)
        repo_collection_identifiers = []
        for i in records:          
            for j in i[0].setSpec():
                if j[:3] == 'col' and j not in repo_collection_identifiers:
                    repo_collection_identifiers.append(j)

        repo_collections = dict()
        sets = client.listSets()
        for i in sets:
            if i[0] in repo_collection_identifiers:
                repo_collections[i[0]] = i[1]
                collection = Set()
                collection.identifier = i[0]
                collection.name = i[1]
                collection.repository = REPO_ID
                try:
                    collection.save()
                except:
                    collection.update()

        context['collections'] = repo_collections
        return context


class HarvesterView(TemplateView):

    """Harvest records from a given set"""
    template_name = 'harvester.html'

    def get_context_data(self, **kwargs):
        context = super(HarvesterView, self).get_context_data(**kwargs)
        
        URL = 'http://scholarspace.manoa.hawaii.edu/dspace-oai/request'
        SET_ID = kwargs.pop('set') # 'com_10125_4250'
        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(URL, registry)

        records = client.listRecords(
            metadataPrefix='oai_dc', set=SET_ID)

        record_list = []
        for i in records:
            header = dict()
            header['identifier'] = i[0].identifier()
            header['datestamp'] = i[0].datestamp()
            header['setSpec'] = i[0].setSpec()
            header['deleted'] = i[0].isDeleted()

            metadata = dict()
            for key in i[1].getMap():
                metadata[key] = i[1].getField(key)

            record = []
            record.append(header)
            record.append(metadata)
            record_list.append(record)

        context['records'] = record_list
        return context

# Sample request for a single collection
# http://scholarspace.manoa.hawaii.edu/dspace-oai/request?verb=ListRecords&metadataPrefix=oai_dc&set=col_10125_7735

# Sample request for a set listRecords
# http://scholarspace.manoa.hawaii.edu/dspace-oai/request?verb=ListIdentifiers&metadataPrefix=oai_dc&set=col_10125_7735
