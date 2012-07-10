from django.contrib.sitemaps import Sitemap
from django.core.paginator import Paginator
from parts.models import Part

class PartSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    limit = 5000

    def items(self):
        return Part.objects.all().order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at
