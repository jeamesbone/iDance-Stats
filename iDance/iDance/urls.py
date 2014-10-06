from django.conf.urls import patterns, include, url
from django.contrib import admin

from iDance import views 

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iDance.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^import/', views.importData),
    url(r'^scores/', views.scores),
    url(r'^playerScores/', views.playerScores),
    url(r'^systemHighs/', views.systemHighs),
    url(r'^match/', views.match),
)
