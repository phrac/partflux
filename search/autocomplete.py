from django.http import HttpResponse, HttpResponseNotFound
from django.template.defaultfilters import truncatechars
from django.conf import settings
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery
from django.http import Http404
from parts.models import Category, Part

import json

def autocomplete(request):
    type = request.GET.get('type', '')
    q = request.GET.get('q', '')
    if q.__len__() < 3:
        return HttpResponse()
    suggestions = []
    if type == 'company':
        sqs = SearchQuerySet().filter(name__startswith=q)[:10]
        suggestions = [result.object.name for result in sqs]
    elif type == 'category':
        sqs = SearchQuerySet().models(Category).filter(text__startswith=q)[:10]
        suggestions = [result.object.name for result in sqs]        
    else:
        sqs = SearchQuerySet().models(Part).filter(text__startswith=q)[:10]
        for result in sqs:
            suggestions.append(result.object.number)
    
    the_data = json.dumps(suggestions)
#        return HttpResponse(the_data, content_type='application/json')

    return HttpResponse(the_data, content_type='application/json')

