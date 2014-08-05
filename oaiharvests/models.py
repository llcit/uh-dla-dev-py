from django.db import models
from django.core.urlresolvers import reverse

from model_utils.models import TimeStampedModel

import json
import pdb #pdb.set_trace()

class Repository(TimeStampedModel):

    """ A institutional digital library OAI service provider -- e.g., ScholarSpace """

    name = models.CharField(max_length=256)
    base_url = models.URLField(unique=True)

    def list_communities(self):
        return self.community_set.all()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('oai_repository', args=[str(self.id)])


class Community(TimeStampedModel):

    """A hierarchical organization of sets -- e.g., Kaipuleohone is a community collection"""

    identifier = models.CharField(primary_key=True, max_length=256)
    name = models.CharField(max_length=256, blank=True, default=None)
    repository = models.ForeignKey(Repository)

    def list_collections(self):
        return self.collection_set.all()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('oai_community', args=[str(self.identifier)])


class Collection(TimeStampedModel):

    """Models the OAI standard conception of a SET"""

    identifier = models.CharField(primary_key=True, max_length=256)
    name = models.CharField(max_length=256, blank=True)
    community = models.ForeignKey(Community, null=True, blank=True)

    def count_records(self):
        return self.record_set.all().count()

    def list_records(self):
        return self.record_set.all()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
       return reverse('oai_collection', args=[str(self.identifier)])

class Record(TimeStampedModel):

    """OAI conception of an ITEM"""
    identifier = models.CharField(max_length=256, unique=True)
    hdr_datestamp = models.DateTimeField()
    hdr_setSpec = models.ForeignKey(Collection)

    def remove_data(self):
        MetadataElement.objects.filter(record=self).delete()
        return

    def metadata_items(self):
        return self.metadataelement_set.all()

    def metadata_items_json(self):
        json_metadata = {}
        elements = self.metadataelement_set.all()
        for metadata in elements:
            if json.loads(metadata.element_data):
                json_metadata[metadata.element_type]=(json.loads(metadata.element_data)[0])
            # else:
            #     json_metadata[metadata.element_type]= []
        return json_metadata

    def get_metadata_item(self, e_type):
        return self.metadata_items().filter(element_type=e_type)

    def __unicode__(self):
        return '%s - %s'%(self.hdr_setSpec, self.get_metadata_item('title')[0].element_data)

    def get_absolute_url(self):
        return reverse('item', args=[str(self.id)])

    """Function to get the coordinates of the element to plot in map """
    def get_coordinates(self,position):
        #Get languages
        if json.loads(self.get_metadata_item('language')[0].element_data):
            language = ""
            for each in json.loads(self.get_metadata_item('language')[0].element_data):
                language = language + " " + each
        else:
            language = "No info"
        #Get contributors
        if json.loads(self.get_metadata_item('contributor')[0].element_data):
            contributors = ""
            for each in json.loads(self.get_metadata_item('contributor')[0].element_data):
                contributors = contributors + " " + each
        else:
            contributors = "No info"
        dict = {"Record":json.loads(self.get_metadata_item('title')[0].element_data)[0],"Date":json.loads(self.get_metadata_item('date')[0].element_data)[0],"Contributor":contributors,"Language":language,"North":position[0], "East":position[1]}   
        
        return dict

    

class MetadataElement(models.Model):

    """A tuple containing an element_type (dublin core) and its data"""
    record = models.ForeignKey(Record, null=True)
    element_type = models.CharField(max_length=256)
    element_data = models.TextField(default='')

    def __unicode__(self):
        return u'%s:%s'%(self.element_type, self.element_data)

    def get_absolute_url(self):
        pass  # return reverse('collection', args=[str(self.id)])

class HarvestRegistration(TimeStampedModel):
    """ Records of harvested collections """
    collection = models.ForeignKey(Collection)
    harvest_date = models.DateTimeField()
