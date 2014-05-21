from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib import messages

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

from .models import Repository, Community, Collection, MetadataElement, Record
# from .forms import BrowseRepositoryForm


class RepositoryListView(ListView):
    model = Community
    template_name = 'harvester_list_repos.html'

    def get_context_data(self, **kwargs):
        context = super(RepositoryListView, self).get_context_data(**kwargs)
        # context['communities'] = selt.get_object().set_community.all()
        return context


class HarvesterBrowseRepoView(TemplateView):

    """
    Browse an institutional repository for selective harvesting. A repository should be seen as
    a collection of records. A repo can be a full digital library or a
    community with the library.

    Expected keyword argument is a string representing a community collection identifier
    """
    template_name = 'harvester_collector.html'

    def get_context_data(self, **kwargs):
        context = super(
            HarvesterBrowseRepoView, self).get_context_data(**kwargs)
        repo_id = kwargs.pop('set')

        """ Verify current SET is a community type and initialize repo object """
        try:
            if repo_id[:3] == 'com':
                repo = Community.objects.get(pk=repo_id)
            else:
                raise
        except:
            messages.add_message(
                self.request, messages.ERROR, 'Selected repository is not registered with this site.')
            return context

        registered_collections = Collection.objects.filter(community=repo)
        registered_id_list = registered_collections.values_list(
            'identifier', flat=True)

        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        client = Client(repo.repository.base_url, registry)

        try:
            records = client.listRecords(
                metadataPrefix='oai_dc', set=repo.identifier)
        except:
            messages.add_message(
                self.request, messages.ERROR, 'Repository or Collection with id ' + repo_id + ' was not found.')
            return context

        """ Filter collections from records to build list of collections in the SET """
        repo_collection_identifiers = []
        for i in records:
            for j in i[0].setSpec():
                if j[:3] == 'col':
                    if j not in registered_id_list and j not in repo_collection_identifiers:
                        repo_collection_identifiers.append(j)

        # try:
        #     institutional_repo = Repository.objects.get(base_url=URL)
        # except:
        #     institutional_repo = Repository()
        #     institutional_repo.name = NAME
        #     institutional_repo.base_url = URL

        # institutional_repo.save()

        # if REPO_ID[:3] == 'com':

        #     try:
        #         community_repo = Community.objects.get(identifier=REPO_ID)
        #     except:
        #         community_repo = Community()
        #         community_repo.identifier = REPO_ID
        #         community_repo.name = ''
        #         community_repo.repository = institutional_repo

        #     community_repo.save()

        """ Build dictionary of collections for possible harvesting """
        sets = client.listSets()

        collections = dict()
        for i in sets:
            if i[0] in repo_collection_identifiers:
                collections[i[0]] = i[1]
                # try:
                #     collection = Collection.objects.get(pk=i[0])
                # except:
                #     collection = Collection()
                #     collection.identifier = i[0]
                #     collection.name = i[1]
                #     collection.community = community_repo or None

                # try:
                #     collection.save()
                # except:
                #     pass

        context['repository'] = repo
        context['registered_collections'] = registered_collections
        context['collections'] = collections
        return context


class HarvesterView(TemplateView):

    """Harvest records from a given set"""
    template_name = 'harvester.html'

    def get_context_data(self, **kwargs):
        context = super(HarvesterView, self).get_context_data(**kwargs)

        URL = 'http://scholarspace.manoa.hawaii.edu/dspace-oai/request'
        SET_ID = kwargs.pop('set')  # 'com_10125_4250'
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
