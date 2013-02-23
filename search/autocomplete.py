from django.http import HttpResponse, HttpResponseNotFound
from django.template.defaultfilters import truncatechars
from django.conf import settings
from haystack.query import SearchQuerySet

import json

def autocomplete(request):
    sqs = SearchQuerySet().filter(content_auto=request.GET.get('q', ''))[:5]
    suggestions = ['one', 'two', 'three',]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps(suggestions)
    return HttpResponse(the_data, content_type='application/json')

