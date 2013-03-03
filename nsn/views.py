from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.template import RequestContext
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from haystack.query import SearchQuerySet

from django.contrib.auth.models import User

from nsn.models import Nsn, Fsc, Mrc

def index(request):
    nsns = Nsn.objects.all().only('number').order_by('number')
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    p = Paginator(nsns, 25, request=request, reltuple=True)
    try:
        nsn_list = p.page(page)
    except (PageNotAnInteger, EmptyPage):
        nsn_list = p.page(1)

    return render_to_response('nsn/index.html',
                              {'nsn_list': nsn_list,
                               'page_num': page,
                              },
                              context_instance=RequestContext(request))
                              
def detail(request, nsn_id, nsn_number):
    nsn = get_object_or_404(Nsn, id=nsn_id, number=nsn_number)
    mlt = SearchQuerySet().more_like_this(nsn)[:20]
    
    return render_to_response('nsn/detail.html',
                              {'nsn': nsn,
                               'mlt': mlt,
                               },
                              context_instance=RequestContext(request))
