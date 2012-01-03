from django.db import models
from django_hstore import hstore

# Create your models here.

class Part(models.Model):
	part_number = models.CharField(max_length=48)
	part_description = models.TextField()
	company = models.CharField(max_length=48)
	metadata = hstore.DictionaryField()
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	hits = models.IntegerField()
	approved = models.BooleanField()

	meta = hstore.Manager()

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ('part_number', 'company',)

class Xref(models.Model):
	part = models.ForeignKey(Part, related_name='+')
	xref = models.ForeignKey(Part, related_name='+')

	class Meta:
		unique_together = ('part', 'xref',)

	def __unicode__(self):
		return self.name
