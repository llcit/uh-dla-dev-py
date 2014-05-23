from django.db import models
from django.core.urlresolvers import reverse

from model_utils.models import TimeStampedModel

class Repository(TimeStampedModel):

    """ A institutional digital library OAI service provider -- e.g., ScholarSpace """

    name = models.CharField(max_length=256)
    base_url = models.URLField(unique=True)

    def list_communities(self):
        return self.community_set.all()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('repository', args=[str(self.id)])


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
        return reverse('community', args=[str(self.identifier)])


class Collection(TimeStampedModel):

    """Models the OAI standard conception of a SET"""

    identifier = models.CharField(primary_key=True, max_length=256)
    name = models.CharField(max_length=256)
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

    identifier = models.CharField(primary_key=True, max_length=256)
    hdr_datestamp = models.DateTimeField()
    hdr_setSpec = models.ForeignKey(Collection)

    def remove_data(self):
        data = MetadataElement.objects.filter(record=self)
        try:
            self.metadataelement_set.remove(data)
        except:
            pass
        return

    def metadata_items(self):
        return self.metadataelement_set.all()

    def __unicode__(self):
        return '%s...%s'%(self.hdr_setSpec, self.identifier[20:])

    def get_absolute_url(self):
        pass  # return reverse('collection', args=[str(self.id)])

class MetadataElement(models.Model):

    """A tuple containing an element_type (dublin core) and its data"""
    record = models.ForeignKey(Record, null=True)
    element_type = models.CharField(max_length=256)
    element_data = models.TextField(default='')

    def __unicode__(self):
        return u'%s'%self.element_type

    def get_absolute_url(self):
        pass  # return reverse('collection', args=[str(self.id)])

class HarvestRegistration(TimeStampedModel):
    """ Records of harvested collections """
    collection = models.ForeignKey(Collection)
    harvest_date = models.DateTimeField()
