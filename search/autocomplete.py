from django.http import HttpResponse, HttpResponseNotFound
from django.template.defaultfilters import truncatechars
from django.conf import settings

from pyes import *
import json

def autocomplete(request):
    """ 
    Handles jQuery XHR requests for autocomplete 
    
    """
    if request.is_ajax():
        if not "term" in request.GET:
            return HttpResponseNotFound()
        else:
            term = request.GET['term']
        if not "type" in request.GET:
            return HttpResponseNotFound()
        else:
            type = request.GET['type']

        conn = ES(settings.ES_HOST)

        if type == 'company':
            query = PrefixQuery(field='company_name', prefix=term )
        if type == 'part':
            query = PrefixQuery(field='number',prefix=term)

        s = Search(query, fields=['company_name', 'number', 'desc'], size=10)
        raw_results = conn.search(s)

        results = []
        for r in raw_results:
            if type == 'company':
                results.append({'label': r.company_name})
            if type == 'part':
                results.append({'label': r.number })

        return HttpResponse(json.dumps(results), mimetype="application/json")
    else:
        return HttpResponseNotFound('ajax only')

