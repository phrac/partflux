from django.http import HttpResponse
from django.template.defaultfilters import truncatechars
from django.conf import settings

from pyes import *
import json

def autocomplete(request):
    """ 
    Handles jQuery XHR requests for autocomplete 
    
    """
    term = request.GET['term']
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
            results.append(r.company_name)
        if type == 'part':
            results.append({'label': "%s - %s" % (r.number,
                                                  truncatechars(r.desc,60)),
                                                  'value': r.number})

    return HttpResponse(json.dumps(results), mimetype="application/json")

