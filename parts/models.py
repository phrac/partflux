from django.db import models
from django_orm.postgresql import hstore
from django_orm.postgresql.fts.fields import VectorField
from django_orm.manager import FtsManager as SearchManager

"""
Stores a single part number
Many to many relationship with itself
"""

class Part(models.Model):
	number = models.CharField(max_length=48)
	description = models.TextField()
	company = models.CharField(max_length=48)
	metadata = hstore.DictionaryField()
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	hits = models.IntegerField()
	approved = models.BooleanField()
	xrefs = models.ManyToManyField('Part')
	tsv = VectorField()
	
	objects = SearchManager(
          	search_field = 'tsv',
			fields = 'description',
	)

	def __unicode__(self):
		return self.number

	class Meta:
		unique_together = ('number', 'company',)
	
	def save(self):
		super(Part, self).save()
		if hasattr(self, '_orm_manager'):
			self._orm_manager.update_index(pk=self.pk)
