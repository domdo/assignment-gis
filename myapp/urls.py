from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^first10$', views.get_first10_railstations, name='first10'),
    url(r'^firstLine$', views.get_railway_w_station, name='firstLine'),
    url(r'^nearestStations', views.get_nearest_stations, name='nearestStations'),
    url(r'^station&routes', views.get_station_w_routes, name='station&routes'),
    url(r'^route', views.get_route, name='route'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)