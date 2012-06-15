from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core import serializers
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars
from pyes import *
import requests, json, ast
from parts.models import Part, Xref
from companies.models import Company
from search.forms import SearchForm

def index(request):
    return render_to_response('search/index.html',
                              {},
                              context_instance=RequestContext(request))

def results(request):
    #url ='http://localhost:9200/parts/part-type/'
    
    #query = {
    #    "query" : { "query_string" : {"query" : "helmet"} },
    #    "facets" : {
    #        "attributes" : { "terms" : { 
    #            "script_field" : "_source.attributes",
    #            "size":15
    #        }
    #        }
    #    }
    #}

    #query = json.dumps(query)
    #print query

    #result = requests.post(url + '_search?pretty=true', query)
    #results = json.loads(result.content)
    #facets = results['facets']['attributes']['terms']
    #facet_dict = {} 
    #for facet in facets:
    #    f = {}
    #    f_vals = []
    #    f['count'] = facet['count']
    #    terms = facet['term'].replace('=', ':').strip('{}').split(',')

    NUM_RESULTS = 20
    conn = ES('127.0.0.1:9200')
    searchform = SearchForm(request.GET)
    
    if not "q" in request.GET:
        return redirect('search.views.index')
    else:
        q = request.GET['q']

    if searchform.is_valid():
        #query = TextQuery('fulltext', q, operator='and', type='phrase_prefix')
        #query = TextQuery('fulltext',
        #                  q,
        #                  operator='and',
        #                 )
        query = StringQuery(q,
                            default_operator="AND",
                            search_fields=['number', 
                                           'company', 
                                           'desc',
                                           'attrstring',],
                           )
        s = Search(query, fields=['pgid'], size=5)
        raw_results = conn.search(s)

        results = []
        for r in raw_results:
            if r.pgid is not None:
                results.append(Part.objects.get(pk=r.pgid))
            else:
                pass

        if "page" in request.GET:                                                                    
            page = request.GET.get('page', 1)
        else:
            page = 1

        p = Paginator(results, NUM_RESULTS, request=request)
        try:
            results_list = p.page(page)
        except (PageNotAnInteger, EmptyPage):
            results_list = p.page(1)

    return render_to_response('search/results.html',
                              { 
                                  'results_list': results_list, 
                                  'searchterm': q,
                              },
                              context_instance=RequestContext(request))

def autocomplete(request):
    term = request.GET['term']
    type = request.GET['type']
    conn = ES('127.0.0.1:9200')
    
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

