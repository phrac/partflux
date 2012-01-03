from django.db import models
from django_hstore import hstore

# Create your models here.


class Part(models.Model):
	number = models.CharField(max_length=48)
	description = models.TextField()
	company = models.CharField(max_length=48)
	metadata = hstore.DictionaryField()
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	hits = models.IntegerField()
	approved = models.BooleanField()
	#xrefs = models.ManyToManyField(Xref)
	objects = hstore.Manager()

	def __unicode__(self):
		return self.number

	class Meta:
		unique_together = ('number', 'company',)

class Xref(models.Model):
	origpart = models.ForeignKey(Part, related_name='+')
	xrefpart = models.ForeignKey(Part, related_name='+')

	class Meta:
		unique_together = ('origpart', 'xrefpart',)

	def __unicode__(self):
		return self.origpart

