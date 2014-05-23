from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django import forms

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib import messages
import json
from itertools import tee

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

from .models import Repository, Community, Collection, MetadataElement, Record
from .forms import CreateRepositoryForm

class RepositoryListView(ListView):
    model = Repository
    template_name = 'repository_list.html'


class RepositoryView(DetailView):
    model = Repository
    template_name = 'repository_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RepositoryView, self).get_context_data(**kwargs)
        context['collections'] = Collection.objects.filter(
            community__repository=self.get_object()).order_by('community')
        return context


class RepositoryCreateView(CreateView):
    model = Repository
    template_name = 'repository_form.html'
    form_class = CreateRepositoryForm

    def verify_remote_repository(self, **kwargs):
        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        try:
            client = Client(kwargs.pop('base_url'), registry)
            server = client.identify()
            return server
        except:
            return None

    def form_valid(self, form):
        # server = self.verify_remote_repository(base_url=form.cleaned_data['base_url'])
        # if server:
        #     return super(RepositoryCreateView, self).form_valid(form)
        return super(RepositoryCreateView, self).form_valid(form)



    def get_context_data(self, **kwargs):
        context = super(RepositoryCreateView, self).get_context_data(**kwargs)
        context['view_type'] = 'add'
        return context

class RepositoryUpdateView(UpdateView):
    model = Repository
    template_name = 'repository_form.html'

    def get_context_data(self, **kwargs):
        context = super(RepositoryUpdateView, self).get_context_data(**kwargs)
        context['view_type'] = 'edit'
        return context

class RepositoryDeleteView(DeleteView):
    model = Repository
    success_url = reverse_lazy('repository_list')
    template_name = 'repository_confirm_delete.html'


class CommunityView(DetailView):
    model = Community
    template_name = 'community_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CommunityView, self).get_context_data(**kwargs)
        context['collections'] = self.get_object().list_collections()
        return context


class CommunityCreateView(CreateView):
    model = Community


class CommunityUpdateView(UpdateView):
    model = Community


class CommunityDeleteView(DeleteView):
    model = Community


class CollectionView(DetailView):
    model = Collection
    template_name = 'collection_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionView, self).get_context_data(**kwargs)
        context['num_records'] = self.get_object().count_records()
        return context


class CollectionCreateView(CreateView):
    model = Collection


class CollectionUpdateView(UpdateView):
    model = Collection


class CollectionDeleteView(DeleteView):
    model = Collection


class HarvesterCommunityListView(ListView):
    model = Community
    template_name = 'harvester_list_repos.html'

    def get_context_data(self, **kwargs):
        context = super(
            HarvesterCommunityListView, self).get_context_data(**kwargs)
        # context['communities'] = selt.get_object().set_community.all()
        return context


class HarvesterCommunityView(DetailView):
    model = Community
    template_name = 'harvester_community_repo.html'

    def get_context_data(self, **kwargs):
        context = super(
            HarvesterCommunityView, self).get_context_data(**kwargs)
        context['collections'] = self.get_object().collection_set.all()
        return context


class HarvesterRegistrationView(DetailView):

    """
    Creates or updates Collection objects from an institutional repository community for future 
    harvesting. The source of the collections is a community set within the institutional repo.

    Expected model instance is a pk representing a community collection identifier.

    Expected outcome are new Collection instances stored in local db.
    """
    model = Community
    template_name = 'harvester_collector.html'

    def get_context_data(self, **kwargs):
        self.context = super(
            HarvesterRegistrationView, self).get_context_data(**kwargs)
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

        """ Filter records to build list of collections in the SET """
        remote_collections = dict()
        for i in records:
            for j in i.setSpec():
                if j[:3] == 'col':
                    remote_collections[j] = ''

        """ Build collection object (id and human readable name) """
        sets = client.listSets()
        for i in sets:
            if i[0] in remote_collections:
                """ Retrieve or create a collection obj """
                try:
                    collection = Collection.objects.get(pk=i[0])
                except:
                    collection = Collection()
                    collection.identifier = i[0]
                    collection.name = i[1]
                    collection.community = repo

                collection.save()

        self.context['registered_collections'] = repo.collections()
        return self.context


