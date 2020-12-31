from __future__ import absolute_import
from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from celery import task
from .models import Estado, Ciudad, Servicio, Actividad, Club, ServicioClub, ActividadClub, ActividadHorario, Sucursal, Foto, EvaluacionSucursal, Cliente, EvaluacionCliente, Favorito, Horario, RegistroHorario, Sesion, Subscripcion, Visita, PagoSucursal, IncidenciaContrasena
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import json
import requests
from celery import Celery
from celery.schedules import crontab
import datetime
from datetime import date, timedelta, datetime
import pytz
import decimal
from decimal import Decimal
Dec = Decimal
from dateutil.relativedelta import relativedelta
import conekta
conekta.api_key = 'key_z1MPjh96QF3wgdMeSLNLWA'
conekta.locale = 'es'

@periodic_task(run_every=(crontab(minute=1,hour=0)), name="limpiarIncidencias", ignore_result=True)
def limpiarIncidencias():
	try:
		incidencias = IncidenciaContrasena.objects.filter(estatus=0)
	except IncidenciaContrasena.DoesNotExist:
		incidencias = False
	if incidencias:
		for i in incidencias:
			i.delete()

@periodic_task(run_every=crontab(minute=0, hour=7), name="actualizarEstatusSesion", ignore_result=True)
def actualizarEstatusSesion():
	today = str(date.today())
	hoy = date.today()
	try:
		sesiones = Sesion.objects.filter(activo=True)
	except Sesion.DoesNotExist:
		sesiones = False
	if sesiones:
		for s in sesiones:
			caducidad = s.caducidad
			if hoy > caducidad:
				s.activo = False
				s.save()

@periodic_task(run_every=(crontab(minute=0,hour=23)), name="ActualizarSaldoSucursal", ignore_result=True)
def ActualizarSaldoSucursal():
	today = str(date.today())
	try:
		sucursales = Sucursal.objects.filter(activa=True)
	except Sucursal.DoesNotExist:
		sucursales = False
	if sucursales:
		for s in sucursales:
			try:
				visitas = Visita.objects.filter(sucursal=s,fecha=today)
			except Visita.DoesNotExist:
				visitas = False
			try:
				subscripcionesHoy = Subscripcion.objects.filter(sucursal=s,fechaSubscripcion=today)
			except Subscripcion.DoesNotExist:
				subscripcionesHoy = False
			numVisitas = len(visitas)
			costoDia = s.dia
			totalVisitas = numVisitas * costoDia
			numSubscripcionesHoy = len(subscripcionesHoy)
			costoMes = s.mensualidad
			totalSubscripcionesHoy = numSubscripcionesHoy * costoMes
			saldoActual = s.saldo
			saldoNuevo1 =  totalVisitas + totalSubscripcionesHoy
			comision = (saldoNuevo1*10)/100
			saldoNuevo2 = saldoNuevo1 - comision
			saldoNuevo3 = saldoActual + saldoNuevo2
			s.saldo = saldoNuevo3
			s.save()

@periodic_task(run_every=(crontab(minute=0,hour=6)), name="RenovarSubscripciones", ignore_result=True)
def RenovarSubscripciones():
	today = str(date.today())
	try:
		subscripciones = Subscripcion.objects.filter(activa=True,fechaRenovacion=today)
	except Subscripcion.DoesNotExist:
		subscripciones = False
	if subscripciones:
		for s in subscripciones:
			cliente = s.cliente
			direccion = s.direccion
			sucursal = s.sucursal
			totalCobrar = Dec(sucursal.mensualidad)
			cincoPorciento = (totalCobrar * 5)/100
			totalCobrar = totalCobrar + cincoPorciento
			hoy = date.today()
			fechaRenovacion = hoy + relativedelta(months=1)
			totalGym = Dec(sucursal.mensualidad) * Dec(0.9)
			totalCentavos = (totalCobrar)*100
			name = 'Renovacion subscripcion mensual.'
			try:
				cargo = conekta.Order.create({
					"currency": "MXN",
					"customer_info": {
						"customer_id": cliente.idCustomer
					},
					"line_items": [{
						"name": name,
						"unit_price": totalCentavos,
						"quantity": 1
					}],
					"charges": [{
						"payment_method": {
							"payment_source_id":direccion,
							"type": "card"
						}
					}]
				})
			except:
				cargo = False
			if cargo:
				s.fechaRenovacion = fechaRenovacion
				s.activa = True
				s.save()
			else:
				s.activa = False
				s.save()