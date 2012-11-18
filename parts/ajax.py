from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from parts.models import Part, BuyLink
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
        return HttpResponseRedirect(reverse('parts.views.detail', args=[part.id, c.slug, p.slug]))

@login_required
def update_company(request):
    pk = request.POST.get('part_pk', '')
    company = request.POST.get('company', '').strip().upper()

    c, _created = Company.objects.get_or_create(name=company)

    p = get_object_or_404(Part, id=pk)

    p.company = c
    p.save()
    
    return HttpResponseRedirect(reverse('parts.views.detail', args=[p.id, c.slug, p.slug]))


@login_required
def delete_buylink(request, buylink_id):
    bl = get_object_or_404(BuyLink, id=buylink_id)
    p = get_object_or_404(Part, id=bl.part.id)
    c = get_object_or_404(Company, id=p.company.id)

    if request.user.is_staff:
        bl.delete()
        return HttpResponseRedirect(reverse('parts.views.detail', args=[p.id, c.slug, p.slug]))