class HarvestRecordsView(DetailView):

    """ Harvest records in a single collection """
    model = Collection
    template_name = 'harvester_collection.html'

    def get_context_data(self, **kwargs):
        context = super(
            HarvestRecordsView, self).get_context_data(**kwargs)
        collection = self.get_object()
        repo = collection.community.repository

        """ Create OAI client from repo object """
        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(repo.base_url, registry)

        """ Harvest each record in collection """
        records = client.listRecords(
            metadataPrefix='oai_dc', set=collection.identifier)

        for i in records:
            """ Read Header """
            try:
                record = Record.object.get(collection=collection)
                record.remove_data()
            except:
                record = Record()

            # record.identifier = i[0].identifier()
            # record.hdr_datestamp = i[0].datestamp()
            # record.hdr_setSpec = collection
            # record.save()

            # """ Read Metadata """

            # dataelements = i[1].getMap()
            # for key in dataelements:
            #     element = MetadataElement()
            #     element.record = record
            #     element.element_type = key
            #     data = dataelements[key]
            #     datastring = ''
            #     for i in data:
            #         datastring += i
            #     print datastring
            #     element.element_data = datastring
            #     element.save()

        context['records'] = self.get_object().record_set.all()
        return context


class HarvesterCollectionView(DetailView):

    """Show records from a given set"""
    model = Collection
    template_name = 'harvester_collection.html'

    def get_context_data(self, **kwargs):
        context = super(
            HarvesterCollectionView, self).get_context_data(**kwargs)
        context['records'] = self.get_object().record_set.all()
        return context



    # def post(self, request, *args, **kwargs):
    #     """ Create OAI client from repo object """
    #     repo = self.get_object().community.repository

    #     registry = MetadataRegistry()
    #     registry.registerReader('oai_dc', oai_dc_reader)
    #     client = Client(repo.repository.base_url, registry)

    #     """ Filter POST data to build list of selected collections to harvest """
    #     harvest_list = []
    #     for i in request.POST:
    #         if i[:3] == 'col':
    # harvest_list.append(i) # -->request.POST[harvest_list[0]]

    #     """ Iterate over list of selected collections adding to local storage each iteration """
    #     for i in harvest_list:
    #         selected_set_id = i
    #         selected_set_name = request.POST[i]
    #         print selected_set_id, selected_set_name

    #         """ Retrieve or create a collection obj """
    #         try:
    #             collection = Collection.objects.get(pk=selected_set_id)
    #         except:
    #             collection = Collection()
    #             collection.identifier = selected_set_id
    #             collection.name = selected_set_name
    #             collection.community = repo

    #         collection.save()

    #         """ Harvest each record in remote collection """
    #         records = client.listRecords(
    #             metadataPrefix='oai_dc', set=selected_set_id)

    #         for i in records:
    #             record = Record()
    #             """ Read Header """
    #             record.identifier = i[0].identifier()
    #             record.hdr_datestamp = i[0].datestamp()
    #             record.hdr_setSpec = collection
    #             record.save()

    #             record.remove_data()

    #             """ Read Metadata """
    #             for key in i[1].getMap():
    #                 element = MetadataElement()
    #                 element.record = record
    #                 element.element_type = key
    #                 data = i[1].getField(key)
    # datastring = ''
    # for j in data:
    # print j
    # datastring += j + ', '
    #                 element.element_data = data
    #                 element.save()

    # return HttpResponseRedirect(reverse('home'))
    #     response_data = []
    #     response_data.append('added collection for harvesting')
    # return HttpResponse(json.dumps(response_data), content_type="application/json")
    #     return render(request, self.template_name, self.context)




# Sample request for a single collection
# http://scholarspace.manoa.hawaii.edu/dspace-oai/request?verb=ListRecords&metadataPrefix=oai_dc&set=col_10125_7735

# Sample request for a set listRecords
# http://scholarspace.manoa.hawaii.edu/dspace-oai/request?verb=ListIdentifiers&metadataPrefix=oai_dc&set=col_10125_7735
