from django.urls import path
from . import views

urlpatterns = [
    path('', views.site, name='home'),
    path('sites/', views.site, name='sites'),
    path('sponsors/', views.sponsor, name='sponsors'),
    path('data/', views.site_data, name='data'),
    path('getsite/', views.get_site, name='get_site'),
    path('getsponsor/', views.get_sponsor, name='get_sponsor'),
    path('getgeo/', views.get_geo, name='get_geo'),
    path('sitedetails/<int:siteid>/', views.site_details, name='site_details'),
    path('sponsordetails/<int:ceid>/', views.sponsor_details, name='sponsor_details'),
    path('points/', views.points, name='points'),
]
