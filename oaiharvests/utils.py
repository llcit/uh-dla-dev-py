# utils.py

""" 
OAIUtils : A set of utility functions that handle requests and format responses for OAI provider. 

http://www.openarchives.org/OAI/openarchivesprotocol.html
"""

from oaipmh.client import BaseClient, Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

class OAIUtils(object):
    repositories = []
    communities = []
    collections = []

    def harvest_oai_collection_records(self, collection):
        records = []
        try:
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            client = Client(collection.community.repository.base_url, registry)
            records = client.listRecords(
                metadataPrefix='oai_dc', set=collection.identifier)
        except:
            return

        return records




    def list_oai_community_sets(self, repository):

        try:
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            client = Client(repository.base_url, registry)
            sets = client.listSets()
        except:
            return

        """ Filter records to build list of community sets """
        self.communities = []
        for i in sets:
            set_id = i[0]
            set_name = i[1]
            """ Build collection tuples (id, human readable name) """
            if set_id[:3] == 'com':
                set_data = []
                set_data.append(set_id)
                set_data.append(set_name)
                self.communities.append(set_data)

        self.communities = sorted(
            self.communities, key=lambda community: community[1])

    def list_oai_collections(self, community):
        """ Retrieve the header data for each record in the current community repo """

        try:
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            client = Client(community.repository.base_url, registry)
            records = client.listIdentifiers(
                metadataPrefix='oai_dc', set=community.identifier)
        except:
            community_collections = set()
            return


        """ Filter records to build list of collections in the community set """
        community_collections = set()
        for i in records:
            for j in i.setSpec():
                if j[:3] == 'col':
                    community_collections.add(j)
    
        print len(community_collections)
        """ Build collection tuples (identifier, name) """
        for i in community_collections:
            # print i
            # print community_collections
            
            set_data = []
            set_data.append(i)  # Store identifier
            set_data.append('Collection: %s'%i)  # Store human readable name
            # print set_data
            self.collections.append(set_data)
