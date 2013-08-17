from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from parts.models import Part

def index(request):
    return render_to_response('main/comingsoon.html',
                              {
                              },
                              context_instance=RequestContext(request))

def status_messages(request):
    if request.is_ajax():
        return render_to_response('partials/status_messages.html', {}, context_instance=RequestContext(request))

