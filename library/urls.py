from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login,logout
from django.contrib import admin
from register import register
from library.views import library,search,book_info, borrow, return_book, query
import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'library.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^library/$', library),
    (r'^$', library),
    (r'^accounts/login/$',  login,{'template_name': 'login.html'}),
    (r'^accounts/logout/$', logout),
    (r'^accounts/register/$', register),
    (r'^search/$', search),
    (r'^book_info/$', book_info),
    (r'^borrow/$', borrow),
    (r'^return_book/$', return_book),
    (r'^query/$', query),
)

urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        })
)

urlpatterns += staticfiles_urlpatterns()
