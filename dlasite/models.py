from django.db import models
from django.core.urlresolvers import reverse


class MetadataType(models.Model):
    set_type = models.CharField(max_length=96)  # Add Choices here...
    name = models.CharField(max_length=96)
    description = models.CharField(max_length=512)
    comment = models.CharField(null=True, default=None)


class Collection(models.Model):
    public = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('collection', args=[str(self.id)])


class Item(models.Model):
    collection = models.ForeignKey(Collection)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item', args=[str(self.id)])


class Element(models.Model):
	item = models.ForeignKey(Item)
    metadata_type = models.ForeignKey(MetadataType)
    data = models.TextField()

    def __unicode__(self):
        return '%s - %s' % (metadata_type, data)
