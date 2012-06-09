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
        form = CompanyAdminForm(request.POST)
        if form.is_valid():
            c.name = form.cleaned_data['name']
            c.desc = form.cleaned_data['description']
            if form.cleaned_data['url']:
                c.url = form.cleaned_data['url']
            if form.cleaned_data['wikipedia_url']:
                c.wp_url = form.cleaned_data['wikipedia_url']
            if form.cleaned_data['facebook_url']:
                c.fb_url = form.cleaned_data['facebook_url']
            if form.cleaned_data['twitter_url']:
                c.tw_url = form.cleaned_data['twitter_url']
            if form.cleaned_data['linkedin_url']:
                c.lnkin_url = form.cleaned_data['linkedin_url']
            if form.cleaned_data['email']:
                c.email = form.cleaned_data['email']
            c.p = form.cleaned_data['phone']
            c.f = form.cleaned_data['fax']
            c.add1 = form.cleaned_data['address1']
            c.add2 = form.cleaned_data['address2']
            c.city = form.cleaned_data['city']
            c.st = form.cleaned_data['state']
            c.cntry = form.cleaned_data['country']
            c.zip = form.cleaned_data['zipcode']
            c.save()

            if request.FILES.get('logo', False):
                status = uploadlogo(request, c.pk)
            request.flash.success = "Company details successfully saved."
            return HttpResponseRedirect(reverse('companies.views.detail',
                                                args=[c.slug]))
        else:
            print 'form not valid'
        
    else:
        form = CompanyAdminForm({'name': c.name, 
                                 'description': c.desc,
                                 'url': c.url,
                                 'wikipedia_url': c.wp_url,
                                 'facebook_url': c.fb_url,
                                 'twitter_url': c.tw_url,
                                 'linkedin_url': c.lnkin_url,
                                 'email': c.email,
                                 'phone': c.p,
                                 'fax': c.f,
                                 'address1': c.add1,
                                 'address2': c.add2,
                                 'city': c.city,
                                 'state': c.st,
                                 'zipcode': c.zip,
                                 'country': c.cntry,})

    return render_to_response('companies/edit.html',
                               {'company': c,
                                'form': form,
                               },
                               context_instance=RequestContext(request))


def uploadlogo(request, company_id):
    c = get_document_or_404(Company, pk=company_id)
    if request.FILES.get('logo', False):
        f = request.FILES['logo']
        new_filename = "logo_%s_%s" % (str(company_id), f.name)

        try:
            c.logo.delete()
            c.logo.put(f, filename=new_filename)
            c.save()
            return True

        except ValidationError:
            fs.delete(new_filename)
            return 'File is not an image.'
