from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection
from django_restapi.responder import XMLResponder

from bme.web.models import *

themecamp_resource = Collection(
	queryset = theme_camp.objects.all(),
	responder = XMLResponder())     

urlpatterns = patterns('',
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^$', 'bme.web.views.index'),
     (r'^(?P<year_year>\d{4})/$', 'bme.web.views.year_info'),
     (r'^(?P<year_year>\d{4})/themecamps/$', 'bme.web.views.themecamps'),
     (r'^(?P<year_year>\d{4})/themecamp/(?P<theme_camp_name>[a-z-]{0,50})/$', 'bme.web.views.themecampname'),
     (r'^(?P<year_year>\d{4})/themecamp/(?P<theme_camp_id>\d{1,4})/$', 'bme.web.views.themecampid'),
     (r'^(?P<year_year>\d{4})/art_installations/$', 'bme.web.views.art_installations'),
     (r'^(?P<year_year>\d{4})/art_installation/(?P<art_installation_name>[0-9a-z-]{0,255})/$', 'bme.web.views.art_installation_name'),
     (r'^(?P<year_year>\d{4})/art_installation/(?P<art_installation_id>\d{1,4})/$', 'bme.web.views.art_installation_id'),
     (r'^(?P<year_year>\d{4})/(?P<hour>\d{1,2}):(?P<minute>\d{1,2})/(?P<street>[a-z-]{0,50})/$', 'bme.web.views.neighborhood'),
     (r'^geocoder/(?P<year_year>\d{4})/(?P<hour>\d{1,2}):(?P<minute>\d{1,2})/(?P<street>[a-z-]{0,50})/$', 'bme.web.views.geocoder'),
     (r'^xml/themecamp/(.*?)/?$', themecamp_resource),
)
