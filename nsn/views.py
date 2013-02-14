from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.template import RequestContext
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

from django.contrib.auth.models import User

from nsn.models import Nsn, Fsc, Mrc

def index(request):
    nsn_list = Nsn.objects.all()[:250]
    

    return render_to_response('nsn/index.html',
                              {'nsn_list': nsn_list},
                              context_instance=RequestContext(request))
                              
def detail(request, nsn_id, nsn_number):
    nsn = get_object_or_404(Nsn, id=nsn_id)
    
    return render_to_response('nsn/detail.html',
                              {'nsn': nsn},
                              context_instance=RequestContext(request))