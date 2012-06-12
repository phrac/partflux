from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from companies.models import Company
from companies.forms import CompanyAdminForm

from parts.models import Part

def index(request):
    companies_list = Company.objects.all().order_by('-created_at')
    paginator = Paginator(companies_list, 20)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        companies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        companies = paginator.page(paginator.num_pages)

    return render_to_response('companies/index.html', 
                              {'companies_list': companies}, 
                              context_instance=RequestContext(request))

def detail(request, company_slug):
    c = get_object_or_404(Company, slug=company_slug)
    parts_list = Part.objects.filter(company=c.id).order_by('-created_at')[:25]
    form = CompanyAdminForm()
    return render_to_response('companies/detail.html',
                               {'company': c,
                                'parts_list': parts_list,
                               },
                               context_instance=RequestContext(request))

def edit(request, company_slug):
    c = get_object_or_404(Company, slug=company_slug)
    if request.method == 'POST':
        form = CompanyAdminForm(request.POST, instance=c)
        if form.is_valid():
            if request.FILES.get('logo', False):
                status = uploadlogo(request, c.pk)
            print 'valid form'
            form.save()
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


def uploadlogo(request, company_id):
    c = get_document_or_404(Company, pk=company_id)
    if request.FILES.get('file', False):
        f = request.FILES['file']
    
        """Handle the file upload"""
        new_filename = "%s_%s" % (str(company_id), f.name)
        c.logo.save(new_filename, f)
        c.save()
