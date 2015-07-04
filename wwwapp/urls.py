from django.conf.urls import patterns, include, url
from django.contrib import admin
from pkw import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wwwapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	 url(r'^$', 'pkw.views.home', name='home'),
	 url(r'^req/votes/(?P<id>[0-9]*)/$', 'pkw.views.getVotesData'),
	 url(r'^req/save/(?P<id>[0-9]*)/$', 'pkw.views.saveVotes'),
	 url(r'^req/$', 'pkw.views.getVoivs'),
	 url(r'^req/(?P<voiv>[\w\-]*)/$', 'pkw.views.getDistricts'),
	 url(r'^req/(?P<voiv>[\w\-]*)/(?P<dist>[\w \-,\.]*)/$', 'pkw.views.getCommCounty'),
	 url(r'^req/(?P<voiv>[\w\-]*)/(?P<dist>[\w \-,\.]*)/(?P<county>[\w \-,\.]*)/$', 'pkw.views.getComm'),
)
