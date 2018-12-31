from django.urls import path
from . import views

urlpatterns = [
    path('', views.sha),
    path('SHA', views.sha),
    path('sha', views.sha),
    path('ORO', views.oro),
    path('oro', views.oro),
    path('CLE', views.cle),
    path('cle', views.cle),
    path('mil', views.mil),
    path('MIL', views.mil),
    path('nml', views.nml),
    path('NML', views.nml),
    path('FOL', views.fol),
    path('fol', views.fol)
]
