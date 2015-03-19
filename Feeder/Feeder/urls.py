from django.conf.urls import patterns
from Main.feeds import *
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
    #url(r'^admin/', include(admin.site.urls)),
    (r'^rssdata/', RssSomeData()),
    (r'^atomdata/', AtomSomeData()),
    (r'^jsondata/', 'Main.views.someDataListJson'),
    (r'^xmldata/', 'Main.views.someDataListXml'),
)

urlpatterns = format_suffix_patterns(urlpatterns)