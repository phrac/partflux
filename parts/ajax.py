from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from parts.models import Part
from companies.models import Company

@login_required
def update_description(request):
    pk = request.POST.get('pk', '')
    desc = request.POST.get('value', '').strip().upper()

    p = get_object_or_404(Part, id=pk)
    c = get_object_or_404(Company, id=p.company.id)

    p.description = desc
    p.save()

    if request.is_ajax():
       return HttpResponse() 
    else:
        return HttpResponseRedirect(reverse('parts.views.detail', args=[part_id, c.slug, p.slug]))

