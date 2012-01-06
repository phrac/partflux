from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q

from parts.models import Part
from parts.forms import MetadataForm


def index(request):
	parts_list = Part.objects.all().order_by('created_at')[:5]
	return render_to_response('parts/index.html',
                           {'parts_list': parts_list},
                           context_instance=RequestContext(request))

def detail(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    xrefs = p.xrefs.all()
    metaform = MetadataForm(request.POST or None, instance=p)
    if metaform.is_valid():
        p = metaform.save()
        p.save()
        return HttpResponseRedirect(reverse("parts.views.detail", args=[part_id]))

    return render_to_response('parts/detail.html', 
								{'part': p, 'xrefs': xrefs, 'metadata_form': metaform},
							  	context_instance=RequestContext(request))

def search(request):
	q = request.GET.get('q', '')
	if q:
		#partresults = Part.ft.filter(number__istartswith=q).defer("metadata", "tsv")[:25]
		#ftresults = Part.ft.search(q).defer("metadata", "tsv")[:25]
		
		results = Part.objects.filter(
                                        Q(number__istartswith=q) |
								        Q(tsv__query=q)
							        )[:25]
		
		numresults = Part.objects.filter(
							            Q(number__istartswith=q) |
            							Q(tsv__query=q)
			            				).count()
	else:
		partresults = []
	return render_to_response('parts/index.html',
								{ 
									'parts_list': results, 
									'searchterm': q,
									'numresults': numresults
								},
								context_instance=RequestContext(request))


