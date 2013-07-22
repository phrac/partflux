from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.files.storage import default_storage
import json

from parts.models import Part, PartImage, Attribute, Category
from companies.models import Company
from users.models import UserFavoritePart

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
def delete_image(request):
    if request.user.is_staff:
        image_id = request.POST.get('image-id', '')
        part_id = request.POST.get('part-id', None)
        img = get_object_or_404(PartImage, pk=image_id)
        part = get_object_or_404(Part, pk=part_id)
        part.images.remove(img)
        img.delete()
        if request.is_ajax:
            return render_to_response('parts/includes/image_table.html',
                                      {'part': part, },
                                      context_instance=RequestContext(request))
        
        
@login_required
def flag(request):

    reason = request.POST.get('reason', None)
    flag_type = request.POST.get('flag-type', None)
    flag_id = request.POST.get('flag-id', None)
    pk = request.POST.get('part_pk', '')
    p = get_object_or_404(Part, id=pk)
    
    if flag_type == 'attr':
        attr = Attribute.objects.get(id=flag_id)
        attrflag = AttributeFlag(reason=reason, attribute=attr,
                                 user=request.user, active=True)
        attrflag.save()


    if request.is_ajax:
        return render_to_response('parts/includes/attribute_table.html',
                                          {'part': p, },
                                          context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('parts.views.detail', args=[part.id, c.slug, p.slug]))

@login_required
def add_favorite(request):
    pk = request.POST.get('part_pk', '')
    notes = request.POST.get('notes', '')
    p = get_object_or_404(Part, id=pk)

    favepart = UserFavoritePart(user=request.user, part=p, notes=notes)
    favepart.save()

    if request.is_ajax:
        return HttpResponse()
    else:
        return HttpResponseRedirect(reverse('parts.views.detail', args=[part.id, c.slug, p.slug]))
        
@login_required
def delete_favorite(request):
    fave_id = request.POST.get('fave-id', '')
    fave = get_object_or_404(UserFavoritePart, id=fave_id, user=request.user)
    fave.delete()
    
    fave_parts = UserFavoritePart.objects.filter(user=request.user)

    if request.is_ajax:
        return render_to_response('users/includes/faveparts-table.html',
                                 {'fave_parts': fave_parts,},
                                 context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('parts.views.detail', args=[part.id, c.slug, p.slug]))
        
@login_required
def get_parent_categories(request):
    categories = {}
    c = Category.objects.filter(parent=None).order_by('name')
    for cat in c:
        categories[cat.id] = cat.name
    return HttpResponse(json.dumps(categories), content_type='application/json')
    
@login_required
def get_child_categories(request, parent_id):
    categories = {}
    c = Category.objects.filter(parent=parent_id).order_by('name')
    for cat in c:
        categories[cat.id] = cat.name
    return HttpResponse(json.dumps(categories), content_type='application/json')
    
def get_distributors(request, part_id):
    p = Part.objects.get(id=part_id)

    if request.is_ajax:
        return render_to_response('parts/includes/buylink_table.html',
                                  {'part': p,},
                                  context_instance=RequestContext(request))


