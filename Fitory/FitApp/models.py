# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
import os
from image_cropping import ImageRatioField,ImageCropField,ImageCropWidget

# Create your models here.

class Estado(models.Model):
	nombre = models.CharField(max_length=100,default="...")
	def __unicode__(self):
		return self.nombre

class Ciudad(models.Model):
	nombre = models.CharField(max_length=100,default="...")
	estado = models.ForeignKey(Estado,default=None,blank=True,null=True)
	def __unicode__(self):
		return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=100,default="...")
    icono = models.ImageField(upload_to='servicios/',default='default/servicio.png')
    def __unicode__(self):
        return self.nombre

class Actividad(models.Model):
    nombre = models.CharField(max_length=100,default="...")
    icono = models.ImageField(upload_to='actividades/',default='default/actividad.jpg')
    def __unicode__(self):
        return self.nombre

class Club(models.Model):
    user = models.OneToOneField(User,default=None)
    nombre = models.CharField(max_length=100,default="...")
    fechaIncorporacion = models.DateField('Fecha',auto_now_add=True)
    RFC = models.CharField(max_length=100,default="...")
    banco = models.CharField(max_length=100,default="...")
    tarjetahabiente = models.CharField(max_length=100,default="...")
    numCuenta = models.CharField(max_length=100,default="...")
    paginaWeb = models.CharField(max_length=100,default="...")
    facebook = models.CharField(max_length=100,default="...")
    instagram = models.CharField(max_length=100,default="...")
    twitter = models.CharField(max_length=100,default="...")
    evaluacionPromedio = models.DecimalField(max_digits=9,decimal_places=2,default=0.0)
    activado = models.BooleanField(default=False)
    codigoClub = models.CharField(max_length=100,default="...")
    codigoRepresentante = models.CharField(max_length=100,default="...")
    direccion = models.CharField(max_length=100,default="...")
    telefono = models.CharField(max_length=100,default="...")
    correo = models.CharField(max_length=100,default="...")
    foto = models.ImageField(upload_to='usuarios/',default='default/club.png')
    fotocrop = ImageRatioField('foto', '200x200')
    Legal = models.BooleanField(default=False)
    fechaLegal = models.DateField('Fecha acepto terminos',default=None,blank=True,null=True)
    cropURL = models.CharField(max_length=200,default=None,blank=True,null=True)
    def __unicode__(self):
        return self.nombre

class Sucursal(models.Model):
    club = models.ForeignKey(Club)
    nombre = models.CharField(max_length=100,default="...")
    descripcion = models.TextField(max_length=1000,blank=True,null=True)
    correo = models.CharField(max_length=100,default="...")
    telefono = models.CharField(max_length=100,default="...")
    estado = models.ForeignKey(Estado)
    ciudad = models.ForeignKey(Ciudad)
    municipio = models.CharField(max_length=100,default="...")
    calle = models.CharField(max_length=100,default="...")
    numExt = models.CharField(max_length=100,default=None,blank=True,null=True)
    numInt = models.CharField(max_length=100,default=None,blank=True,null=True)
    colonia = models.CharField(max_length=100,default="...")
    cp = models.CharField(max_length=100,default="...")
    latitud = models.CharField(max_length=100,default="...")
    longitud = models.CharField(max_length=100,default="...")
    calificacion = models.DecimalField(max_digits=9,decimal_places=2,default=0.0)
    ibeacon = models.CharField(max_length=100,default=None,blank=True,null=True)
    maximo = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    mensualidad = models.DecimalField(max_digits=9,decimal_places=2,default=0.0)
    dia = models.DecimalField(max_digits=9,decimal_places=2,default=0.0)
    porcentajeCliente = models.DecimalField(max_digits=9,decimal_places=2,default=0.0)
    porcentajeUser = models.DecimalField(max_digits=9,decimal_places=2,default=0.0)
    saldo = models.DecimalField(max_digits=9,decimal_places=2,default=0.0)
    activa = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='logos/',default='default/logo.jpg')
    logocrop = ImageRatioField('logo', '200x200')
    cropURL = models.CharField(max_length=200,default=None,blank=True,null=True)
    tips = models.TextField(max_length=1000,blank=True,null=True)
    diasPruebas = models.IntegerField('Dias de pruebas',default=0)
    def __unicode__(self):
        return self.nombre

class Usuario(models.Model):
    user = models.OneToOneField(User,default=None)
    sucursal = models.ForeignKey(Sucursal)
    nombre = models.CharField(max_length=100,default="...")
    activo = models.BooleanField(default=False)
    Legal = models.BooleanField(default=False)
    fechaLegal = models.DateField('Fecha acepto terminos',default=None,blank=True,null=True)
    def __unicode__(self):
        return self.nombre

class Horario(models.Model):
    sucursal = models.ForeignKey(Sucursal)
    lunes = models.BooleanField(default=False)
    martes = models.BooleanField(default=False)
    miercoles = models.BooleanField(default=False)
    jueves = models.BooleanField(default=False)
    viernes = models.BooleanField(default=False)
    sabado = models.BooleanField(default=False)
    domingo = models.BooleanField(default=False)
    numDias = models.IntegerField(default=0)
    tipo = models.CharField(max_length=100,default=None,blank=True,null=True)

class RegistroHorario(models.Model):
    sucursal = models.ForeignKey(Sucursal)
    dia = models.CharField(max_length=100,default=None,blank=True,null=True)
    apertura = models.TimeField(blank=True,null=True)
    cierre = models.TimeField(blank=True,null=True)

