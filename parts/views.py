from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db import IntegrityError
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

from parts.models import Part, Xref, PartImage, BuyLink
from companies.models import Company
from parts.forms import MetadataForm, XrefForm, ImageUploadForm, BuyLinkForm

def index(request):
    parts_list = Part.objects.all().order_by('-created_at')[:25]

    return render_to_response('parts/index.html',
                              {'parts_list': parts_list},
                              context_instance=RequestContext(request))

def detail(request, company_slug, part_slug):
    c = get_object_or_404(Company, slug=company_slug)
    p = get_object_or_404(Part, slug=part_slug, company=c.id)
    #p.hits += 1
    #p.save()
    
    xrefs = Xref.objects.filter(part=p.id).exclude(xrefpart=p.id)
    reverse_xrefs = Xref.objects.filter(xrefpart=p.id).exclude(part=p.id)
    buylinks = BuyLink.objects.filter(part=p.id).order_by('price')[:10]

    metaform = MetadataForm(None)
    xrefform = XrefForm(None)
    imageuploadform = ImageUploadForm(None)
    buylinkform = BuyLinkForm(None)

    if 'buylink_button' in request.POST:
        buylinkform = BuyLinkForm(request.POST)
        if buylinkform.is_valid:
            status = addbuylink(request, p.pk)
            if status is True:
                request.flash.success = "URL added successfully"
            else:
                request.flash.error = "Adding URL failed: %s" % status
            return HttpResponseRedirect(reverse('parts.views.detail', args=[p.company.slug, p.slug]))

    if 'metadata_button' in request.POST:
        metaform = MetadataForm(request.POST)
        if metaform.is_valid:
            status = addmeta(request, p.pk)
            if status is True:
                request.flash.success = "Characteristic added. Thanks for your contribution!"
            else:
                request.flash.error = "Adding characteristic failed: %s" % status
            return HttpResponseRedirect(reverse('parts.views.detail', args=[p.company.slug, p.slug]))

    if 'xref_button' in request.POST:
        xrefform = XrefForm(request.POST)
        if xrefform.is_valid:
            status = addxref(request, p.pk)
            if status is True:
                request.flash.success = "Cross reference added. Thanks for your contribution!"
            else:
                request.flash.error = "Adding cross reference failed: %s" % status
            return HttpResponseRedirect(reverse('parts.views.detail', args=[p.company.slug, p.slug]))
    
    if 'image_button' in request.POST:
        imageuploadform = ImageUploadForm(request.POST, request.FILES)
        if imageuploadform.is_valid:
            status = uploadimage(request, p.pk)
            if status is True:
                request.flash.success = "Image upload success. Thanks for your contribution!"
            else:
                request.flash.error = "Image upload failed: %s" % status
            return HttpResponseRedirect(reverse('parts.views.detail', args=[p.company.slug, p.slug]))

    return render_to_response('parts/detail.html', 
                              {'part': p, 
                               'xrefs': xrefs,
                               'attributes': sorted(p.attributes.iteritems()),
                               'reverse_xrefs': reverse_xrefs,
                               'buylinks': buylinks,
                               'metadata_form': metaform, 
                               'xref_form' : xrefform,
                               'imageuploadform' : imageuploadform,
                               'buylinkform' : buylinkform,
                              },
                              context_instance=RequestContext(request))

def addmeta(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    metaform = MetadataForm(request.POST)
    if metaform.is_valid():
        key = metaform.cleaned_data['key'].strip().upper()
        value = metaform.cleaned_data['value'].strip().upper()
        status = p.save_attributes(key, value)

        if status == True:
            return True
        else:
            return 'Characteristic exists'

def addbuylink(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    buylinkform = BuyLinkForm(request.POST)
    if buylinkform.is_valid():
        url = buylinkform.cleaned_data['url']
        company = buylinkform.cleaned_data['company'].strip().upper()
        price = buylinkform.cleaned_data['price']
        c, _created = Company.objects.get_or_create(name=company)
        buylink = BuyLink(part=p, company=c, price=price, url=url)
        try:
            buylink.save()
            return True
        except IntegrityError:
            return 'Link already exists'


def addpart(request, part_number, company, desc):
    c, _created = Company.objects.get_or_create(name=company)
    newpart, _created = Part.objects.get_or_create(number=part_number, company=c)
    if _created == True:
        newpart.user = request.user
        newpart.description = desc
        newpart.hits = 0
        newpart.save()
    return newpart

def addpartform(request):
    if request.method == 'POST':
        partform = XrefForm(request.POST)
        if partform.is_valid():
            part_number = partform.cleaned_data['part'].upper()
            desc = partform.cleaned_data['desc'].upper()
            company = partform.cleaned_data['company'].upper()
            newpart = addpart(request, part_number, company, desc)
            return HttpResponseRedirect(newpart.get_absolute_url())
    else:
        partform = XrefForm()
    return render_to_response('parts/add.html',
                              {'partform': partform,},
                              context_instance=RequestContext(request))

def addxref(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    xrefform = XrefForm(request.POST)
    print 'adding xref' 
    if xrefform.is_valid():
        part_number = xrefform.cleaned_data['part'].upper()
        company = xrefform.cleaned_data['company'].upper()
        copy_attrs = xrefform.cleaned_data['copy_attrs']
        """Check if the company exists and create it if it does not"""
        c, _created = Company.objects.get_or_create(name=company)
        """Check if the cross referenced part exists and create it if it does not"""
        newpart, _created = Part.objects.get_or_create(number=part_number, company=c)
        if _created == True:
            newpart.user = request.user
            newpart.description = p.description
            newpart.hits = 0
            if copy_attrs == True:
                newpart.attributes = p.attributes
            newpart.save()

        xr1, _created = Xref.objects.get_or_create(part=p, xrefpart=newpart)
        if _created == True:
            xr1.user = request.user
            xr1.save()
            return True
        else:
            return 'Cross Reference already exists'
            
def uploadimage(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    if request.FILES.get('file', False):
        f = request.FILES['file']
    
        """Handle the file upload"""
        new_filename = "%s_%s" % (str(part_id), f.name)
        image = PartImage()
        image.user = request.user
        image.image.save(new_filename, f)
        image.save()
        p.images.add(image)
        p.save()

            
    



