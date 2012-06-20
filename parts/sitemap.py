from django.contrib.sitemaps import Sitemap
from parts.models import Part

class PartSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Part.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
