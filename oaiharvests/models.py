from django.db import models

from model_utils.models import TimeStampedModel

class Repository(TimeStampedModel):

    """A digital library. Institutional -- e.g., ScholarSpace"""

    name = models.CharField(max_length=256)
    base_url = models.URLField(unique=True)

    def __unicode__(self):
        return '%s -> %s' % (self.name, self.base_url)

    def get_absolute_url(self):
        pass  # return reverse('collection', args=[str(self.id)])


class Community(TimeStampedModel):

    """A hierarchical organization of sets -- e.g., Kaipuleohone is a community collection"""

    identifier = models.CharField(primary_key=True, max_length=256)
    name = models.CharField(max_length=256, blank=True, default=None)
    repository = models.ForeignKey(Repository)

    def collections(self):
        return Collection.objects.filter(community=self)

    def __unicode__(self):
        return '%s -> %s' % (self.identifier, self.name)

    def get_absolute_url(self):
        pass  # return reverse('collection', args=[str(self.id)])


class Collection(TimeStampedModel):

    """Models the OAI standard conception of a SET"""

    identifier = models.CharField(primary_key=True, max_length=256)
    name = models.CharField(max_length=256)
    community = models.ForeignKey(Community, null=True, blank=True)

    def __unicode__(self):
        return '%s -> %s' % (self.identifier, self.name)

    def get_absolute_url(self):
        pass  # return reverse('collection', args=[str(self.id)])


class Record(TimeStampedModel):

    """OAI conception of an ITEM"""

    identifier = models.CharField(primary_key=True, max_length=256)
    hdr_datestamp = models.DateTimeField()
    hdr_setSpec = models.ForeignKey(Collection)

    def __unicode__(self):
        return self.identifier

    def get_absolute_url(self):
        pass  # return reverse('collection', args=[str(self.id)])

class MetadataElement(models.Model):

    """A tuple containing an element_type (dublin core) and its data"""
    record = models.ForeignKey(Record)
    element_type = models.CharField(max_length=256)
    element_data = models.TextField(default=' ')

    def __unicode__(self):
        return '%s -> %s' % (self.element_type, self.element_data)

    def get_absolute_url(self):
        pass  # return reverse('collection', args=[str(self.id)])



class HarvestRegistration(TimeStampedModel):
    """ Records of harvest time by collection """
    collection = models.ForeignKey(Collection)
