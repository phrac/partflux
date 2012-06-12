from django.forms import ModelForm
from companies.models import Company

class CompanyAdminForm(ModelForm):
    class Meta:
        model = Company
