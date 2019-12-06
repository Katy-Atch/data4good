from django.urls import path
from . import views

urlpatterns = [
    path('', views.map, name='home'),
    path('map/', views.map, name='map'),
    path('sponsors/', views.sponsor, name='sponsor'),
    path('update/', views.update, name='update'),
    path('data/', views.site_data, name='data'),
    path('details/<int:siteid>/', views.details, name='details'),
    path('points/', views.points, name='points'),
]
