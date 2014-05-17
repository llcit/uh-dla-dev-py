from django.shortcuts import render
from django.views.generic.base import TemplateView

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

class HarvesterAddRepoView(TemplateView):
    template_name = 'harvester_collector.html'

    def get_context_data(self, **kwargs):
        context = super(HarvesterAddRepoView, self).get_context_data(**kwargs)
        URL = 'http://scholarspace.manoa.hawaii.edu/dspace-oai/request'
        SET_ID = 'col_10125_7735'
        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(URL, registry)
        
        collections = client.listSets()
        collection_list = []
        for i in collections:
            collection = dict()
            collection['setSpec'] = i[0]
            collection['setName'] = i[1]
            collection['setType'] = i[0][:3]
            collection_list.append(collection)

        context['collections'] = collection_list
        return context


class HarvesterView(TemplateView):
    template_name = 'harvester.html'

    def get_context_data(self, **kwargs):
        context = super(HarvesterView, self).get_context_data(**kwargs)
        URL = 'http://scholarspace.manoa.hawaii.edu/dspace-oai/request'
        SET_ID = 'col_10125_7735'
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
            header['setSpec'] =  i[0].setSpec()
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
#http://scholarspace.manoa.hawaii.edu/dspace-oai/request?verb=ListRecords&metadataPrefix=oai_dc&set=col_10125_7735

# Sample request for a set listRecords
# http://scholarspace.manoa.hawaii.edu/dspace-oai/request?verb=ListIdentifiers&metadataPrefix=oai_dc&set=col_10125_7735