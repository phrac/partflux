from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from parts.models import Part
from reputation.models import ReputationAction

def home(request):
    recent_parts = Part.objects.all().only('number').order_by('-updated_at')[:10]
    recent_action = ReputationAction.objects.all().order_by('-created')[:10]
    return render_to_response('main/home.html', 
                              {'recent_action': recent_action,
                               'recent_parts': recent_parts,
                              },
                              context_instance=RequestContext(request))

def comingsoon(request):
    return render_to_response('main/comingsoon.html',
                              {},
                              context_instance=RequestContext(request))

def index(request):
    return render_to_response('main/index.html',
                              {},
                              context_instance=RequestContext(request))

def status_messages(request):
    if request.is_ajax():
        return render_to_response('partials/status_messages.html', {}, context_instance=RequestContext(request))

