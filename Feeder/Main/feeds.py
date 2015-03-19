from django.contrib.syndication.views import Feed
from Main.models import SomeData
from django.utils.feedgenerator import Atom1Feed

class RssSomeData(Feed):
    title = "Some data"
    link = "/feeder/"
    description = "blah blah blah"

    def items(self):
        return SomeData.objects.all().order_by('-pk')[:2]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.link

    def item_description(self, item):
        return item.description


class AtomSomeData(RssSomeData):
    feed_type = Atom1Feed
    subtitle = RssSomeData.description