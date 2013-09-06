from django.http import HttpResponseRedirect

from distributors.models import DistributorSKU, SKUClick

def track_click(request, sku_id):
    sku = DistributorSKU.objects.get(id=sku_id)
    ip = request.META.get('REMOTE_ADDR')
    path = request.get_full_path()
    referrer = request.META.get('HTTP_REFERER')
    user_agent = request.META.get('HTTP_USER_AGENT')
    click = SKUClick(sku=sku, ip=ip, path=path, referrer=referrer, user_agent=user_agent)
    click.save()
    return HttpResponseRedirect(sku.affiliate_url)
