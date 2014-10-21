from django.db import models
from django.core.urlresolvers import reverse

from model_utils.models import TimeStampedModel

import json, operator
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
       return reverse('collection', args=[str(self.identifier)])

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
        
        return json_metadata

    def get_metadata_item(self, e_type):
        return self.metadata_items().filter(element_type=e_type)

    """Sort record dictionary by key"""
    def sort_metadata_dict(self, record_dict):
        return sorted(record_dict.items(), key=operator.itemgetter(0))

    def as_dict(self):
        record_dict = {}
        elements = self.metadataelement_set.all().order_by('element_type')
        for e in elements:
            data = json.loads(e.element_data)
            if e.element_type == 'coverage': 
                try:               
                    record_dict['coverage_lat'] = [data[0]]
                    record_dict['coverage_lng'] = [data[1]]
                except:
                    record_dict['coverage_lat'] = []
                    record_dict['coverage_lng'] = []
            else:
                record_dict[e.element_type] = data
        record_dict['collection'] = [self.hdr_setSpec]
        record_dict['site_url'] = [self.get_absolute_url()]
        return record_dict

    """Function to get the coordinates of the element to plot in map """
    def get_coordinates(self, json_position):
        coords = {
            "lat":json_position[0], 
            "lng":json_position[1]
        }
        print coords
        return coords

    def __unicode__(self):
        title = json.loads(self.get_metadata_item('title')[0].element_data)[0]
        return '%s - %s'%(self.hdr_setSpec, title)

    def get_absolute_url(self):
        return reverse('item', args=[str(self.id)])
    

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
