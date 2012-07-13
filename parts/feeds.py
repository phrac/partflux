from django.contrib.syndication.views import Feed
from parts.models import Part

class LatestPartsFeed(Feed):
    title = "Part Engine Newest Parts"
    link = "/parts/"
    description = "Fresh parts added to the Part Engine Database"

    def items(self):
        return Part.objects.order_by('-created_at')[:25]

    def item_title(self, item):
        return "%s by %s" % (item.number, item.company.name)

    def item_description(self, item):
        return item.description                     