from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required

from companies.models import Company
from companies.forms import CompanyAdminForm

from parts.models import Part
import os

def index(request):
    companies = Company.objects.all().order_by('name')

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    p = Paginator(companies, 25, request=request)
    try:
        results_list = p.page(page)
    except (PageNotAnInteger, EmptyPage):
        results_list = p.page(1)

    return render_to_response('companies/index.html', 
                              {'results_list': results_list}, 
                              context_instance=RequestContext(request))
                              
def redirect_new_page(request, company_slug):
    c = get_object_or_404(Company, slug=company_slug) 
    return HttpResponsePermanentRedirect(reverse('companies.views.detail', args=[c.id, c.slug]))

def detail(request, company_id, company_slug):
    c = get_object_or_404(Company, id=company_id)
    parts_list = Part.objects.filter(company=c.id).order_by('-created_at')
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    p = Paginator(parts_list, 25, request=request)
    try:
        results_list = p.page(page)
    except (PageNotAnInteger, EmptyPage):
        results_list = p.page(1)
    form = CompanyAdminForm()
    return render_to_response('companies/detail.html',
                               {'company': c,
                                'parts_list': results_list,
                               },
                               context_instance=RequestContext(request))

@login_required
def edit(request, company_slug):
    c = get_object_or_404(Company, slug=company_slug)
    if request.method == 'POST':
        form = CompanyAdminForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            if request.FILES.get('logo', False):
                status = uploadlogo(request, c.pk)
            
            request.flash.success = "Company details successfully saved."
            return HttpResponseRedirect(reverse('companies.views.detail',
                                                args=[c.slug]))
        else:
            print form.errors
    else:
        form = CompanyAdminForm(instance=c)
        
    return render_to_response('companies/edit.html',
                               {'company': c,
                                'form': form,
                               },
                               context_instance=RequestContext(request))


### this should really be in forms.py under the CompanyAdminForm
@login_required
def uploadlogo(request, company_id):
    c = get_object_or_404(Company, pk=company_id)
    if request.FILES.get('logo', False):
        f = request.FILES['logo']
    
        """Handle the file upload"""
        ext = os.path.splitext(f.name)[1]
        ext = ext.lower()
        new_filename = "%s_%s%s" % (str(c.pk), str(c.slug), ext)
        if c.logo:
            default_storage.delete(c.logo)
        c.logo = new_filename
        c.logo.save(new_filename, f)
        c.save()
