from django.db import models

class Repository(models.Model):
	name = models.CharField(max_length=256)
	base_url = models.URLField()

class Community(models.Model):
	identifier = models.CharField(max_length=256)
	name = models.CharField(max_length=256)
	repository = models.ForeignKey(Repository)

class Set(models.Model):
	identifier = models.CharField(max_length=256)
	name = models.CharField(max_length=256)
	repository = models.CharField(max_length=256)
	

class Record(models.Model):
	identifier = models.CharField(max_length=256)
	datestamp = models.DateTimeField()
	setSpec = models.ManyToManyField(Set)


