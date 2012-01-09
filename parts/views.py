from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User


from parts.models import Part, Metadata, Xref
from companies.models import Company
from parts.forms import MetadataForm, XrefForm


def index(request):
    parts_list = Part.objects.all().order_by('created_at')
    paginator = Paginator(parts_list, 20)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        parts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        parts = paginator.page(paginator.num_pages)

    return render_to_response('parts/index.html',
                           {'parts_list': parts},
                           context_instance=RequestContext(request))

def detail(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    
    xrefs = Xref.objects.filter(part=part_id).exclude(xrefpart=part_id)
    reverse_xrefs = Xref.objects.filter(xrefpart=part_id).exclude(part=part_id)

    metadata = Metadata.objects.filter(part=part_id)
    
    metaform = MetadataForm(request.POST or None)
    xrefform = XrefForm(request.POST or None)

    if request.user.is_authenticated():
        if metaform.is_valid():
            key = metaform.cleaned_data['key']
            value = metaform.cleaned_data['value']
            meta, _created = Metadata.objects.get_or_create(part=p, key=key)
            if _created == True:
                meta.user = request.user
                meta.values.append(value)
            else:
                if meta.values.count(value) == 0:
                    meta.values.append(value)
            meta.save()
            return HttpResponseRedirect(reverse("parts.views.detail", args=[part_id]))
    
    if request.user.is_authenticated():
        if xrefform.is_valid():
            part_number = xrefform.cleaned_data['part']
            desc = xrefform.cleaned_data['desc']
            company = xrefform.cleaned_data['company']
            # first we need to get the company or create it if it doesn't exist
            c, _created = Company.objects.get_or_create(name=company)
            # next, check if the cross referenced part exists and create it if it does not
            newpart, _created = Part.objects.get_or_create(number=part_number, company=c)
            if _created == True:
                newpart.user = request.user
                newpart.desc = desc
                newpart.hits = 0
                newpart.save()
         
            xr1, _created = Xref.objects.get_or_create(part=p, xrefpart=newpart)
            if _created == True:
                xr1.user = request.user
                xr1.save()
            return HttpResponseRedirect(reverse("parts.views.detail", args=[part_id]))

    # default response (do we need to clean this up so that forms aren't sent
    # for unauthenticated users?
    return render_to_response('parts/detail.html', 
                              {'part': p, 
                               'metadata': metadata, 
                               'xrefs': xrefs, 
                               'reverse_xrefs': reverse_xrefs, 
                               'metadata_form': metaform, 
                               'xref_form' : xrefform},
                              context_instance=RequestContext(request))


"""
process and display search results for users

"""
def search(request):
    q = request.GET.get('q', '')
    if q:
        results = Part.objects.filter(Q(number__istartswith=q) |
                                      Q(tsv__query=q)).distinct().defer('tsv')
    else:
        results = []
    
    paginator = Paginator(results, 20)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        parts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        parts = paginator.page(paginator.num_pages)

    
    return render_to_response('parts/index.html',
                              { 
                                  'parts_list': parts, 
                                  'searchterm': q,
                              },
                              context_instance=RequestContext(request))


