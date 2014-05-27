# oaiharvests/forms.py
from django.forms import ModelForm, ValidationError
from django import forms
from django.contrib import messages

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

from .models import Repository, Community, Collection


class CreateRepositoryForm(ModelForm):

    def clean(self):
        cleaned_data = super(CreateRepositoryForm, self).clean()
        try:
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            client = Client(cleaned_data.get('base_url'), registry)
            server = client.identify()
            # set the repository name -- will apply to model instance when saved.
            cleaned_data['name'] = server.repositoryName()
        except:
            raise ValidationError('Repository base url is invalid.')

        return cleaned_data

    def save(self):
        repository = super(CreateRepositoryForm, self).save(commit=False)
        repository.name = self.cleaned_data.get('name')
        repository.save()
        return repository

    class Meta:
        model = Repository
        fields = ['base_url']


class CreateCommunityForm(ModelForm):
    # modify identifier field to show list of repository communities

    community_list = []
    def clean(self):
        cleaned_data = super(CreateCommunityForm, self).clean()

        for i in self.community_list:
            if i[0] == cleaned_data['identifier']:
                cleaned_data['name'] = i[1]
                break

        print 'clean->', self.community_list
        return cleaned_data

    def build_oai_set(self, repository):
        print 'OAI request -> ', self.community_list
        try:
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            client = Client(repository.base_url, registry)
            sets = client.listSets()
        except:
            raise ValidationError('Repository cannot be accessed.')
            return None

        """ Filter records to build list of community sets """
        oai_communities = []
        for i in sets:
            set_id = i[0]
            set_name = i[1]
            """ Build collection tuples (id, human readable name) for use in dropdown """
            if set_id[:3] == 'com':
                set_data = []
                set_data.append(set_id)
                set_data.append(set_name)
                oai_communities.append(set_data)
            print i
        return oai_communities

    def __init__(self, *args, **kwargs):
        repo = kwargs.pop('repo')
        if not self.community_list:
            self.community_list = self.build_oai_set(repo)

        super(CreateCommunityForm, self).__init__(*args, **kwargs)
        print 'com list->', self.community_list #self.fields['identifier'].widget.choices

        # repository = kwargs['initial']['repository']        
        self.fields['identifier'] = forms.CharField(widget=forms.Select(choices=self.community_list))
        self.fields['identifier'].label = 'Select Community Collection to Add:'
        self.fields['repository'].empty_label = None
        

    class Meta:
        model = Community
        fields = ['identifier', 'name', 'repository']
        widgets = {'name': forms.HiddenInput()}

class CreateCollectionForm(ModelForm):
    collection_list = []

    def build_oai_collection(self, community):
        print 'OAI request collections -> ', self.collection_list
        
        """ retrieve the header data for each record in the current community repo """
        try:
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            client = Client(community.repository.base_url, registry)
            records = client.listIdentifiers(
                metadataPrefix='oai_dc', set=community.identifier)
        except:
            raise ValidationError('Repository cannot be accessed.')
            return None

        """ Filter records to build list of collections in the SET """
        remote_collections = []
        for i in records:
            for j in i.setSpec():
                if j[:3] == 'col':
                    remote_collections.append(j)

        print remote_collections
        community_collections = set(remote_collections)
        print 'set',community_collections

        """ Build collection object (id and human readable name) """
        oai_collections = []
        sets = client.listSets()
        for i in sets:
            if i[0] in community_collections:
                """ Retrieve or create a collection obj """
                set_id = i[0]
                set_name = i[1]
                """ Build collection tuples (id, human readable name) for use in dropdown """
                if set_id[:3] == 'col':
                    set_data = []
                    set_data.append(set_id)
                    set_data.append(set_name)
                    oai_collections.append(set_data)
                    print 'added' , set_data
        return oai_collections       

    def clean(self):
        cleaned_data = super(CreateCollectionForm, self).clean()

        for i in self.collection_list:
            print i
            if i[0] == cleaned_data['identifier']:
                cleaned_data['name'] = i[1]
                break

        print 'clean->', self.collection_list
        return cleaned_data

    def __init__(self, *args, **kwargs):
        community = kwargs.pop('community')
        if not self.collection_list:
            self.collection_list = self.build_oai_collection(community)
            print 'col list->', self.collection_list #self.fields['identifier'].widget.choices


        super(CreateCollectionForm, self).__init__(*args, **kwargs)

        # repository = kwargs['initial']['repository']        
        self.fields['identifier'] = forms.CharField(widget=forms.Select(choices=self.collection_list))
        self.fields['identifier'].label = 'Select Collection to Add:'
        self.fields['community'].empty_label = None

    class Meta:
        model = Collection
        fields = ['identifier', 'name', 'community']
        widgets = {'name': forms.HiddenInput()}



