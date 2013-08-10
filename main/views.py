from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from parts.models import Part

def home(request):
    recent_parts = Part.objects.all().only('number').order_by('-updated_at')[:10]
    return render_to_response('main/home.html', 
                              {
                               'recent_parts': recent_parts,
                              },
                              context_instance=RequestContext(request))

def index(request):
    recent_parts = Part.objects.all().only('number').order_by('-updated_at')[:10]
    return render_to_response('main/index.html',
                              {
                               'recent_parts': recent_parts,
                              },
                              context_instance=RequestContext(request))

def status_messages(request):
    if request.is_ajax():
        return render_to_response('partials/status_messages.html', {}, context_instance=RequestContext(request))

