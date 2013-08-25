from django.db import models
from parts.models import Part, Attribute

class PartMatch(models.Model):
    part_a = models.ForeignKey(Part)
    part_b = models.ForeignKey(Part)
    match_score = models.DecimalField(max_digits=7, decimal_place=4)

    def score_part(self, part_a_id, part_b_id):
        part_a = Part.object.get(id=part_a_id)
        part_b = Part.objects.get(id=part_b_id)
        score = 0


