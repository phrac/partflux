from django.http import HttpResponseRedirect

from distributors.models import DistributorSKU

def track_click(request, sku_id):
    sku = DistributorSKU.objects.get(id=sku_id)
    return HttpResponseRedirect(sku.affiliate_url)
