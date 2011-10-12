from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('flickrdatechanger.views',
    url(r'^$', 'home', name='home'),
    url(r'^flickr_auth/$', 'flickr_authenticate', name='flickr_authenticate'),
)
