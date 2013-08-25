from amazon.api import AmazonAPI
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify

from parts.models import Part

class Distributor(models.Model):
    name = models.CharField(max_length=64, unique=True)
    affiliate_identifier = models.CharField(max_length=64, unique=True)
    slug = models.CharField(max_length=72, blank=True, null=True)
    description = models.TextField(null=True)
    url = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    email = models.EmailField(max_length=32, null=True, blank=True)
    fax = models.CharField(max_length=16, null=True, blank=True)
    country = models.CharField(max_length=24, null=True, blank=True)
    affiliate_url = models.URLField()

    class Meta:
        ordering = ('name',)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:72]
        super(Distributor, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('distributors.views.detail', [self.id, str(self.slug)])

class DistributorSKU(models.Model):
    sku = models.CharField(max_length=32)
    distributor = models.ForeignKey(Distributor)
    part = models.ForeignKey(Part, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=6, max_length=16,
                                null=True)
    url = models.URLField(max_length=256)
    affiliate_url = models.URLField(max_length=512, null=True)
    impression_url = models.URLField(max_length=512, null=True)
    updated = models.DateTimeField(auto_now=True)
    xpath = models.CharField(max_length=1024, null=True)

    class Meta:
        unique_together = ('sku', 'distributor',)

    def __unicode__(self):
        return "%s - %s" % (self.distributor, self.sku)

    def update_price(self):
        # check if this is an Amazon product
        if self.distributor.name == 'Amazon':
            amazon = AmazonAPI(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_ASSOCIATE_TAG)
            try:
                product = amazon.lookup(ItemId=self.part.asin)
                price = product.price_and_currency
                return price[0]
            except:
                pass
        else:
            import urllib2
            from lxml import etree
            import microdata
            import urllib

            items = microdata.get_items(urllib.urlopen(self.url))
            for i in items:
                if i.offers:
                    return "%s (md)".replace("$", "") % i.offers.price.strip().replace("$", "")
            html = urllib2.urlopen(self.url).read()
            tree = etree.HTML(html)
            price = tree.xpath("%s/text()[1]" % self.xpath)
            try:
                return "%s (xp)" % price[0].replace("$", "")
            except:
                return "N/A"

    @models.permalink
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('distributors.click.track_click', args=[str(self.id)])


class SKUHistoricalPrice(models.Model):
    part = models.ForeignKey(Part)
    sku = models.ForeignKey(DistributorSKU)
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(max_length=16)
    price_UOM = models.CharField(max_length=9)