class ServicioClub(models.Model):
    sucursal = models.ForeignKey(Sucursal,default=None,blank=True,null=True)
    servicio = models.ForeignKey(Servicio)
    def __unicode__(self):
        return self.sucursal.club.nombre + ' Sucursal: '+ self.sucursal.nombre + ': '+ self.servicio.nombre

class ActividadClub(models.Model):
    sucursal = models.ForeignKey(Sucursal,default=None,blank=True,null=True)
    actividad = models.ForeignKey(Actividad)
    def __unicode__(self):
        return self.sucursal.club.nombre + ' Sucursal: '+ self.sucursal.nombre + ': '+ self.actividad.nombre

class ActividadHorario(models.Model):
    actividadClub = models.ForeignKey(ActividadClub)
    horaInicio = models.TimeField(default=None,blank=True,null=True)
    horaFin = models.TimeField(default=None,blank=True,null=True)
    lunes = models.BooleanField(default=False)
    martes = models.BooleanField(default=False)
    miercoles = models.BooleanField(default=False)
    jueves = models.BooleanField(default=False)
    viernes = models.BooleanField(default=False)
    sabado = models.BooleanField(default=False)
    domingo = models.BooleanField(default=False)
    
class Foto(models.Model):
    sucursal = models.ForeignKey(Sucursal)
    archivo = models.ImageField(upload_to='fotos/',default='default/foto.png')

class Cliente(models.Model):
    user = models.OneToOneField(User)
    nombre = models.CharField(max_length=100,default="...")
    apellido = models.CharField(max_length=100,default="...")
    telefono = models.CharField(max_length=100,default="...")
    hombre = models.BooleanField(default=False)
    mujer = models.BooleanField(default=False)
    fechaIngreso = models.DateField('Fecha',auto_now_add=True)
    salud = models.BooleanField(default=False)
    convivir = models.BooleanField(default=False)
    vermeBien = models.BooleanField(default=False)
    diversion = models.BooleanField(default=False)
    estado = models.ForeignKey(Estado,default=None,blank=True,null=True)
    ciudad = models.ForeignKey(Ciudad,default=None,blank=True,null=True)
    ubicacion = models.BooleanField(default=False)
    bluetooth = models.BooleanField(default=False)
    idFacebook = models.CharField(max_length=100,default="...")
    idGoogle = models.CharField(max_length=100,default=None,blank=True,null=True)
    idCustomer = models.CharField(max_length=100,default=None,blank=True,null=True)
    playerID = models.CharField(max_length=900,default=None,blank=True,null=True)
    foto = models.ImageField(upload_to='clientes/',default='default/perfil.png')
    fotocrop = ImageRatioField('foto', '200x200')
    cropURL = models.CharField(max_length=200,default=None,blank=True,null=True)
    def __unicode__(self):
        return self.nombre

class EvaluacionCliente(models.Model):
    cliente = models.ForeignKey(Cliente)
    puntaje = models.IntegerField(default=0)

class Favorito(models.Model):
    cliente = models.ForeignKey(Cliente,default=None,blank=True,null=True)
    sucursal = models.ForeignKey(Sucursal,default=None,blank=True,null=True)

class EvaluacionSucursal(models.Model):
    cliente = models.ForeignKey(Cliente,default=None,blank=True,null=True)
    sucursal = models.ForeignKey(Sucursal,default=None,blank=True,null=True)
    puntaje = models.IntegerField(default=0)

class Sesion(models.Model):
    cliente = models.ForeignKey(Cliente)
    sucursal = models.ForeignKey(Sucursal)
    total = models.DecimalField(max_digits=9,decimal_places=2,default=0.0)
    sesiones = models.IntegerField(default=0)
    sesionesRestantes = models.IntegerField(default=0)
    caducidad = models.DateField('Fecha',default=timezone.now)
    activo = models.BooleanField(default=False)

class Subscripcion(models.Model):
    cliente = models.ForeignKey(Cliente)
    sucursal = models.ForeignKey(Sucursal)
    totalCobrar = models.DecimalField(max_digits=9,decimal_places=2,default=0.0)
    totalGym = models.DecimalField(max_digits=9,decimal_places=2,default=0.0)
    fechaSubscripcion = models.DateField('Fecha Subscripcion',default=timezone.now)
    fechaRenovacion = models.DateField('Fecha Renovacion',default=timezone.now)
    direccion = models.CharField(max_length=100,default=None,blank=True,null=True)
    activa = models.BooleanField(default=False)

class Visita(models.Model):
    cliente = models.ForeignKey(Cliente)
    sucursal = models.ForeignKey(Sucursal)
    fecha = models.DateField('Fecha',auto_now_add=True)
    hora = models.TimeField('Hora',auto_now_add=True)

class IncidenciaContrasena(models.Model):
	correo = models.EmailField(default='example@example.com')
	fecha = models.DateTimeField(default=timezone.now)
	estatus = models.IntegerField(default=0)
	token = models.CharField(max_length=32)

class PagoSucursal(models.Model):
    sucursal = models.ForeignKey(Sucursal)
    pagar = models.DecimalField(max_digits=9,decimal_places=2,default=0.0)
    numRastreo = models.CharField(max_length=100,default=None,blank=True,null=True)
    fecha = models.DateField('Fecha Pago',default=timezone.now)

class SubscripcionFree(models.Model):
    cliente = models.ForeignKey(Cliente)
    sucursal = models.ForeignKey(Sucursal)
    fechaSubscripcion = models.DateField('Fecha Subscripcion',default=timezone.now)
    fechaFin = models.DateField('Fecha Fin',default=timezone.now)
    direccion = models.CharField(max_length=100,default=None,blank=True,null=True)
    sesiones = models.IntegerField(default=0)
    sesionesRestantes = models.IntegerField(default=0)
    activa = models.BooleanField(default=False)