from django.http import HttpResponse, HttpResponseNotFound
from django.template.defaultfilters import truncatechars
from django.conf import settings
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

import json

def autocomplete(request):
    q = request.GET.get('q', '')
    sqs = SearchQuerySet().filter(content__startswith=q)[:5]
    suggestions = [result.object.number for result in sqs]
    the_data = json.dumps(suggestions)
    return HttpResponse(the_data, content_type='application/json')

