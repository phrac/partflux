from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User


from parts.models import Part, Xref
from companies.models import Company
from parts.forms import MetadataForm, XrefForm, SearchForm


def index(request):
    parts_list = Part.objects.all().order_by('-created_at')[:25]
    
    return render_to_response('parts/index.html',
                              {'parts_list': parts_list},
                              context_instance=RequestContext(request))

def detail(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    
    xrefs = Xref.objects.filter(part=part_id).exclude(xrefpart=part_id)
    reverse_xrefs = Xref.objects.filter(xrefpart=part_id).exclude(part=part_id)
    
    metaform = MetadataForm(None)
    xrefform = XrefForm(None)

    if 'metadata_button' in request.POST:
        metaform = MetadataForm(request.POST)
        if metaform.is_valid:
            addmeta(request, part_id)
            return HttpResponseRedirect(reverse('parts.views.detail', args=[part_id]))

    if 'xref_button' in request.POST:
        xrefform = XrefForm(request.POST)
        if xrefform.is_valid:
            addxref(request, part_id)
            return HttpResponseRedirect(reverse('parts.views.detail', args=[part_id]))

    return render_to_response('parts/detail.html', 
                              {'part': p, 
                               'metadata': sorted(p.metadata.iteritems()),
                               'xrefs': xrefs, 
                               'reverse_xrefs': reverse_xrefs, 
                               'metadata_form': metaform, 
                               'xref_form' : xrefform
                              },
                              context_instance=RequestContext(request))

def addmeta(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    metaform = MetadataForm(request.POST)
    if metaform.is_valid():
        key = metaform.cleaned_data['key'].strip().upper()
        value = metaform.cleaned_data['value'].strip().upper()
        p.metadata[key] = value
        p.save()
        
def addpart(request):
    if request.method == 'POST':
        partform = XrefForm(request.POST)
        if partform.is_valid():
            part_number = partform.cleaned_data['part'].upper()
            desc = partform.cleaned_data['desc'].upper()
            company = partform.cleaned_data['company'].upper()
            # first we need to get the company or create it if it doesn't exist
            c, _created = Company.objects.get_or_create(name=company)
            # next, check if the cross referenced part exists and create it if it does not
            newpart, _created = Part.objects.get_or_create(number=part_number, company=c)
            if _created == True:
                newpart.user = request.user
                newpart.description = desc
                newpart.hits = 0
                newpart.save()
            return HttpResponseRedirect('/parts/%d/%s/' % (newpart.id, newpart.number,))
    else:
        partform = XrefForm()

    return render_to_response('parts/add.html',
                              {'partform': partform,},
                              context_instance=RequestContext(request))


def addxref(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    xrefform = XrefForm(request.POST)
    print 'adding xref' 
    if xrefform.is_valid():
        part_number = xrefform.cleaned_data['part'].upper()
        company = xrefform.cleaned_data['company'].upper()
        # first we need to get the company or create it if it doesn't exist
        c, _created = Company.objects.get_or_create(name=company)
        # next, check if the cross referenced part exists and create it if it does not
        newpart, _created = Part.objects.get_or_create(number=part_number, company=c)
        if _created == True:
            newpart.user = request.user
            newpart.description = p.description
            newpart.hits = 0
            newpart.save()
         
        xr1, _created = Xref.objects.get_or_create(part=p, xrefpart=newpart)
        if _created == True:
            xr1.user = request.user
            xr1.save()
    


