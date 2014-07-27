from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('inventory.api_urls')),
    url(r'^', include('inventory.urls', namespace="inventory")),
)
