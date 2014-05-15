from django.shortcuts import render
from django.views.generic.base import TemplateView

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

class HarvesterView(TemplateView):
	template_name = 'harvester.html'

    def get_context_data(self, **kwargs):
        context = super(HarvesterView, self).get_context_data(**kwargs)
        URL = 'http://scholarspace.manoa.hawaii.edu/dspace-oai/request'
        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(URL, registry)
        records = client.listRecords(
            metadataPrefix='oai_dc', set='col_10125_7735').getMap()
        myrecords = []
        # for i in records:
        #     mydict = dict()
        #     metadata = i[1].getMap()
        # #     # print metadata
        #     for key in metadata:
        #         mydict[key] = i[1].getField(key)
        #         print '%s->%s' % (key, i[1].getField(key))
        #     myrecords.append(mydict)


        context['records'] = records

        return context