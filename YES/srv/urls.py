from django.conf.urls import url

from . import views

from django.views.i18n import javascript_catalog
    
js_info_dict = {
    'packages': ('srv',),
}

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^login$', views.login, name='login'),
    url(r'^makeResa$', views.makeResa, name='makeResa'),
    url(r'^reservationsByDate$', views.reservationsByDate, name='reservationsByDate'),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),
]
