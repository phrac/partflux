from django.forms import ModelForm
from parts.models import Part

class MetadataForm(ModelForm):
    class Meta:
        model = Part
        fields = ('metadata',)
