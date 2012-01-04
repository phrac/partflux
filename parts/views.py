from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from parts.models import Part

def index(request):
	parts_list = Part.objects.all().order_by('created_at')[:5]
	return render_to_response('parts/index.html', 
								 {'parts_list': parts_list},
								 context_instance=RequestContext(request))

def detail(request, part_id):
	p = get_object_or_404(Part, pk=part_id)
	xrefs = p.xrefs.all()
	return render_to_response('parts/detail.html', 
								{'part': p, 'xrefs': xrefs},
							  	context_instance=RequestContext(request))


