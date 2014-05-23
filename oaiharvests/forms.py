# oaiharvests/forms.py
from django.forms import ModelForm

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

from .models import Repository

class CreateRepositoryForm(ModelForm):
    def clean(self):
        cleaned_data = super(CreateRepositoryForm, self).clean()
        
        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        try:
            client = Client(cleaned_data.get('base_url'), registry)
            server = client.identify()
        except:
        	print 'BAD URL!:', cleaned_data.get('base_url')
            # raise ValidationError('Repository base url is invalid.')

        return self.cleaned_data

    class Meta:
	    model = Repository
	    fields = ['base_url']