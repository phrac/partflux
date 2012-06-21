from django.contrib.sitemaps import Sitemap
from django.core.paginator import Paginator
from parts.models import Part

class PartSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Part.objects.all()[:50000]

    def lastmod(self, obj):
        return obj.updated_at
