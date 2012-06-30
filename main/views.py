from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from parts.models import Part

def home(request):
    return render_to_response('main/index.html', 
                              {},
                              context_instance=RequestContext(request))

def comingsoon(request):
    return render_to_response('main/comingsoon.html',
                              {},
                              context_instance=RequestContext(request))

def index(request):
    recent_activity = Part.objects.all().only('number').order_by('-updated_at')[:50]
    return render_to_response('main/index.html',
                              {'recent' : recent_activity,},
                              context_instance=RequestContext(request))

def status_messages(request):
    if request.is_ajax():
        return render_to_response('partials/status_messages.html', {}, context_instance=RequestContext(request))

