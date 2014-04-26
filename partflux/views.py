from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from parts.models import Part
from distributors.models import DistributorSKU

def index(request):
    part_updates = Part.objects.all().order_by('-updated_at')[:7]
    dist_updates = DistributorSKU.objects.all().order_by('-updated')[:7]
    return render_to_response('main/index.html',
                              {
                                  'parts': part_updates,
                                  'skus': dist_updates,
                              },
                              context_instance=RequestContext(request))

def status_messages(request):
    if request.is_ajax():
        return render_to_response('partials/status_messages.html', {}, context_instance=RequestContext(request))

