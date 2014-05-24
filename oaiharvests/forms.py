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

    def __init__(self, repository, *args, **kwargs):
        super(CreateCommunityForm, self).__init__(*args, **kwargs)
        
        try:
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            client = Client(repository.base_url, registry)
            sets = client.listSets()
        except:
            # self[errors] = 'Error accessing the remote repository.'
            return

        """ Filter records to build list of community sets """
        oai_communities = []
        for i in sets:
            set_id = i[0]
            set_name = i[1]
            """ Build collection object (id and human readable name) """
            if set_id[:3] == 'com':
                set_data = []
                set_data.append(set_id)
                set_data.append(set_name)
                oai_communities.append(set_data)
        
        self.fields['identifier'] = forms.CharField(widget=forms.Select(choices=list(oai_communities)))
        self.fields['repository'].initial = repository       
        

    class Meta:
        model = Community
        fields = ['identifier', 'name', 'repository']  



