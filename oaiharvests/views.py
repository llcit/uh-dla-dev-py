from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django import forms

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib import messages
import json

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

from .models import Repository, Community, Collection, MetadataElement, Record
from .forms import CreateRepositoryForm, CreateCommunityForm, CreateCollectionForm
from .utils import OAIUtils

class RepositoryListView(ListView):
    model = Repository
    template_name = 'repository_list.html'


class RepositoryView(DetailView):
    model = Repository
    template_name = 'repository_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RepositoryView, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['communities'] = obj.list_communities()
        return context


class RepositoryCreateView(CreateView):
    model = Repository
    template_name = 'repository_form.html'
    form_class = CreateRepositoryForm

    def get_context_data(self, **kwargs):
        context = super(RepositoryCreateView, self).get_context_data(**kwargs)
        context['view_type'] = 'add'
        return context


class RepositoryUpdateView(UpdateView):
    model = Repository
    template_name = 'repository_form.html'

    def get_context_data(self, **kwargs):
        context = super(RepositoryUpdateView, self).get_context_data(**kwargs)
        context['view_type'] = 'update'
        return context


class RepositoryDeleteView(DeleteView):
    model = Repository
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('repository_list')



class CommunityView(DetailView):
    model = Community
    template_name = 'community_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CommunityView, self).get_context_data(**kwargs)
        context['collections'] = self.get_object().list_collections()
        return context

class CommunityCreateView(DetailView):
    model = Repository
    template_name = 'community_add_form.html'
    oai = OAIUtils()


    def post(self, request, **kwargs):
        print 'post->'
        form = CreateCommunityForm(request.POST, repo=self.get_object(), community_list=self.oai.communities)

        if form.is_valid():
            choices = form.fields['identifier'].widget.choices
            for i in choices:
                if i[0] == form.instance.identifier:
                    form.instance.name = i[1]
                    break

            form.save()
            return HttpResponseRedirect(reverse('repository', args=[str(self.get_object().id)]))

        return render_to_response('community_add_form.html', {'form': form})
        

    def get_context_data(self, **kwargs):
        context = super(CommunityCreateView, self).get_context_data(**kwargs)
        self.oai.list_oai_community_sets(self.get_object())
        
        form = CreateCommunityForm(repo=self.get_object(), community_list=self.oai.communities)
        context['form'] = form
        return context

class CommunityUpdateView(UpdateView):
    model = Community
    template_name = 'collection_form.html'

    def get_context_data(self, **kwargs):
        context = super(CommunityUpdateView, self).get_context_data(**kwargs)        
        context['view_type'] = 'update community collection info'
        return context

class CommunityDeleteView(DeleteView):
    model = Community
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('repository_list')

    def get_context_data(self, **kwargs):
        context = super(CommunityDeleteView, self).get_context_data(**kwargs)        
        context['view_type'] = 'delete community collection'
        return context


class CollectionView(DetailView):
    model = Collection
    template_name = 'collection_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionView, self).get_context_data(**kwargs)
        context['num_records'] = self.get_object().count_records()
        return context


class CollectionCreateView(DetailView):
    model = Community
    template_name = 'collection_form.html'
    oai = OAIUtils()
    
    def post(self, request, **kwargs):
        form = CreateCollectionForm(request.POST, community=self.get_object(), collections_list=self.oai.collections)

        if form.is_valid():            
            choices = form.fields['identifier'].widget.choices
            for i in choices:
                if i[0] == form.instance.identifier:
                    form.instance.name = i[1]
                    break
            form.save()
            return HttpResponseRedirect(reverse('community', args=[str(self.get_object().identifier)]))

        return render_to_response('collection_add_form.html', {'form': form})
        

    def get_context_data(self, **kwargs):
        context = super(CollectionCreateView, self).get_context_data(**kwargs)        
        self.oai.list_oai_collections(self.get_object())
        form = CreateCollectionForm(community=self.get_object(), collections_list=self.oai.collections)
        context['form'] = form
        context['view_type'] = 'add new collection'
        return context

class CollectionUpdateView(UpdateView):
    model = Collection
    template_name = 'collection_form.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionUpdateView, self).get_context_data(**kwargs)        
        context['view_type'] = 'update collection info'
        return context

class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('repository_list')

    def get_context_data(self, **kwargs):
        context = super(CollectionDeleteView, self).get_context_data(**kwargs)        
        context['view_type'] = 'delete collection info'
        return context


class CollectionHarvestView(DetailView):
    model = Collection
    template_name = 'collection_detail.html'
    
    
    def get_context_data(self, **kwargs):
        context = super(
            CollectionHarvestView, self).get_context_data(**kwargs)
        oai = OAIUtils()
        collection = self.get_object()
        repository = collection.community.repository
        records = oai.harvest_oai_collection_records(collection)

        for i in records:
            """ Read Header """
            try:
                record = Record.objects.get(identifier=i[0].identifier())
                print 'deleting-> ', record
                record.remove_data()
            except:
                record = Record()

                record.identifier = i[0].identifier()
                record.hdr_datestamp = i[0].datestamp()
                record.hdr_setSpec = collection
            
            record.save()

            """ Read Metadata """

            dataelements = i[1].getMap()
            for key in dataelements:
                element = MetadataElement()
                element.record = record
                element.element_type = key
                data = dataelements[key]
                datastring = ''
                for i in data:
                    datastring += i
                # print datastring
                element.element_data = datastring
                element.save()

        context['records'] = self.get_object().record_set.all()
        context['num_records'] = self.get_object().count_records()
        return context







# Sample request for a single collection
# http://scholarspace.manoa.hawaii.edu/dspace-oai/request?verb=ListRecords&metadataPrefix=oai_dc&set=col_10125_7735

# Sample request for a set listRecords
# http://scholarspace.manoa.hawaii.edu/dspace-oai/request?verb=ListIdentifiers&metadataPrefix=oai_dc&set=col_10125_7735
