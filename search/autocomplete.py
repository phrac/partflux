from django.http import HttpResponse, HttpResponseNotFound
from django.template.defaultfilters import truncatechars
from django.conf import settings
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery
from django.http import Http404

import json

def autocomplete(request):
    if request.is_ajax():
        type = request.GET.get('type', '')
        q = request.GET.get('q', '')
        print 'AUTOCOMPLETE: %s' % q
        if q.__len__() < 3:
            return HttpResponse()
        suggestions = []
        if type == 'company':
            sqs = SearchQuerySet().filter(name__startswith=q)[:5]
            suggestions = [result.object.name for result in sqs]
        else:
            sqs = SearchQuerySet().filter(content__startswith=q)[:5]
            for result in sqs:
                if result.object.number:
                    suggestions.append(result.object.number)
                else:
                    pass
        
        the_data = json.dumps(suggestions)
        return HttpResponse(the_data, content_type='application/json')

    else:
        raise Http404


