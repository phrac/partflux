from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q

from parts.models import Part, Metadata, Xref
from parts.forms import MetadataForm, XrefForm


def index(request):
	parts_list = Part.objects.all().order_by('created_at')[:5]
	return render_to_response('parts/index.html',
                           {'parts_list': parts_list},
                           context_instance=RequestContext(request))

def detail(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    
    xrefs = Xref.objects.filter(part=part_id).exclude(xrefpart=part_id)
    reverse_xrefs = Xref.objects.filter(xrefpart=part_id).exclude(part=part_id)

    metadata = Metadata.objects.filter(id=part_id)
    metaform = MetadataForm(request.POST or None)
    if metaform.is_valid():
        p = metaform.save()
        p.save()
        return HttpResponseRedirect(reverse("parts.views.detail", args=[part_id]))
    
    xrefform = XrefForm(request.POST or None)
    if xrefform.is_valid():
        part_number = xrefform.cleaned_data['part'].upper()
        desc = xrefform.cleaned_data['desc'].upper()
        company = xrefform.cleaned_data['company'].upper()
        
        newpart, created = Part.objects.get_or_create(number=part_number, company=company)
        if created == True:
            newpart.desc = desc
            newpart.hits = 0
        newpart.save()
         
        xr1, created = Xref.objects.get_or_create(part=p, xrefpart=newpart)
        
        return HttpResponseRedirect(reverse("parts.views.detail", args=[part_id]))


    return render_to_response('parts/detail.html', 
                              {'part': p, 'xrefs': xrefs, 'reverse_xrefs':
                               reverse_xrefs, 'metadata_form': metaform, 'xref_form' : xrefform},
							  	context_instance=RequestContext(request))

def search(request):
    q = request.GET.get('q', '')
    if q:
        results = Part.objects.filter(Q(number__istartswith=q) | Q(tsv__query=q))[:25]
        numresults = Part.objects.filter(Q(number__istartswith=q) | Q(tsv__query=q)).count()
    else:
        partresults = []
    
    return render_to_response('parts/index.html',
                              { 
                                  'parts_list': results, 
                                  'searchterm': q,
                                  'numresults': numresults
                              },
                              context_instance=RequestContext(request))


