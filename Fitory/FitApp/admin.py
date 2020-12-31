# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Estado, Ciudad, Servicio, Actividad, Club, ServicioClub, ActividadClub, ActividadHorario, Sucursal, Foto, EvaluacionSucursal, Cliente, EvaluacionCliente, Favorito, Horario, RegistroHorario, Sesion, Subscripcion, IncidenciaContrasena, PagoSucursal, Usuario, Visita, SubscripcionFree
from image_cropping import ImageCroppingMixin

# Register your models here.

class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')
    list_filter = ['id','nombre']
    search_fields = ['id','nombre']

admin.site.register(Estado,EstadoAdmin)

class CiudadAdmin(admin.ModelAdmin):
    list_display = ('id','estado','nombre')
    list_filter = ['id','estado','nombre']
    search_fields = ['id','estado','nombre']

admin.site.register(Ciudad,CiudadAdmin)

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','icono')
    list_filter = ['id','nombre','icono']
    search_fields = ['id','nombre','icono']

admin.site.register(Servicio,ServicioAdmin)

class ActividadAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','icono')
    list_filter = ['id','nombre','icono']
    search_fields = ['id','nombre','icono']

admin.site.register(Actividad,ActividadAdmin)

class ClubAdmin(ImageCroppingMixin,admin.ModelAdmin):
    list_display = ('id','user','nombre','fechaIncorporacion','activado')
    list_filter = ['id','user','nombre','fechaIncorporacion','activado']
    search_fields = ['id','user','nombre','fechaIncorporacion','activado']

admin.site.register(Club,ClubAdmin)

class ServicioClubAdmin(admin.ModelAdmin):
    list_display = ('id','sucursal','servicio')
    list_filter = ['id','sucursal','servicio']
    search_fields = ['id','sucursal','servicio']

admin.site.register(ServicioClub,ServicioClubAdmin)

class ActividadClubAdmin(admin.ModelAdmin):
    list_display = ('id','sucursal','actividad')
    list_filter = ['id','sucursal','actividad']
    search_fields = ['id','sucursal','actividad']

admin.site.register(ActividadClub,ActividadClubAdmin)

class ActividadHorarioAdmin(admin.ModelAdmin):
    list_display = ('id','actividadClub','horaInicio','horaFin','lunes','martes','miercoles','jueves','viernes','sabado','domingo')
    list_filter = ['id','actividadClub','horaInicio','horaFin','lunes','martes','miercoles','jueves','viernes','sabado','domingo']
    search_fields = ['id','actividadClub','horaInicio','horaFin','lunes','martes','miercoles','jueves','viernes','sabado','domingo']

admin.site.register(ActividadHorario,ActividadHorarioAdmin)

class SucursalAdmin(ImageCroppingMixin,admin.ModelAdmin):
    list_display = ('id','club','nombre','activa')
    list_filter = ['id','club','nombre','activa']
    search_fields = ['id','club','nombre','activa']

admin.site.register(Sucursal,SucursalAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id','user','sucursal','nombre','activo')
    list_filter = ['id','user','sucursal','nombre','activo']
    search_fields = ['id','user','sucursal','nombre','activo']

admin.site.register(Usuario,UsuarioAdmin)

class HorarioAdmin(admin.ModelAdmin):
    list_display = ('id','sucursal','lunes','martes','miercoles','jueves','viernes','sabado','domingo','numDias','tipo')
    list_filter = ['id','sucursal','lunes','martes','miercoles','jueves','viernes','sabado','domingo','numDias','tipo']
    search_fields = ['id','sucursal','lunes','martes','miercoles','jueves','viernes','sabado','domingo','numDias','tipo']

admin.site.register(Horario,HorarioAdmin)

class RegistroHorarioAdmin(admin.ModelAdmin):
    list_display = ('id','sucursal','dia','apertura','cierre')
    list_filter = ['id','sucursal','dia','apertura','cierre']
    search_fields = ['id','sucursal','dia','apertura','cierre']

admin.site.register(RegistroHorario,RegistroHorarioAdmin)

class FotoAdmin(admin.ModelAdmin):
    list_display = ('id','sucursal','archivo')
    list_filter = ['id','sucursal','archivo']
    search_fields = ['id','sucursal','archivo']

admin.site.register(Foto,FotoAdmin)

class ClienteAdmin(ImageCroppingMixin,admin.ModelAdmin):
    list_display = ('id','user','nombre','hombre','mujer','idFacebook','idGoogle','idCustomer','playerID','estado','ciudad')
    list_filter = ['id','user','nombre','hombre','mujer','idFacebook','idGoogle','idCustomer','playerID']
    search_fields = ['id','user','nombre','hombre','mujer','idFacebook','idGoogle','idCustomer','playerID']

admin.site.register(Cliente,ClienteAdmin)

class EvaluacionClienteAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','puntaje')
    list_filter = ['id','cliente','puntaje']
    search_fields = ['id','cliente','puntaje']

admin.site.register(EvaluacionCliente,EvaluacionClienteAdmin)

class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','sucursal')
    list_filter = ['id','cliente','sucursal']
    search_fields = ['id','cliente','sucursal']

admin.site.register(Favorito,FavoritoAdmin)

class EvaluacionSucursalAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','sucursal','puntaje')
    list_filter = ['id','cliente','sucursal','puntaje']
    search_fields = ['id','cliente','sucursal','puntaje']

admin.site.register(EvaluacionSucursal,EvaluacionSucursalAdmin)

class SesionAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','sucursal','activo')
    list_filter = ['id','cliente','sucursal','activo']
    search_fields = ['id','cliente','sucursal','activo']

admin.site.register(Sesion,SesionAdmin)

class SubscripcionAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','sucursal','activa','fechaSubscripcion','fechaRenovacion')
    list_filter = ['id','cliente','sucursal','activa','fechaSubscripcion','fechaRenovacion']
    search_fields = ['id','cliente','sucursal','activa','fechaSubscripcion','fechaRenovacion']

admin.site.register(Subscripcion,SubscripcionAdmin)

class IncidenciaContrasenaAdmin(admin.ModelAdmin):
    list_display = ('id','correo','token','estatus')
    list_filter = ['id','correo','token','estatus']
    search_fields = ['id','correo','token','estatus']

admin.site.register(IncidenciaContrasena,IncidenciaContrasenaAdmin)

class PagoSucursalAdmin(admin.ModelAdmin):
    list_display = ('id','sucursal','pagar','numRastreo','fecha')
    list_filter = ['id','sucursal','pagar','numRastreo','fecha']
    search_fields = ['id','sucursal','pagar','numRastreo','fecha']

admin.site.register(PagoSucursal,PagoSucursalAdmin)

class VisitaAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','sucursal','fecha','hora')
    list_filter = ['id','cliente','sucursal','fecha','hora']
    search_fields = ['id','cliente','sucursal','fecha','hora']

admin.site.register(Visita,VisitaAdmin)

class SubscripcionFreeAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','sucursal','activa')
    list_filter = ['id','cliente','sucursal','activa']
    search_fields = ['id','cliente','sucursal','activa']

admin.site.register(SubscripcionFree,SubscripcionFreeAdmin)