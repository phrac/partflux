from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User


from parts.models import Part, Xref
from partgroups.models import PartGroup
from companies.models import Company
from partgroups.forms import PartGroupForm


def index(request):
    user_partgroups = PartGroup.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        partgroupform = PartGroupForm(request.POST)
        if partgroupform.is_valid():
            name = partgroupform.cleaned_data['name']
            desc = partgroupform.cleaned_data['description']
            private = partgroupform.cleaned_data['private']
            newgroup, _created = PartGroup.objects.get_or_create(name=name,
                                                             user=request.user)
            if _created == True:
                newgroup.description = desc
                newgroup.private = private
                newgroup.save()
            """ redirect back to clear the form """
            return HttpResponseRedirect(reverse('partgroups.views.index'))


    else:
        partgroupform = PartGroupForm()
    return render_to_response('partgroups/index.html',
                              {'partgroup_form': partgroupform,
                               'user_partgroups': user_partgroups,
                              },
                              context_instance=RequestContext(request))


def detail(request, partgroup_id):
    pg = get_object_or_404(PartGroup, pk=partgroup_id)

    
