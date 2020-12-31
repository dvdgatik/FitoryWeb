"""Fitory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from FitApp import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'estado', views.EstadoViewSet)
router.register(r'ciudad', views.CiudadViewSet)
router.register(r'servicio', views.ServicioViewSet)
router.register(r'actividad', views.ActividadViewSet)
router.register(r'club', views.ClubViewSet)
router.register(r'servicioClub', views.ServicioClubViewSet)
router.register(r'actividadClub', views.ActividadClubViewSet)
router.register(r'actividadHorario', views.ActividadHorarioViewSet)
router.register(r'sucursal', views.SucursalViewSet)
router.register(r'horario', views.HorarioViewSet)
router.register(r'registroHorario', views.RegistroHorarioViewSet)
router.register(r'foto', views.FotoViewSet)
router.register(r'evaluacionSucursal', views.EvaluacionSucursalViewSet)
router.register(r'cliente', views.ClienteViewSet)
router.register(r'evaluacionCliente', views.EvaluacionClienteViewSet)
router.register(r'favorito', views.FavoritoViewSet)
router.register(r'sesion', views.SesionViewSet)
router.register(r'subscripcion', views.SubscripcionViewSet)
router.register(r'visita', views.VisitaViewSet)
router.register(r'pagosSucursal', views.PagoSucursalViewSet)
router.register(r'subscripcionFree', views.SubscripcionFreeViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('FitApp.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
