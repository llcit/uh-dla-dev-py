from django.db import models

class Repository(models.Model):
	name = models.CharField(max_length=256)
	base_url = models.URLField()

class Set(models.Model):
	identifier = models.CharField(max_length=256)
	repository = models.ForeignKey(Repository)

class Record(models.Model):
	identifier = models.CharField(max_length=256)
	datestamp = models.DateTimeField()
	setSpec = models.ManyToManyField(Set)


