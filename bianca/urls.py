from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^login/$', 'delivery.views.user_login'),
     url(r'^$', 'delivery.views.index'),
     url(r'^cadastro/$', 'delivery.views.user_register'),
     url(r'^nova_conta/(?P<activation_key>[a-zA-Z0-9_.-]+)/$', 'delivery.views.user_activation'),
     url(r'^passo1/', 'delivery.views.passo1'),
     url(r'^logout/', 'delivery.views.logout_view'),
     url(r'^recupera_senha/$', 'delivery.views.password_reset'),
     url(r'^recupera_senha/sucesso/$', 'delivery.views.password_reset_done'),
     url(r'^nova_senha/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'delivery.views.password_reset_confirm'),
     url(r'^nova_senha/sucesso/$', 'delivery.views.password_reset_complete'),
     #url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'index.html'}),
     #url(r'^bianca/', include('bianca.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('django.contrib.auth.urls')),
)
