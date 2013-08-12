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

def get_images(request, part_id):
    p = Part.objects.get(id=part_id)
    if request.is_ajax:
        return render_to_response('parts/includes/image_table.html',
                                  {'part': p,},
                                  context_instance=RequestContext(request))

@login_required
def admin_asin_search(request, part_id):
    p = Part.objects.get(id=part_id)

    if request.is_ajax:
        return render_to_response('parts/includes/admin_asin_search.html',
                                  {'part': p,},
                                  context_instance=RequestContext(request))

@login_required
def set_redirect_part(request):
    from_part = request.GET.get('from', '')
    to_part = request.GET.get('to', '')
    from_part_object = Part.objects.get(id=from_part)
    to_part_object = Part.objects.get(id=to_part)
    from_part_object.redirect_part = to_part_object
    from_part_object.save()
    to_part_object.cross_references.remove(from_part_object)

    return HttpResponseRedirect(reverse('parts.views.detail',
                                                    args=[to_part_object.id,
                                                          to_part_object.company.slug,
                                                          to_part_object.slug]))

@login_required
def delete_part(request):
    part = request.GET.get('pid', '')
    Part.objects.get(id=part).delete()

    return HttpResponseRedirect(reverse('parts.views.empty_category'))
    

