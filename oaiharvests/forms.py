# oaiharvests/forms.py
from django.forms import ModelForm, ValidationError

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

    class Meta:
        model = Community
        fields = ['identifier', 'name', 'repository']
