from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from apps.prisoners.models import *


from tastypie.api import Api
from apps.prisoners.api import AddressResource
from apps.prisoners.api import BlockResource

v1_api = Api(api_name='v1')
v1_api.register(AddressResource())
v1_api.register(BlockResource())

admin.autodiscover()

urlpatterns = patterns('',
    # Simple login for securing site on Heroku
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),

    # Admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', admin.site.urls),

    #api!!!
    (r'^api/', include(v1_api.urls)),
    
    # Project URLs go here
	url(r'^map/', 'apps.prisoners.views.map', name = 'map'),
    url(r'^bookings/', 'apps.prisoners.views.bookings', name = 'bookings'),
)

urlpatterns += staticfiles_urlpatterns()
