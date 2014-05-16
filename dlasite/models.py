from django.db import models


class Collection(models.Model):

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('', args=[str(self.id)])


class Record(models.Model):

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('', args=[str(self.id)])


class Element(models.Model):
	
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('', args=[str(self.id)])
