def get_current_path(request):
    return {
        'current_path': request.get_full_path()
    }

def get_current_domain(request):
    from django.contrib.sites.models import Site
    return {
        'current_domain': 'http://%s' % Site.objects.get_current().domain
    }

