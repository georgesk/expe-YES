from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^makeResa$', views.makeResa, name='makeResa'),
    url(r'^reservationsByDate$', views.reservationsByDate, name='reservationsByDate'),
]
