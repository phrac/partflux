from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from parts.models import Part, BuyLink, Attribute, AttributeFlag
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
    if request.user.is_staff:
        bl = get_object_or_404(BuyLink, id=buylink_id)
        p = get_object_or_404(Part, id=bl.part.id)
        c = get_object_or_404(Company, id=p.company.id)
        bl.delete()
        
        return HttpResponseRedirect(reverse('parts.views.detail', args=[p.id, c.slug, p.slug]))

@login_required
def flag(request):

    reason = request.POST.get('reason', None)
    flag_type = request.POST.get('flag-type', None)
    flag_id = request.POST.get('flag-id', None)

    if flag_type == 'attr':
        attr = Attribute.objects.get(id=flag_id)
        attrflag = AttributeFlag(reason=reason, attribute=attr,
                                 user=request.user, active=True)
        attrflag.save()


    if request.is_ajax:
        return HttpResponse()
