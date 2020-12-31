# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
import datetime
from django.utils import timezone
from datetime import date, timedelta, datetime
import unicodedata
import os, sys
import json
from django.views.generic import View
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.files.storage import FileSystemStorage
import decimal
from decimal import *
from django.shortcuts import get_list_or_404, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from io import BytesIO
import time
from django.utils.crypto import get_random_string
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from .models import Estado, Ciudad, Servicio, Actividad, Club, ServicioClub, ActividadClub, ActividadHorario, Sucursal, Foto, EvaluacionSucursal, Cliente, EvaluacionCliente, Favorito, Horario, RegistroHorario, Sesion, Subscripcion, Visita, IncidenciaContrasena, PagoSucursal, Usuario, SubscripcionFree
import conekta
conekta.api_key = 'key_z1MPjh96QF3wgdMeSLNLWA'
conekta.locale = 'es'
from .serializers import UserSerializer, UserLoginSerializer, EstadoSerializer, CiudadSerializer, ServicioSerializer, ActividadSerializer, ClubSerializer, ServicioClubSerializer, ActividadClubSerializer, ActividadHorarioSerializer, SucursalSerializer, HorarioSerializer, RegistroHorarioSerializer, FotoSerializer, EvaluacionSucursalSerializer, ClienteSerializer, EvaluacionClienteSerializer, FavoritoSerializer, SesionSerializer, SubscripcionSerializer, VisitaSerializer, CustomerConektaSerializer, BorrarCustomerConektaSerializer, addMetodoPagoSerializer, MetodosPagoSerializer, deleteMetodoPagoSerializer, ActualizarFotoClienteSerializer, CalcularPromedioEvaluacionesSerializer, ConsultaFechaSerializer, SubscripcionMensualSerializer, CancelarSubscripcionMensualSerializer, ActualizarSubscripcionMensualSerializer, CobrarPorSesionSerializer, PerfilSucursalSerializer, DiasDisponiblesSerializer, PagoSucursalSerializer, UsuarioSerializer, RevisarVisitaSerializer, RegistrarVisitaSerializer, RegistrarCelularSerializer, ActivarSubscripcionFreeSerializer, RevisarSubscripcionFreeSerializer, CheckPhoneSerializer, UpdatePhoneSerializer, VerifyPhoneSerializer, SubscripcionFreeSerializer, GetSubscriptionsSerializer
Dec = decimal.Decimal
import requests
import xlsxwriter
from xlsxwriter.utility import xl_range_abs
from .forms import cropFotoClub, cropLogoSucursal, cropFotoCliente
from easy_thumbnails.files import get_thumbnailer

# Create your views here.
def Index(request):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
        return render(request,'FitApp/index.html',{'usuario':usuario})
    else:
        return render(request,'FitApp/index.html')

def VistaQR(request):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
        return render(request,'FitApp/templateqr.html',{'usuario':usuario})
    else:
        return render(request,'FitApp/templateqr.html')

def Actividades(request):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
        return render(request,'FitApp/Actividades.html',{'usuario':usuario})
    else:
        return render(request,'FitApp/Actividades.html',{'usuario':usuario})

def Paquetes(request):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
        return render(request,'FitApp/paquetes.html',{'usuario':usuario})
    else:
        return render(request,'FitApp/paquetes.html')

def Clubes(request):
    try:
        estados = Estado.objects.all()
    except Estado.DoesNotExist:
        estados = False
    try:
        sucursales = Sucursal.objects.all()
    except Sucursal.DoesNotExist:
        sucursales = False
    try:
        ciudad = Ciudad.objects.all()
    except Ciudad.DoesNotExist:
        ciudad = False
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
        return render(request,'FitApp/clubes.html',{'estados':estados,'sucursales':sucursales,'ciudad':ciudad,'usuario':usuario})
    else:
        return render(request,'FitApp/clubes.html',{'estados':estados,'sucursales':sucursales,'ciudad':ciudad})

def BuscadorClub(request):
    if request.method == "POST":
        try:
            estados = Estado.objects.all()
        except Estado.DoesNotExist:
            estados = False
        try:
            ciudad = Ciudad.objects.all()
        except Ciudad.DoesNotExist:
            ciudad = False
        try:
            ciudad_id = request.POST['ciudad']
        except MultiValueDictKeyError:
            ciudad_id = False
        try:
            estado_id = request.POST['estado']
        except MultiValueDictKeyError:
            estado_id = False
        usuario = False
        if ciudad_id and not estado_id:
            try:
                ciudades = Ciudad.objects.get(id=ciudad_id)
            except Ciudad.DoesNotExist:
                ciudades = False
            if ciudades:
                try:
                    sucursales = Sucursal.objects.filter(ciudad=ciudades) 
                except Sucursal.DoesNotExist:
                    sucursales = False
                if request.user.is_authenticated and not request.user.is_staff:
                    user = request.user
                    if user:
                        try:
                            usuario = Cliente.objects.get(user=user)
                        except Cliente.DoesNotExist:
                            usuario = False
                    return render(request,'FitApp/buscadorclub.html',{'sucursales':sucursales,'estados':estados,'ciudad':ciudad,'usuario':usuario})
                else:
                    return render(request,'FitApp/buscadorclub.html',{'sucursales':sucursales,'estados':estados,'ciudad':ciudad})
        if estado_id and not ciudad_id:
            try:
                estado = Estado.objects.get(id=estado_id)
            except Estado.DoesNotExist:
                estado = False
            if estado:
                try:
                    sucursales = Sucursal.objects.filter(estado=estado) 
                except Sucursal.DoesNotExist:
                    sucursales = False
                if request.user.is_authenticated and not request.user.is_staff:
                    user = request.user
                    if user:
                        try:
                            usuario = Cliente.objects.get(user=user)
                        except Cliente.DoesNotExist:
                            usuario = False
                    return render(request,'FitApp/buscadorclub.html',{'sucursales':sucursales,'estados':estados,'ciudad':ciudad,'usuario':usuario})
                else:
                    return render(request,'FitApp/buscadorclub.html',{'sucursales':sucursales,'estados':estados,'ciudad':ciudad})
        if ciudad_id and estado_id:
            try:
                ciudades = Ciudad.objects.get(id=ciudad_id)
            except Ciudad.DoesNotExist:
                ciudades = False
            try:
                estado = Estado.objects.get(id=estado_id)
            except Estado.DoesNotExist:
                estado = False
            if ciudades and estado:
                if ciudades.estado == estado:
                    try:
                        sucursales = Sucursal.objects.filter(estado=estado,ciudad=ciudades) 
                    except Sucursal.DoesNotExist:
                        sucursales = False
                    if request.user.is_authenticated and not request.user.is_staff:
                        user = request.user
                        if user:
                            try:
                                usuario = Cliente.objects.get(user=user)
                            except Cliente.DoesNotExist:
                                usuario = False
                        return render(request,'FitApp/buscadorclub.html',{'sucursales':sucursales,'estados':estados,'ciudad':ciudad,'usuario':usuario})
                    else:
                        return render(request,'FitApp/buscadorclub.html',{'sucursales':sucursales,'estados':estados,'ciudad':ciudad})
        if not ciudad_id and not estado_id:
            try:
                sucursales = Sucursal.objects.all() 
            except Sucursal.DoesNotExist:
                sucursales = False
            if request.user.is_authenticated and not request.user.is_staff:
                user = request.user
                if user:
                    try:
                        usuario = Cliente.objects.get(user=user)
                    except Cliente.DoesNotExist:
                        usuario = False
                return render(request,'FitApp/buscadorclub.html',{'estados':estados,'ciudad':ciudad,'sucursales':sucursales,'usuario':usuario})
            else:
                return render(request,'FitApp/buscadorclub.html',{'estados':estados,'ciudad':ciudad,'sucursales':sucursales})
        else:
            return render(request,'FitApp/buscadorclub.html',{'estados':estados,'ciudad':ciudad})
    else:
        return render(request,'FitApp/buscadorclub.html')

def getCiudadesWeb(request,estado_id):
    if request.is_ajax() and request.method == 'POST':
        estado = Estado.objects.get(id=estado_id)
        cat_ciudades = {}
        try:
            ciudades = Ciudad.objects.filter(estado=estado)
        except Ciudad.DoesNotExist:
            ciudades = False
        if ciudades:
            for c in ciudades:
                cat_ciudades[c.id] = c.nombre
        return HttpResponse(json.dumps(cat_ciudades), content_type="application/json")
    else:
        cat_ciudades = {'None':None}
        return HttpResponse(json.dumps(cat_ciudades), content_type="application/json")

def detalleSucursal(request,sucursal_id):   
    swipe = False 
    try:
        estados = Estado.objects.all()
    except Estado.DoesNotExist:
        estados = False    
    try:
        sucursal = Sucursal.objects.get(id=sucursal_id) 
    except Sucursal.DoesNotExist:
        sucursal = False   
    listaSig = []
    listaAnt = []
    try:
        antsucursal = Sucursal.objects.filter(id__lt=sucursal_id).order_by('-id')[:1]
    except Sucursal.DoesNotExist:
        antsucursal = False
    try:
        sigsucursal = Sucursal.objects.filter(id__gt=sucursal_id).order_by('id')[:1]
    except Sucursal.DoesNotExist:
        sigsucursal = False
    if antsucursal:
        for a in antsucursal:
            listaAnt.append(a.id)
    if sigsucursal:
        for a in sigsucursal:
            listaSig.append(a.id)
    dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
    sucursalRegistrosHorario = []
    sucursalHorario = []
    if sucursal:
        sucursalMensualidadMasPorcentaje = []
        sucursalDiadMasPorcentaje = []
        mensualidad = sucursal.mensualidad
        cincoPorciento = (mensualidad*5)/100
        mensualidadMasCincoPCT = mensualidad + cincoPorciento
        mensualidadMasCincoPCT = round(mensualidadMasCincoPCT,2)
        sucursalMensualidadMasPorcentaje.append((sucursal,mensualidadMasCincoPCT))
        dia = sucursal.dia
        quincePorciento = (dia*15)/100
        diaMasCincoPCT = dia + quincePorciento
        diaMasCincoPCT = round(diaMasCincoPCT,2)
        sucursalDiadMasPorcentaje.append((sucursal,diaMasCincoPCT))
        try:
            fotos = Foto.objects.filter(sucursal=sucursal)
        except Foto.DoesNotExist:
            fotos = False            
        try: 
            horario = Horario.objects.get(sucursal=sucursal)            
        except Horario.DoesNotExist:
            horario = False
        if horario:
            sucursalHorario.append((sucursal,horario))
        else:
            sucursalHorario.append((sucursal,None))
        if horario:
            tipo = horario.tipo
            if dias:
                for d in dias:
                    if tipo == u'Corrido':
                        try:
                            registros = RegistroHorario.objects.get(sucursal=sucursal,dia=d)
                        except RegistroHorario.DoesNotExist:
                            registros = False
                        if registros:
                            sucursalRegistrosHorario.append((sucursal,d,tipo,registros))
                        else:
                            sucursalRegistrosHorario.append((sucursal,d,tipo,None))
                    else:
                        try:
                            registros = RegistroHorario.objects.filter(sucursal=sucursal,dia=d)
                        except RegistroHorario.DoesNotExist:
                            registros = False
                        if registros:
                            sucursalRegistrosHorario.append((sucursal,d,tipo,registros))
                        else:
                            sucursalRegistrosHorario.append((sucursal,d,tipo,None))
        try:
            servicios = ServicioClub.objects.filter(sucursal=sucursal)
        except ServicioClub.DoesNotExist:
            servicios = False
        try: 
            actividades = ActividadClub.objects.filter(sucursal=sucursal)
        except ActividadClub.DoesNotExist:
            actividades = False
        try:
            clubActividadesT = ActividadClub.objects.filter(sucursal=sucursal)
        except ActividadClub.DoesNotExist:
            clubActividadesT = False
        clubActividadHorarios = []
        if clubActividadesT:
            for cAct in clubActividadesT:
                try:
                    horarios = ActividadHorario.objects.filter(actividadClub=cAct)
                except ActividadHorario.DoesNotExist:
                    horarios = False
                numHorarios = 0
                if horarios:
                    numHorarios = len(horarios)
                    clubActividadHorarios.append((cAct,horarios,numHorarios))
                else:
                    clubActividadHorarios.append((cAct,None,numHorarios))
        usuario = False
        if request.user.is_authenticated and not request.user.is_staff:
            user = request.user
            if user:
                try:
                    usuario = Cliente.objects.get(user=user)
                except Cliente.DoesNotExist:
                    usuario = False
                try:
                    favoritos = Favorito.objects.filter(cliente=usuario,sucursal=sucursal)
                except Favorito.DoesNotExist:
                    favoritos = False
            return render(request,'FitApp/clubDetalle.html',{'sucursal':sucursal,'fotos':fotos,'horario':horario,'servicios':servicios,'actividades':actividades,'sucursalRegistrosHorario':sucursalRegistrosHorario,'sucursalHorario':sucursalHorario,'dias':dias,'clubActividadHorarios':clubActividadHorarios,'clubActividadesT':clubActividadesT,'listaAnt':listaAnt,'listaSig':listaSig,'usuario':usuario,'favoritos':favoritos,'sucursalMensualidadMasPorcentaje':sucursalMensualidadMasPorcentaje,'sucursalDiadMasPorcentaje':sucursalDiadMasPorcentaje,'swipe':swipe})
        else:
            return render(request,'FitApp/clubDetalle.html',{'sucursal':sucursal,'fotos':fotos,'horario':horario,'servicios':servicios,'actividades':actividades,'sucursalRegistrosHorario':sucursalRegistrosHorario,'sucursalHorario':sucursalHorario,'dias':dias,'clubActividadHorarios':clubActividadHorarios,'clubActividadesT':clubActividadesT,'listaAnt':listaAnt,'listaSig':listaSig,'sucursalMensualidadMasPorcentaje':sucursalMensualidadMasPorcentaje,'sucursalDiadMasPorcentaje':sucursalDiadMasPorcentaje,'swipe':swipe})
    else:
        return render(request,'FitApp/clubes.html',{'estados':estados})

def getFavoritosAdd(request,sucursal_id,usuario_id):
    sucursal = Sucursal.objects.get(id=sucursal_id)
    usuario = Cliente.objects.get(id=usuario_id)
    nFavoritos = Favorito(sucursal=sucursal,cliente=usuario)
    nFavoritos.save()
    url = '/Clubes/'+str(sucursal.id)+'/'
    return HttpResponseRedirect(url)

def getFavoritosDelete(request,sucursal_id,favoritos_id):
    sucursal = Sucursal.objects.get(id=sucursal_id)
    try:
        favoritos = Favorito.objects.get(id=favoritos_id)
    except Favorito.DoesNotExist:
        favoritos = False
    if favoritos:
        favoritos.delete()
        url = '/Clubes/'+str(sucursal.id)+'/'
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect("/")

def paquetesPagoMensual(request,sucursal_id):
    try:
        sucursal = Sucursal.objects.get(id=sucursal_id) 
    except Sucursal.DoesNotExist:
        sucursal = False   
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False 
            try:
                suscripcionN = Subscripcion.objects.filter(cliente=usuario).order_by('-id')[:1]
            except Subscripcion.DoesNotExist:
                suscripcionN = False
            try:
                secionesN = Sesion.objects.filter(cliente=usuario).order_by('-id')[:1]
            except Sesion.DoesNotExist:
                secionesN = False
            if usuario:
                if not usuario.idCustomer == None:
                    customerID = usuario.idCustomer
                    customer = conekta.Customer.find(customerID)
                    listaMetodos = []
                    metodosPago = customer.payment_sources
                    for m in metodosPago:
                        tarjetas = {'id':m.id, 'last4':m.last4,'brand':m.brand,'exp_month': m.exp_month, 'exp_year':m.exp_year}
                        listaMetodos.append(tarjetas)
                    return render(request,'FitApp/paquetesPago.html',{'sucursal':sucursal,'usuario':usuario,'listaMetodos':listaMetodos,'suscripcionN':suscripcionN,'secionesN':secionesN})
                else:
                    return render(request,'FitApp/paquetesPago.html',{'sucursal':sucursal,'usuario':usuario,'suscripcionN':suscripcionN,'secionesN':secionesN})
            else:
                return render(request,'FitApp/paquetesPago.html',{'sucursal':sucursal,'usuario':usuario})
        else:
            return render(request,'FitApp/paquetesPago.html',{'sucursal':sucursal,'usuario':usuario})
    else:
        return render(request,'FitApp/paquetesPago.html',{'sucursal':sucursal})

def paquetesPagoDiario(request,sucursal_id):
    try:
        sucursal = Sucursal.objects.get(id=sucursal_id) 
    except Sucursal.DoesNotExist:
        sucursal = False
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            visible = False
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False 
            try:
                suscripcionN = Subscripcion.objects.filter(sucursal=sucursal,cliente=usuario).order_by('-id')[:1]
            except Subscripcion.DoesNotExist:
                suscripcionN = False
            try:
                secionesN = Sesion.objects.filter(sucursal=sucursal,cliente=usuario).order_by('-id')[:1]
            except Sesion.DoesNotExist:
                secionesN = False 
            if secionesN and not suscripcionN:
                visible = False    
            elif not secionesN and suscripcionN:
                visible = False 
            elif secionesN and suscripcionN:
                visible = False 
            elif not secionesN and not suscripcionN:
                visible = True
            try:
                suscripcionF = SubscripcionFree.objects.filter(sucursal=sucursal,cliente=usuario).order_by('-id')[:1]
            except SubscripcionFree.DoesNotExist:
                suscripcionF = False
            if usuario: 
                if not usuario.idCustomer == None:
                    customerID = usuario.idCustomer
                    customer = conekta.Customer.find(customerID)
                    listaMetodos = []
                    metodosPago = customer.payment_sources
                    for m in metodosPago:
                        tarjetas = {'id':m.id, 'last4':m.last4,'brand':m.brand,'exp_month': m.exp_month, 'exp_year':m.exp_year}
                        listaMetodos.append(tarjetas)
                    return render(request,'FitApp/paquetesPagoDiario.html',{'usuario':usuario,'listaMetodos':listaMetodos,'sucursal':sucursal,'suscripcionN':suscripcionN,'secionesN':secionesN,'suscripcionF':suscripcionF,'visible':visible})
                else:
                    return render(request,'FitApp/paquetesPagoDiario.html',{'sucursal':sucursal,'usuario':usuario,'suscripcionN':suscripcionN,'secionesN':secionesN,'suscripcionF':suscripcionF,'visible':visible})  
            else:
                return render(request,'FitApp/paquetesPagoDiario.html',{'sucursal':sucursal,'usuario':usuario}) 
        else:
            return render(request,'FitApp/paquetesPagoDiario.html',{'sucursal':sucursal,'usuario':usuario}) 
    else:
        return render(request,'FitApp/paquetesPagoDiario.html',{'sucursal':sucursal})

def paquetesPagoFree(request,sucursal_id):
    try:
        sucursal = Sucursal.objects.get(id=sucursal_id) 
    except Sucursal.DoesNotExist:
        sucursal = False
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False 
            try:
                suscripcionN = Subscripcion.objects.filter(cliente=usuario,sucursal=sucursal)
            except Subscripcion.DoesNotExist:
                suscripcionN = False
            try:
                secionesN = Sesion.objects.filter(cliente=usuario,sucursal=sucursal)
            except Sesion.DoesNotExist:
                secionesN = False
            try:
                suscripcionF = SubscripcionFree.objects.filter(cliente=usuario,sucursal=sucursal)
            except SubscripcionFree.DoesNotExist:
                suscripcionF = False
            print suscripcionN
            print secionesN
            print suscripcionF
            if usuario:
                if not usuario.idCustomer == None:
                    customerID = usuario.idCustomer
                    customer = conekta.Customer.find(customerID)
                    listaMetodos = []
                    metodosPago = customer.payment_sources
                    for m in metodosPago:
                        tarjetas = {'id':m.id, 'last4':m.last4,'brand':m.brand,'exp_month': m.exp_month, 'exp_year':m.exp_year}
                        listaMetodos.append(tarjetas)
                    return render(request,'FitApp/paquetePagoFree.html',{'usuario':usuario,'listaMetodos':listaMetodos,'sucursal':sucursal,'suscripcionN':suscripcionN,'secionesN':secionesN,'suscripcionF':suscripcionF})
                else:
                    return render(request,'FitApp/paquetePagoFree.html',{'sucursal':sucursal,'usuario':usuario,'suscripcionN':suscripcionN,'secionesN':secionesN,'suscripcionF':suscripcionF})  
            else:
                return render(request,'FitApp/paquetePagoFree.html',{'sucursal':sucursal,'usuario':usuario}) 
        else:
            return render(request,'FitApp/paquetePagoFree.html',{'sucursal':sucursal,'usuario':usuario}) 
    else:
        return render(request,'FitApp/paquetePagoFree.html',{'sucursal':sucursal})
    
def PagoMensualplan(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == "POST":
            sucursalId = request.POST["sucursal"]
            sucursal = Sucursal.objects.get(id=sucursalId)
            usuarioId = request.POST["cliente"]
            usuario = Cliente.objects.get(id=usuarioId)
            precio = request.POST['mensualidad']
            customerID = usuario.idCustomer
            customer = conekta.Customer.find(customerID)
            hoy = date.today()
            renovacion = (hoy + timedelta(30)).strftime('%Y-%m-%d')
            if customer:
                idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id)
                subscription = customer.createSubscription({
                    "plan":idPlan
                })
                if subscription:
                    Ncontrato = Subscripcion(cliente=usuario,sucursal=sucursal,totalCobrar=precio,fechaSubscripcion=hoy,fechaRenovacion=renovacion,activa=True)
                    Ncontrato.save()
                    exito = "tu suscripcion se logro correctamente"
                return render(request,'FitApp/suscripciones.html',{'subscription':subscription,'usuario':usuario,'exito':exito})
            else:
                error = u'Hubo algun error intentelo de nuevo mas tarde'
                return render(request,'FitApp/paquetesPago.html',{'usuario':usuario,'error':error})
        else:
            url = '/Contratar-plan-mensual/'+str(sucursal.id)+'/'
            return HttpResponseRedirect(url)
    else:
        url = '/Contratar-plan-mensual/' +str(sucursal.id)+'/'
        return HttpResponseRedirect(url)

def PagoDiarioplan(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == "POST":
            sucursalId = request.POST["sucursal"]
            sucursal = Sucursal.objects.get(id=sucursalId)
            usuarioId = request.POST["cliente"]
            usuario = Cliente.objects.get(id=usuarioId)
            sesiones = request.POST['sesiones']
            dia = sucursal.dia
            quincePorciento = (dia*15)/100
            diaMasCincoPCT = dia + quincePorciento
            hoy = date.today()
            fin = (hoy + timedelta(30)).strftime('%Y-%m-%d')
            try:
                tarjeta = request.POST['tarjeta']
            except MultiValueDictKeyError:
                tarjeta = False
                errorTarjeta = u'Seleccione una tarjeta'
                return render(request,'FitApp/paquetesPagoDiario.html',{'errorTarjeta':errorTarjeta,'sucursal':sucursal})
            precio = 0
            if sesiones == str(4):
                precio = diaMasCincoPCT * 4
                precio = round(precio,2)
            if sesiones == str(8):
                precio = diaMasCincoPCT * 8
                precio = round(precio,2)
            if sesiones == str(12):
                precio = diaMasCincoPCT * 12
                precio = round(precio,2)
            if sesiones == str(1):
                nSubscripcion = SubscripcionFree(cliente=usuario,sucursal=sucursal,fechaSubscripcion=hoy,fechaFin=fin,activa=True)
                nSubscripcion.save()
                exito = "tu suscripcion se logro correctamente"
                return render(request,'FitApp/suscripciones.html',{'usuario':usuario,'exito':exito,'sucursal':sucursal})
            customerID = usuario.idCustomer
            customer = conekta.Customer.find(customerID)
            aux = float(precio)
            pagototal = int(aux) * 100
            print pagototal
            if customer:
                try:
                    order = conekta.Order.create({
                        "currency": "MXN",
                        "customer_info": {
                            "customer_id": customer.id
                        },
                        "line_items": [{
                            "name": "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id),
                            "unit_price": pagototal,
                            "quantity": 1
                        }],
                        "charges": [{
                                "payment_method": {
                                    "payment_source_id":tarjeta,
                                    "type": "card"
                                }
                            }]
                        })
                    if order:
                        nSesiones = Sesion(cliente=usuario,sucursal=sucursal,total=aux,sesiones=sesiones,activo=True)
                        nSesiones.save()
                        exito = "tu suscripcion se logro correctamente"
                    return render(request,'FitApp/suscripciones.html',{'order':order,'usuario':usuario,'exito':exito})
                except conekta.ConektaError as e:
                    error = e.message
                    order = False     
                    return render(request,'FitApp/paquetesPagoDiario.html',{'error':error,'usuario':usuario})
                else:
                    return render(request,'FitApp/paquetesPagoDiario.html',{'usuario':usuario})
            else:
                return render(request,'FitApp/paquetesPagoDiario.html')
        else:
            return render(request,'FitApp/paquetesPagoDiario.html')
    else:
        return render(request,'FitApp/paquetesPagoDiario.html')

def PagPlanFree(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == "POST":
            sucursalId = request.POST["sucursal"]
            sucursal = Sucursal.objects.get(id=sucursalId)
            usuarioId = request.POST["cliente"]
            usuario = Cliente.objects.get(id=usuarioId)
            dia = sucursal.dia
            hoy = date.today()
            fin = (hoy + timedelta(30)).strftime('%Y-%m-%d')
            # try:
            #     Subscripcion = SubscripcionFree.objects.get(cliente=usuario)
            # except SubscripcionFree.DoesNotExist:
            #     Subscripcion = False
            # if Subscripcion:
            #     error = U'Solo se puede una suscripción por usuario'
            #     return render(request,'FitApp/paquetePagoFree.html',{'sucursal':sucursal,'usuario':usuario,'error':error})
            nSubscripcion = SubscripcionFree(cliente=usuario,sucursal=sucursal,fechaSubscripcion=hoy,fechaFin=fin,activa=True,sesiones=dia)
            nSubscripcion.save()
            exito = "tu suscripcion se logro correctamente"
            return render(request,'FitApp/suscripciones.html',{'usuario':usuario,'exito':exito,'sucursal':sucursal})
        else:
            error = U'Solo se puede una suscripción por usuario'
            return render(request,'FitApp/paquetePagoFree.html',{'sucursal':sucursal,'usuario':usuario,'error':error})
    else:
        error = U'Hubo algun error'
        return render(request,'FitApp/paquetePagoFree.html',{'sucursal':sucursal,'usuario':usuario,'error':error})

def LoginClientes(request):
    return render(request,'FitApp/loginCliente.html')

def RegitrarseClinete(request):
    # targetURL = "https://api.smsmasivos.com.mx/auth"
    # data = {'apikey':"d40b8b72851957ad4f4382f5860027086f7a777e"}
    # r = requests.post(url = targetURL, data = data)
    # prueba = json.loads(r.text)
    # tok = prueba['token']
    # print (tok)
    # targetURL = "https://api.smsmasivos.com.mx/protected/json/phones/verification/start"
    # headers = {
    #     'token':tok
    # }
    # data = {
    #     'phone_number':"8442807852",
    #     'country_code': str(52)
    # }
    # rd = requests.post(url = targetURL, data = data, headers = headers)

    # print(rd.text)
    # for m in r:
    #     prueba = {"token":"m.token"}
    #     print prueba
    return render(request,'FitApp/registroCliente.html')

def verificacion(request):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
        return render(request,'FitApp/verificacion.html',{'usuario':usuario})
    else:
        return render(request,'FitApp/loginCliente.html',{'message':'User does not exist'})

def loginCliente(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        username = username.lower()
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            if not request.user.is_staff:
                url = '/PerfilUsuario/'
                return HttpResponseRedirect(url)
            else:
                return render(request,'FitApp/loginCliente.html',{'message':'Usuario o contraseña incorrecta'})
        else:
            return render(request,'FitApp/loginCliente.html',{'message':'Usuario o contraseña incorrecta'})
        if request.user.is_authenticated():
            if not request.user.is_staff:
                url = '/PerfilUsuario/'
                return HttpResponseRedirect(url)
            else:
                return render(request,'FitApp/loginCliente.html',{'message':'Usuario o contraseña incorrecta'})
        else:
            return render(request,'FitApp/loginCliente.html',{'message':'Usuario o contraseña incorrecta'})
    else:
        return render(request,'FitApp/loginCliente.html')

def RegistroCliente(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        contrasena = request.POST['password']
        objetivo = request.POST['objetivo']
        targetURL = "https://api.smsmasivos.com.mx/auth"
        data = {'apikey':"d40b8b72851957ad4f4382f5860027086f7a777e"}
        r = requests.post(url = targetURL, data = data)
        prueba = json.loads(r.text)
        tok = prueba['token']
        if objetivo == str(1):
            salud = True
        else:
            salud = False
        if objetivo == str(2):
            convivir = True
        else:
            convivir = False

        if objetivo == str(3):
            diversion = True
        else:
            diversion = False
        if objetivo == str(4):
            vermeBien = True
        else:
            vermeBien = False
        try:
            telefono = request.POST['telefono']
        except MultiValueDictKeyError:
            telefono = False
        try:
            hombre = request.POST['hombre']
        except MultiValueDictKeyError:
            hombre = False
        try:
            mujer = request.POST['mujer']
        except MultiValueDictKeyError:
            mujer = False
        email = email.lower()
        mailused = None
        try:
            mailused = User.objects.get(email=email)
            mailExistente = str(mailused.email)
            error = u'EL correo que intenta ingresar ya existe'
            return render(request,'FitApp/registroCliente.html',{'error':error})
        except User.DoesNotExist:
            mailused = None
        if mailused is None:
            user = User.objects.create_user(username=email, email=email)
            user.set_password(contrasena)
            user.save()
            usuario = Cliente(user=user,nombre=nombre,apellido=apellido,hombre=hombre,mujer=mujer,salud=salud,convivir=convivir,vermeBien=vermeBien,diversion=diversion,telefono=telefono)
            usuario.save()
            # autetificacion de codigo cel
            targetURL = "https://api.smsmasivos.com.mx/protected/json/phones/verification/start"
            headers = {
                'token':tok
            }
            data = {
                'phone_number':telefono,
                'country_code': str(52)
            }
            rd = requests.post(url = targetURL, data = data, headers = headers)
            cod = json.loads(rd.text)
            codigouser = cod['code']
            print codigouser
            user = authenticate(username=user.username,password=contrasena)
            if codigouser == "verification_01":
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request,'FitApp/verificacion.html',{'usuario':usuario,'tok':tok})
                    else:
                        return HttpResponse("inactive user")
                else:
                    return render(request,'FitApp/registroCliente.html')
            elif codigouser == "verification_02":
                error = u'Error en la información de la petición intentelo de nuevo'
                user.delete()
                usuario.delete()
                return render(request,'FitApp/registroCliente.html',{'error':error})
            elif codigouser == "verification_03":
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request,'FitApp/verificacion.html',{'usuario':usuario,'tok':tok})
                    else:
                        return HttpResponse("inactive user")
                else:
                    return render(request,'FitApp/registroCliente.html')
            elif codigouser == "verification_04":
                error = u'Usuario ya verificado intente con otro número'
                user.delete()
                usuario.delete()
                return render(request,'FitApp/registroCliente.html',{'error':error})
        else:
            url = '/Registrarse/'
            return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect('/Registrarse/')

def codigoVerificacion(request):
    if request.method == "POST":
        usuarioID = request.POST['usuario']
        usuario = Cliente.objects.get(id=usuarioID)
        token = request.POST['token']
        codigo = request.POST['codigo']
        targetURL = "https://api.smsmasivos.com.mx/protected/json/phones/verification/check"
        headers = {
            'token':token
        }
        data = {
            'phone_number':usuario.telefono,
            'verification_code':codigo
        }
        r = requests.post(url = targetURL, data = data, headers = headers)
        resultado = json.loads(r.text)
        validacion = resultado['code']
        if validacion == "validation_01":
            url = '/PerfilUsuario/'
            return HttpResponseRedirect(url)
        if validacion == "validation_02":
            error = u'Error en la información de la petición'
            return render(request,'FitApp/verificacion.html',{'error':error,'token':token,'usuario':usuario})
        if validacion == "validation_03":
            error = u'Número de intentos excedido intentelo de nuevo mas tarde'
            return render(request,'FitApp/verificacion.html',{'error':error,'token':token,'usuario':usuario})
    else:
        return HttpResponseRedirect('/Registrarse/')

def usuarioTelefono(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == "POST":
            usuarioID = request.POST['usuario']
            usuario = Cliente.objects.get(id=usuarioID)
            telefono = request.POST['telefono']
            targetURL = "https://api.smsmasivos.com.mx/auth"
            data = {'apikey':"d40b8b72851957ad4f4382f5860027086f7a777e"}
            r = requests.post(url = targetURL, data = data)
            prueba = json.loads(r.text)
            tok = prueba['token']
            usuario.telefono = telefono
            usuario.save()
            # autetificacion de codigo cel
            targetURL = "https://api.smsmasivos.com.mx/protected/json/phones/verification/start"
            headers = {
                'token':tok
            }
            data = {
                'phone_number':telefono,
                'country_code': str(52)
            }
            rd = requests.post(url = targetURL, data = data, headers = headers)
            cod = json.loads(rd.text)
            codigouser = cod['code']
            print codigouser
            if codigouser == "verification_01":
                return render(request,'FitApp/verificacion.html',{'usuario':usuario,'tok':tok})
            elif codigouser == "verification_02":
                error = u'Error en la información de la petición intentelo de nuevo'
                return render(request,'FitApp/verificacion.html',{'error':error})
            elif codigouser == "verification_03":
                return render(request,'FitApp/verificacion.html',{'usuario':usuario,'tok':tok})
            elif codigouser == "verification_04":
                error = u'Usuario ya verificado intente con otro número'
                return render(request,'FitApp/verificacion.html',{'error':error})
        else:
            url = '/PerfilUsuario/'
            return HttpResponseRedirect(url)
    else:
        return render(request,'FitApp/loginCliente.html',{'message':'User does not exist'})

def consultaFacebook(request,idFace,email,nombre,apellido):
    try:
        usuario = Cliente.objects.get(user__username=email)
    except Cliente.DoesNotExist:
        usuario = False
    if usuario:
        if usuario.idFacebook == idFace:
            username = usuario.user.username
            password = usuario.user.password
            user = usuario.user
            login(request,user, backend='django.contrib.auth.backends.ModelBackend')
            if not request.user.is_staff:
                url = '/PerfilUsuario/'
                return HttpResponseRedirect(url)
    elif not usuario:
        user = User.objects.create_user(username=email, email=email)
        user.set_password(idFace)
        user.save()
        usuarioC = Cliente(user=user,nombre=nombre,apellido=apellido,idFacebook=idFace)
        usuarioC.save()
        user = authenticate(username=user.username,password=idFace)
        if user is not None:
            if user.is_active:
                login(request, user)
                url = '/PerfilUsuario/'
                return HttpResponseRedirect(url)
            else:
                return HttpResponse("inactive user")
        else:
            url = '/PerfilUsuario/'
            return HttpResponseRedirect(url)
    else:
        return render(request,'FitApp/loginCliente.html')

def consultaGoogle(request,idGoogle,email,nombre,apellido):
    try:
        usuario = Cliente.objects.get(user__username=email)
    except Cliente.DoesNotExist:
        usuario = False
    if usuario:
        if usuario.idGoogle == idGoogle:
            username = usuario.user.username
            password = usuario.user.password
            user = usuario.user
            login(request,user, backend='django.contrib.auth.backends.ModelBackend')
            if not request.user.is_staff:
                url = '/PerfilUsuario/'
                return HttpResponseRedirect(url)
    elif not usuario:
        user = User.objects.create_user(username=email, email=email)
        user.set_password(idGoogle)
        user.save()
        usuarioC = Cliente(user=user,nombre=nombre,apellido=apellido,idGoogle=idGoogle)
        usuarioC.save()
        user = authenticate(username=user.username,password=idGoogle)
        if user is not None:
            if user.is_active:
                login(request, user)
                url = '/PerfilUsuario/'
                return HttpResponseRedirect(url)
            else:
                return HttpResponse("inactive user")
        else:
            url = '/PerfilUsuario/'
            return HttpResponseRedirect(url)
    else:
        return render(request,'FitApp/loginCliente.html')

def LogoutPerfil(request):
    logout(request)
    return HttpResponseRedirect('/')

def PerfilCliente(request):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
            ciudad = Ciudad.objects.all()
        return render(request,'FitApp/perfil.html',{'usuario':usuario,'ciudad':ciudad})
    else:
        return render(request,'FitApp/loginCliente.html',{'message':'User does not exist'})

def EditCliente(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == "POST":
            UsuarioId = request.POST["usuario"]
            usuario = Cliente.objects.get(id=UsuarioId)
            nombre = request.POST["nombre"]
            apellido = request.POST["apellido"]
            # telefono = request.POST["telefono"]
            try:
                foto = request.FILES['foto']
            except MultiValueDictKeyError:
                foto = False
            try:
                ciudadID = request.POST["ciudad"]
            except MultiValueDictKeyError:
                ciudadID = None 
            try:
                ciudad = Ciudad.objects.get(id=ciudadID)
            except Ciudad.DoesNotExist:
                ciudad = None
            objetivo = request.POST["objetivo"]
            if objetivo == str(1):
                salud = True
            else:
                salud = False
            if objetivo == str(2):
                convivir = True
            else:
                convivir = False

            if objetivo == str(3):
                diversion = True
            else:
                diversion = False
            if objetivo == str(4):
                vermeBien = True
            else:
                vermeBien = False
            fotoActual = usuario.foto.name
            if foto == False:
                usuario.nombre = nombre
                usuario.apellido = apellido
                usuario.ciudad = ciudad
                usuario.salud = salud
                usuario.convivir = convivir
                usuario.diversion = diversion
                usuario.vermeBien = vermeBien
                usuario.save()
                url = '/PerfilUsuario/'
                return HttpResponseRedirect(url)
            elif not foto == False:
                if not fotoActual == 'default/perfil.png':
                    os.remove(usuario.foto.path)
                usuario.nombre = nombre
                usuario.apellido = apellido
                usuario.ciudad = ciudad
                usuario.salud = salud
                usuario.convivir = convivir
                usuario.diversion = diversion
                usuario.vermeBien = vermeBien
                usuario.foto = foto
                usuario.save()
                url = '/PerfilUsuario/'
                return HttpResponseRedirect(url)
        else:
            return render(request,'FitApp/perfil.html',{'usuario':usuario})
    else:
        return render(request,'FitApp/loginCliente.html',{'message':'User does not exist'})

def selectObjetivo(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == "POST":
            UsuarioId = request.POST["usuario"]
            usuario = Cliente.objects.get(id=UsuarioId)
            objetivo = request.POST["objetivos"]
            if objetivo == str(1):
                salud = True
            else:
                salud = False
            if objetivo == str(2):
                convivir = True
            else:
                convivir = False
            if objetivo == str(3):
                diversion = True
            else:
                diversion = False
            if objetivo == str(4):
                vermeBien = True
            else:
                vermeBien = False
            try:
                hombre = request.POST['hombre']
            except MultiValueDictKeyError:
                hombre = False
            try:
                mujer = request.POST['mujer']
            except MultiValueDictKeyError:
                mujer = False
            usuario.salud = salud
            usuario.convivir = convivir
            usuario.diversion = diversion
            usuario.vermeBien = vermeBien
            usuario.hombre = hombre
            usuario.mujer = mujer
            usuario.save()
            url = '/PerfilUsuario/'
            return HttpResponseRedirect(url)
        else:
            return render(request,'FitApp/perfil.html',{'usuario':usuario})
    else:
        return render(request,'FitApp/loginCliente.html',{'message':'User does not exist'})

def FavoritosCliente(request):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
            try:
                favoritos = Favorito.objects.filter(cliente=usuario)
            except Favorito.DoesNotExist:
                favoritos = False
        return render(request,'FitApp/favoritos.html',{'usuario':usuario,'favoritos':favoritos})
    else:
        return render(request,'FitApp/loginCliente.html',{'message':'User does not exist'})

def TarjetasCliente(request):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
            if usuario:
                if not usuario.idCustomer == None:
                    customerID = usuario.idCustomer
                    customer = conekta.Customer.find(customerID)
                    listaMetodos = []
                    metodosPago = customer.payment_sources
                    for m in metodosPago:
                        tarjetas = {'id':m.id, 'last4':m.last4,'brand':m.brand,'exp_month': m.exp_month, 'exp_year':m.exp_year}
                        listaMetodos.append(tarjetas)
                    return render(request,'FitApp/tarjetas.html',{'usuario':usuario,'listaMetodos':listaMetodos})
                else:
                    return render(request,'FitApp/tarjetas.html',{'usuario':usuario})
            else:
                return render(request,'FitApp/tarjetas.html',{'usuario':usuario})
        else:
            return render(request,'FitApp/tarjetas.html',{'usuario':usuario})
    else:
        return render(request,'FitApp/loginCliente.html')

def AddTarjetas(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == "POST":
            usuarioID = request.POST['usuario']
            usuario = Cliente.objects.get(id=usuarioID)
            try:
                token = request.POST['conektaTokenId']
            except MultiValueDictKeyError:
                token = False
            try:
                exp_month = request.POST['exp_month']
            except MultiValueDictKeyError:
                exp_month = False
            try:
                exp_year = request.POST['exp_year']
            except MultiValueDictKeyError:
                exp_year = False
            if usuario.idCustomer == None:
                try:
                    customer = conekta.Customer.create({
                        'name': usuario.nombre,
                        'email': usuario.user.username,
                        'payment_sources': [{
                        'type': 'card',
                        'token_id': token
                        }]
                    })
                except conekta.ConektaError as e:
                    error = e.message
                    print error
                if customer:
                    usuario.idCustomer = customer.id
                    usuario.save()
                    url = '/Mis-tarjetas/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def MetodosPagoConekta(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == "POST":
            usuarioID = request.POST['usuario']
            usuario = Cliente.objects.get(id=usuarioID)
            token = request.POST['conektaTokenId']
            customerID = usuario.idCustomer
            customer = conekta.Customer.find(customerID)
            try:
                source = customer.createPaymentSource({"type": "card","token_id": token})
            except conekta.ConektaError as e:
                mensajeError = e.message
                source = False
                print mensajeError
            url = '/Mis-tarjetas/'
            return HttpResponseRedirect(url)
        else:
            url = '/Mis-tarjetas/'
            return HttpResponseRedirect(url)
    else:
        url = '/Mis-tarjetas/'
        return HttpResponseRedirect(url)

def eliminarPagos(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == "POST":
            usuarioID = request.POST['usuario']
            usuario = Cliente.objects.get(id=usuarioID)
            metodoID = request.POST['metodo']
            customerID = usuario.idCustomer
            customer = conekta.Customer.find(customerID)
            if customer:
                try:
                    source = customer.payment_sources
                    for s in source:
                        if s.id == metodoID:
                            s.delete()
                except conekta.ConektaError as e:
                    mensaje = e.message
                url = '/Mis-tarjetas/'
                return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect('/')

def SuscripcionesPerfil(request):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
            if usuario:
                try:
                    subscripcion = Subscripcion.objects.filter(cliente=usuario)
                except Subscripcion.DoesNotExist:
                    subscripcion = False
                try:
                    subscripcionFree = SubscripcionFree.objects.filter(cliente=usuario)
                except subscripcionFree.DoesNotExist:
                    subscripcionFree = False
                try:
                    sesiones = Sesion.objects.filter(cliente=usuario)
                except Sesion.DoesNotExist:
                    sesiones = False
        return render(request,'FitApp/suscripciones.html',{'usuario':usuario,'subscripcion':subscripcion,'sesiones':sesiones,'subscripcionFree':subscripcionFree})
    else:
        return render(request,'FitApp/loginCliente.html',{'message':'User does not exist'})

def PlanContratado(request,suscripcion_id):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
            if usuario:
                try:
                    subscripcion = Subscripcion.objects.get(id=suscripcion_id)
                except Subscripcion.DoesNotExist:
                    subscripcion = False
        return render(request,'FitApp/plancontratado.html',{'usuario':usuario,'subscripcion':subscripcion})
    else:
        return render(request,'FitApp/loginCliente.html',{'message':'User does not exist'})

def PlanContratadoDiario(request,sesiones_id):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
            if usuario:
                try:
                    sesiones = Sesion.objects.get(id=sesiones_id)
                except Sesion.DoesNotExist:
                    sesiones = False
        return render(request,'FitApp/plancontratadodiario.html',{'usuario':usuario,'sesiones':sesiones})
    else:
        return render(request,'FitApp/loginCliente.html',{'message':'User does not exist'})

def CalendarioPerfil(request):
    usuario = False
    if request.user.is_authenticated and not request.user.is_staff:
        user = request.user
        if user:
            try:
                usuario = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                usuario = False
        return render(request,'FitApp/CalendarioPerfil.html',{'usuario':usuario})
    else:
        return render(request,'FitApp/loginCliente.html',{'message':'User does not exist'})

def Legal(request):
    return render(request,'FitApp/legal.html')

def Avisos(request):
    return render(request,'FitApp/Avisos.html')

def LegalDos(request):
    return render(request,'FitApp/LegalDos.html')

def IndexUsers(request):
    return render(request,'FitApp/indexUsers.html')

def correoContacto(request):
    if request.method == "POST":
        Nombre = request.POST['nombre']
        Nombre_club = request.POST['club']
        Email = request.POST['correo']
        telefono = request.POST['telefono']
        try:
            Mensaje = request.POST['Comentarios']
        except MultiValueDictKeyError:
            Mensaje = ' '
        emailSucess = True
        subject = Nombre
        fromMail = Email
        message = 'Tiene un nuevo mensaje de: ' + Nombre + '\n' +'Correo: '+ Email + '\n' + 'Nombre Club/Gimnasio: '+ Nombre_club + '\n' + 'Telefono: '+ telefono + '\n' + 'Mensaje: '+ Mensaje + '\n'
        send_mail(subject, message, fromMail, ['info@fitory.com'], fail_silently=False,)
        respuesta = u'Tu solicitud se envió correctamente en breve nos comunicamos'
        return render(request, 'FitApp/index.html', {'respuesta':respuesta})
    else:
        return HttpResponseRedirect('/')

def loginAdmin(request):
	next = request.GET.get('next', '/homeAdmin/')
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if request.user.is_staff:
					return HttpResponseRedirect('/homeAdmin/')
				else:
					return render(request,'FitApp/loginAdmin.html',{'message':'User does not exist'})
			else:
				return HttpResponse("Inactive user.")
		else:
			return render(request,'FitApp/loginAdmin.html',{'message':'User does not exist'})
	if request.user.is_authenticated():
		if request.user.is_staff:
			return HttpResponseRedirect('/homeAdmin/')
		else:
			return render(request,'FitApp/loginAdmin.html',{'message':'User does not exist'})
	return render(request,'FitApp/loginAdmin.html')

def homeAdmin(request):
    if request.user.is_staff and request.user.is_authenticated:
    	user = request.user
        return render(request,'FitApp/homeAdmin.html',{'user':user})
    else:
        return HttpResponseRedirect('/loginAdmin/')

def homeAdminEstados(request):
    if request.user.is_staff and request.user.is_authenticated:
    	try:
            estados = Estado.objects.all()
        except Estado.DoesNotExist:
            estados = False
        numEstados = len(estados)
        estadoDatos = []
        if estados:
            for e in estados:
                try:
                    ciudades = Ciudad.objects.filter(estado=e)
                except Ciudad.DoesNotExist:
                    ciudades = False
                if ciudades:
                    estadoDatos.append((e,True))
                else:
                    estadoDatos.append((e,False))
        return render(request,'FitApp/homeAdminEstados.html',{'estados':estados,'estadoDatos':estadoDatos,'numEstados':numEstados})
    else:
        return HttpResponseRedirect('/loginAdmin/')

class ReporteEstados(View):
    def get(self,request):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                estados = Estado.objects.all()
            except Estado.DoesNotExist:
                estados = False
            if estados:
                filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                wb = xlsxwriter.Workbook(filename)
                center = wb.add_format({'align':'center'})
                format = wb.add_format({'align':'center'})
                format.set_text_wrap()
                gris = wb.add_format({'font_color':'#9e9e9e'})
                header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                sheet = wb.add_worksheet(u'Estados')
                sheet.write(0,0,u'ID',header)
                sheet.write(0,1,u'NOMBRE',header)
                sheet.set_column('A:A', 20)
                sheet.set_column('B:B', 20)
                sheet.protect()
                row = 0
                for e in estados:
                    row += 1
                    sheet.write(row,0,e.id,body)
                    sheet.write(row,1,e.nombre,body)
                wb.close()
                return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

def addEstado(request):
    if request.user.is_staff and request.user.is_authenticated:
    	if request.method == "POST":
            nombre = request.POST['nombre']
            repetido = False
            try:
                repetido = Estado.objects.get(nombre=nombre)
            except Estado.DoesNotExist:
                repetido = False
            if not repetido:
                estado = Estado(nombre=nombre)
                estado.save()
                return HttpResponseRedirect('/homeAdminEstados/')
            else:
                error = 'Ya existe un estado con el mismo nombre.'
                return render(request,'FitApp/errorEstado.html',{'error':error})
        else:
            return HttpResponseRedirect('/homeAdminEstados/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def editEstado(request):
    if request.user.is_staff and request.user.is_authenticated:
    	if request.method == "POST":
            estadoID = request.POST['estado']
            estado = Estado.objects.get(id=estadoID)
            nombre = request.POST['nombre']
            estado.nombre = nombre
            estado.save()
            return HttpResponseRedirect('/homeAdminEstados/')
        else:
            return HttpResponseRedirect('/homeAdminEstados/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def deleteEstado(request,estado_id):
    if request.user.is_staff and request.user.is_authenticated:
    	try:
            estado = Estado.objects.get(id=estado_id)
        except Estado.DoesNotExist:
            estado = False
        if estado:
            estado.delete()
            return HttpResponseRedirect('/homeAdminEstados/')
        else:
            return HttpResponseRedirect('/homeAdminEstados/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def homeAdminEstadoCiudades(request,estado_id):
    if request.user.is_staff and request.user.is_authenticated:
    	try:
            estado = Estado.objects.get(id=estado_id)
        except Estado.DoesNotExist:
            estado = False
        if estado:
            try:
                ciudadesT = Ciudad.objects.filter(estado=estado)
            except Ciudad.DoesNotExist:
                ciudadesT = False
            try:
                ciudades = Ciudad.objects.filter(estado=estado).order_by('id')
            except Ciudad.DoesNotExist:
                ciudades = False
            page = request.GET.get('page', 1)
            paginator = Paginator(ciudades,50)
            try:
                ciudades = paginator.page(page)
            except PageNotAnInteger:
                ciudades = paginator.page(1)
            except EmptyPage:
                ciudades = paginator.page(paginator.num_pages)
            ciudadDatos = []
            if ciudades:
                for c in ciudades:
                    try:
                        clientes = Cliente.objects.filter(ciudad=c)
                    except Cliente.DoesNotExist:
                        clientes = False
                    try:
                        sucursales = Sucursal.objects.filter(ciudad=c)
                    except Sucursal.DoesNotExist:
                        sucursales = False
                    if clientes and sucursales:
                        ciudadDatos.append((c,True))
                    elif clientes and not sucursales:
                        ciudadDatos.append((c,True))
                    elif not clientes and sucursales:
                        ciudadDatos.append((c,True))
                    elif not clientes and not sucursales:
                        ciudadDatos.append((c,False))
            return render(request,'FitApp/homeAdminEstadoCiudades.html',{'estado':estado,'ciudades':ciudades,'ciudadesT':ciudadesT,'ciudadDatos':ciudadDatos})
        else:
            return HttpResponseRedirect('/homeAdminEstados/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

class ReporteEstadoCiudades(View):
    def get(self,request,estado_id):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                estado = Estado.objects.get(id=estado_id)
            except Estado.DoesNotExist:
                estado = False
            if estado:
                try:
                    ciudades = Ciudad.objects.filter(estado=estado)
                except Ciudad.DoesNotExist:
                    ciudades = False
                if ciudades:
                    filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                    wb = xlsxwriter.Workbook(filename)
                    center = wb.add_format({'align':'center'})
                    format = wb.add_format({'align':'center'})
                    format.set_text_wrap()
                    gris = wb.add_format({'font_color':'#9e9e9e'})
                    header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                    body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                    titulo = u' - Ciudades'
                    sheet = wb.add_worksheet(titulo)
                    sheet.write(0,0,u'ID',header)
                    sheet.write(0,1,u'NOMBRE',header)
                    sheet.set_column('A:A', 20)
                    sheet.set_column('B:B', 20)
                    sheet.protect()
                    row = 0
                    for c in ciudades:
                        row += 1
                        sheet.write(row,0,c.id,body)
                        sheet.write(row,1,c.nombre,body)
                    wb.close()
                    return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

def addCiudad(request):
    if request.user.is_staff and request.user.is_authenticated:
    	if request.method == "POST":
            estadoID = request.POST['estado']
            estado = Estado.objects.get(id=estadoID)
            nombre = request.POST['nombre']
            repetido = False
            try:
                repetido = Ciudad.objects.get(estado=estado,nombre=nombre)
            except Ciudad.DoesNotExist:
                repetido = False
            if not repetido:
                ciudad = Ciudad(estado=estado,nombre=nombre)
                ciudad.save()
                url = '/homeAdminEstados/'+str(estado.id)+'/'
                return HttpResponseRedirect(url)
            else:
                error = 'Ya existe una ciudad con el mismo nombre, en el mismo estado.'
                return render(request,'FitApp/errorCiudad.html',{'error':error,'estado':estado})
        else:
            return HttpResponseRedirect('/homeAdminEstados/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def editCiudad(request):
    if request.user.is_staff and request.user.is_authenticated:
    	if request.method == "POST":
            ciudadID = request.POST['ciudad']
            ciudad = Ciudad.objects.get(id=ciudadID)
            nombre = request.POST['nombre']
            ciudad.nombre = nombre
            ciudad.save()
            url = '/homeAdminEstados/'+str(ciudad.estado.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminEstados/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def deleteCiudad(request,ciudad_id):
    if request.user.is_staff and request.user.is_authenticated:
    	try:
            ciudad = Ciudad.objects.get(id=ciudad_id)
        except Ciudad.DoesNotExist:
            ciudad = False
        if ciudad:
            estado = ciudad.estado
            ciudad.delete()
            url = '/homeAdminEstados/'+str(estado.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminEstados/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def homeAdminServicios(request):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            serviciosT = Servicio.objects.all()
        except Servicio.DoesNotExist:
            serviciosT = False
    	try:
            servicios = Servicio.objects.all().order_by('id')
        except Servicio.DoesNotExist:
            servicios = False
        page = request.GET.get('page', 1)
        paginator = Paginator(servicios,50)
        try:
			servicios = paginator.page(page)
        except PageNotAnInteger:
			servicios = paginator.page(1)
        except EmptyPage:
			servicios = paginator.page(paginator.num_pages)
        servicioDatos = []
        if servicios:
            for s in servicios:
                try:
                    relaciones = ServicioClub.objects.filter(servicio=s)
                except Servicio.DoesNotExist:
                    relaciones = False
                if relaciones:
                    servicioDatos.append((s,True))
                else:
                    servicioDatos.append((s,False))
        return render(request,'FitApp/homeAdminServicios.html',{'servicios':servicios,'serviciosT':serviciosT,'servicioDatos':servicioDatos})
    else:
        return HttpResponseRedirect('/loginAdmin/')

class ReporteServicios(View):
    def get(self,request):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                servicios = Servicio.objects.all()
            except Servicio.DoesNotExist:
                servicios = False
            if servicios:
                filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                wb = xlsxwriter.Workbook(filename)
                center = wb.add_format({'align':'center'})
                format = wb.add_format({'align':'center'})
                format.set_text_wrap()
                gris = wb.add_format({'font_color':'#9e9e9e'})
                header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                sheet = wb.add_worksheet(u'Servicios')
                sheet.write(0,0,u'ID',header)
                sheet.write(0,1,u'NOMBRE',header)
                sheet.write(0,2,u'ICONO',header)
                sheet.set_column('A:A', 20)
                sheet.set_column('B:B', 20)
                sheet.set_column('C:C', 60)
                sheet.protect()
                row = 0
                for s in servicios:
                    row += 1
                    icono = 'https://www.fitory.com/media/'+s.icono.name
                    sheet.write(row,0,s.id,body)
                    sheet.write(row,1,s.nombre,body)
                    sheet.write(row,2,icono,body)
                wb.close()
                return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

def addServicio(request):
    if request.user.is_staff and request.user.is_authenticated:
    	if request.method == "POST":
            nombre = request.POST['nombre']
            try:
                icono = request.FILES['icono']
            except MultiValueDictKeyError:
                icono = False
            repetido = False
            try:
                repetido = Servicio.objects.get(nombre=nombre)
            except Servicio.DoesNotExist:
                repetido = False
            if not repetido:
                if icono:
                    servicio = Servicio(nombre=nombre,icono=icono)
                    servicio.save()
                else:
                    servicio = Servicio(nombre=nombre)
                    servicio.save()
                return HttpResponseRedirect('/homeAdminServicios/')
            else:
                error = 'Ya existe un servicio con el mismo nombre'
                return render(request,'FitApp/errorServicio.html',{'error':error})
        else:
            return HttpResponseRedirect('/homeAdminServicios/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def editServicio(request):
    if request.user.is_staff and request.user.is_authenticated:
    	if request.method == "POST":
            servicioID = request.POST['servicio']
            servicio = Servicio.objects.get(id=servicioID)
            nombre = request.POST['nombre']
            try:
                icono = request.FILES['icono']
            except MultiValueDictKeyError:
                icono = False
            servicio.nombre = nombre
            servicio.save()
            servicioIconoActual = servicio.icono.name
            if icono:
                if servicioIconoActual == 'default/servicio.png':
                    servicio.icono = icono
                    servicio.save()
                else:
                    os.remove(servicio.icono.path)
                    servicio.icono = icono
                    servicio.save()
            return HttpResponseRedirect('/homeAdminServicios/')
        else:
            return HttpResponseRedirect('/homeAdminServicios/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def deleteServicio(request,servicio_id):
    if request.user.is_staff and request.user.is_authenticated:
    	try:
            servicio = Servicio.objects.get(id=servicio_id)
        except Servicio.DoesNotExist:
            servicio = False
        if servicio:
            servicioIconoActual = servicio.icono.name
            if not servicioIconoActual == 'default/servicio.png':
                os.remove(servicio.icono.path)
            servicio.delete()
            return HttpResponseRedirect('/homeAdminServicios/')
        else:
            return HttpResponseRedirect('/homeAdminServicios/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def homeAdminActividades(request):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            actividadesT = Actividad.objects.all()
        except Actividad.DoesNotExist:
            actividadesT = False
    	try:
            actividades = Actividad.objects.all().order_by('id')
        except Actividad.DoesNotExist:
            actividades = False
        page = request.GET.get('page', 1)
        paginator = Paginator(actividades,50)
        try:
			actividades = paginator.page(page)
        except PageNotAnInteger:
			actividades = paginator.page(1)
        except EmptyPage:
			actividades = paginator.page(paginator.num_pages)
        actividadDatos = []
        if actividades:
            for a in actividades:
                try:
                    relaciones = ActividadClub.objects.filter(actividad=a)
                except ActividadClub.DoesNotExist:
                    relaciones = False
                if relaciones:
                    actividadDatos.append((a,True))
                else:
                    actividadDatos.append((a,False))
        return render(request,'FitApp/homeAdminActividades.html',{'actividades':actividades,'actividadesT':actividadesT,'actividadDatos':actividadDatos})
    else:
        return HttpResponseRedirect('/loginAdmin/')

class ReporteActividades(View):
    def get(self,request):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                actividades = Actividad.objects.all()
            except Actividad.DoesNotExist:
                actividades = False
            if actividades:
                filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                wb = xlsxwriter.Workbook(filename)
                center = wb.add_format({'align':'center'})
                format = wb.add_format({'align':'center'})
                format.set_text_wrap()
                gris = wb.add_format({'font_color':'#9e9e9e'})
                header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                sheet = wb.add_worksheet(u'Actividades')
                sheet.write(0,0,u'ID',header)
                sheet.write(0,1,u'NOMBRE',header)
                sheet.write(0,2,u'ICONO',header)
                sheet.set_column('A:A', 20)
                sheet.set_column('B:B', 20)
                sheet.set_column('C:C', 60)
                sheet.protect()
                row = 0
                for a in actividades:
                    row += 1
                    icono = 'https://www.fitory.com/media/'+a.icono.name
                    sheet.write(row,0,a.id,body)
                    sheet.write(row,1,a.nombre,body)
                    sheet.write(row,2,icono,body)
                wb.close()
                return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

def addActividad(request):
    if request.user.is_staff and request.user.is_authenticated:
    	if request.method == "POST":
            nombre = request.POST['nombre']
            try:
                icono = request.FILES['icono']
            except MultiValueDictKeyError:
                icono = False
            repetido = False
            try:
                repetido = Actividad.objects.get(nombre=nombre)
            except Actividad.DoesNotExist:
                repetido = False
            if not repetido:
                if icono:
                    actividad = Actividad(nombre=nombre,icono=icono)
                    actividad.save()
                else:
                    actividad = Actividad(nombre=nombre)
                    actividad.save()
                return HttpResponseRedirect('/homeAdminActividades/')
            else:
                error = 'Ya existe una actividad con el mismo nombre'
                return render(request,'FitApp/errorActividad.html',{'error':error})
        else:
            return HttpResponseRedirect('/homeAdminActividades/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def editActividad(request):
    if request.user.is_staff and request.user.is_authenticated:
    	if request.method == "POST":
            actividadID = request.POST['actividad']
            actividad = Actividad.objects.get(id=actividadID)
            nombre = request.POST['nombre']
            try:
                icono = request.FILES['icono']
            except MultiValueDictKeyError:
                icono = False
            actividad.nombre = nombre
            actividad.save()
            actividadIconoActual = actividad.icono.name
            if icono:
                if actividadIconoActual == 'default/actividad.jpg':
                    actividad.icono = icono
                    actividad.save()
                else:
                    os.remove(actividad.icono.path)
                    actividad.icono = icono
                    actividad.save()
            return HttpResponseRedirect('/homeAdminActividades/')
        else:
            return HttpResponseRedirect('/homeAdminActividades/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def deleteActividad(request,actividad_id):
    if request.user.is_staff and request.user.is_authenticated:
    	try:
            actividad = Actividad.objects.get(id=actividad_id)
        except Actividad.DoesNotExist:
            actividad = False
        if actividad:
            actividadIconoActual = actividad.icono.name
            if not actividadIconoActual == 'default/actividad.jpg':
                os.remove(actividad.icono.path)
            actividad.delete()
            return HttpResponseRedirect('/homeAdminActividades/')
        else:
            return HttpResponseRedirect('/homeAdminActividades/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def homeAdminClubes(request):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            clubesT = Club.objects.all()
        except Club.DoesNotExist:
            clubesT = False
    	try:
            clubes = Club.objects.all().order_by('id')
        except Club.DoesNotExist:
            clubes = False
        page = request.GET.get('page', 1)
        paginator = Paginator(clubes,50)
        try:
			clubes = paginator.page(page)
        except PageNotAnInteger:
			clubes = paginator.page(1)
        except EmptyPage:
			clubes = paginator.page(paginator.num_pages)
        clubDatos = []
        if clubes:
            for c in clubes:
                try:
                    sucursales = Sucursal.objects.filter(club=c)
                except Sucursal.DoesNotExist:
                    sucursales = False
                if not sucursales:
                    clubDatos.append((c,False))
                else:
                    clubDatos.append((c,True))
        formularios = []
        if clubes:
            for c in clubes:
                form = cropFotoClub(instance=c)
                formularios.append((c,form))
        return render(request,'FitApp/homeAdminClubes.html',{'clubesT':clubesT,'clubes':clubes,'clubDatos':clubDatos,'formularios':formularios})
    else:
        return HttpResponseRedirect('/loginAdmin/')

def recortarFotoClub(request):
    if request.user.is_staff and request.user.is_authenticated:
        clubID = request.POST['club']
        club = Club.objects.get(id=clubID)
        form = cropFotoClub(instance=club)
        if request.method == "POST":
            form = cropFotoClub(request.POST,request.FILES,instance=club)
            if form.is_valid():
                thumbnailer = get_thumbnailer(club.foto)
                thumbnailer.delete_thumbnails()
                foto = form.cleaned_data['foto']
                if foto:
					club.foto = foto
					club.fotocrop = 0
                fotocrop = form.cleaned_data['fotocrop']
                club.fotocrop = fotocrop
                club.save()
                thumbnail_url = get_thumbnailer(club.foto).get_thumbnail({'size': (200, 200),'box': club.fotocrop,'crop': True,'detail': True,}).url
                cropURL = thumbnail_url
                club.cropURL = cropURL
                club.save()
                url = '/homeAdminClubes/'+str(club.id)+'/Sucursales/'
                return HttpResponseRedirect(url)
            else:
                url = '/homeAdminClubes/'+str(club.id)+'/Sucursales/'
                return HttpResponseRedirect(url)
        else:
            url = '/homeAdminClubes/'+str(club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect('/loginAdmin/')

class ReporteClubes(View):
    def get(self,request):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                clubes = Club.objects.all()
            except Club.DoesNotExist:
                clubes = False
            if clubes:
                filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                wb = xlsxwriter.Workbook(filename)
                center = wb.add_format({'align':'center'})
                format = wb.add_format({'align':'center'})
                format.set_text_wrap()
                gris = wb.add_format({'font_color':'#9e9e9e'})
                header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                sheet = wb.add_worksheet(u'Clubes')
                sheet.write(0,0,u'ID',header)
                sheet.write(0,1,u'NOMBRE',header)
                sheet.write(0,2,u'FECHA INCORPORACION',header)
                sheet.write(0,3,u'RFC',header)
                sheet.write(0,4,u'BANCO',header)
                sheet.write(0,5,u'TARJETAHABIENTE',header)
                sheet.write(0,6,u'Nº CUENTA',header)
                sheet.write(0,7,u'PÁGINA WEB',header)
                sheet.write(0,8,u'FACEBOOK',header)
                sheet.write(0,9,u'INSTAGRAM',header)
                sheet.write(0,10,u'TWITTER',header)
                sheet.write(0,11,u'EV. PROM',header)
                sheet.write(0,12,u'ESTATUS',header)
                sheet.write(0,13,u'COD. CLUB',header)
                sheet.write(0,14,u'COD. REPRESENTANTE',header)
                sheet.write(0,15,u'DIRECCION',header)
                sheet.write(0,16,u'TELÉFONO',header)
                sheet.write(0,17,u'EMAIL',header)
                sheet.write(0,18,u'FOTO',header)
                sheet.write(0,19,u'ACEPTO TYC',header)
                sheet.write(0,20,u'FECHA TYC',header)
                sheet.set_column('A:A', 20)
                sheet.set_column('B:B', 20)
                sheet.set_column('C:C', 50)
                sheet.set_column('D:D', 50)
                sheet.set_column('E:E', 50)
                sheet.set_column('F:F', 50)
                sheet.set_column('G:G', 50)
                sheet.set_column('H:H', 50)
                sheet.set_column('I:I', 50)
                sheet.set_column('J:J', 50)
                sheet.set_column('K:K', 50)
                sheet.set_column('L:L', 50)
                sheet.set_column('M:M', 50)
                sheet.set_column('N:N', 50)
                sheet.set_column('O:O', 50)
                sheet.set_column('P:P', 50)
                sheet.set_column('Q:Q', 50)
                sheet.set_column('R:R', 50)
                sheet.set_column('S:S', 50)
                sheet.set_column('T:T', 50)
                sheet.set_column('U:U', 50)
                sheet.protect()
                row = 0
                for c in clubes:
                    row += 1
                    estatus = ''
                    if c.activado == True:
                        estatus = 'Activo'
                    else:
                        estatus = 'Inactivo'
                    foto = 'https://www.fitory.com/media/'+c.foto.name
                    acepto = ''
                    if c.Legal == True:
                        acepto = 'Si'
                    else:
                        acepto = 'No'
                    fechaAcepto = ''
                    if c.fechaLegal:
                        fechaAcepto = c.fechaLegal.strftime('%d-%m-%Y')
                    else:
                        fechaAcepto = '-'
                    sheet.write(row,0,c.id,body)
                    sheet.write(row,1,c.nombre,body)
                    sheet.write(row,2,c.fechaIncorporacion.strftime('%d-%m-%Y'),body)
                    sheet.write(row,3,c.RFC,body)
                    sheet.write(row,4,c.banco,body)
                    sheet.write(row,5,c.tarjetahabiente,body)
                    sheet.write(row,6,c.numCuenta,body)
                    sheet.write(row,7,c.paginaWeb,body)
                    sheet.write(row,8,c.facebook,body)
                    sheet.write(row,9,c.instagram,body)
                    sheet.write(row,10,c.twitter,body)
                    sheet.write(row,11,c.evaluacionPromedio,body)
                    sheet.write(row,12,estatus,body)
                    sheet.write(row,13,c.codigoClub,body)
                    sheet.write(row,14,c.codigoRepresentante,body)
                    sheet.write(row,15,c.direccion,body)
                    sheet.write(row,16,c.telefono,body)
                    sheet.write(row,17,c.correo,body)
                    sheet.write(row,18,foto,body)
                    sheet.write(row,19,acepto,body)
                    sheet.write(row,20,fechaAcepto,body)
                wb.close()
                return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

def addClub(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            nombre = request.POST['nombre']
            fechaIncorporacion = request.POST['fechaIncorporacion']
            codigoClub = request.POST['codigoClub']
            codigoRepresentante = request.POST['codigoRepresentante']
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            correo = request.POST['correo']
            password = request.POST['password']
            foto = request.FILES['foto']
            mailUsado = False
            try:
                mailUsado = User.objects.get(email=correo)
            except User.DoesNotExist:
                mailUsado = False
            if not mailUsado:
                user = User.objects.create_user(username=correo,email=correo)
                user.set_password(password)
                user.save()
                repetido = False
                try:
                    repetido = Club.objects.get(user=user,nombre=nombre,fechaIncorporacion=fechaIncorporacion,codigoClub=codigoClub,codigoRepresentante=codigoRepresentante,direccion=direccion,telefono=telefono,correo=correo)
                except Club.DoesNotExist:
                    repetido = False
                if not repetido:
                    club = Club(user=user,nombre=nombre,fechaIncorporacion=fechaIncorporacion,codigoClub=codigoClub,codigoRepresentante=codigoRepresentante,direccion=direccion,telefono=telefono,correo=correo,foto=foto)
                    club.save()
                    return HttpResponseRedirect('/homeAdminClubes/')
                else:
                    error = u'Ya hay un club asignado a este user con la misma información.'
                    return render(request,'FitApp/errorClub.html',{'error':error})
            else:
                error = u'Ya hay un club registrado con este correo.'
                return render(request,'FitApp/errorClub.html',{'error':error})
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def editClubContrasena(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            clubID = request.POST['club']
            club = Club.objects.get(id=clubID)
            try:
                password = request.POST['password'] 
            except MultiValueDictKeyError:
                password = False
            try:
                confirmarPassword = request.POST['confirmarPassword'] 
            except MultiValueDictKeyError:
                confirmarPassword = False
            if password and confirmarPassword:
                if not password == confirmarPassword:
                    user = club.user
                    user.set_password(confirmarPassword)
                    user.save()
                    return HttpResponseRedirect('/homeAdminClubes/')
                else:
                    error = u'La contraseña nueva no debe ser la misma que la contraseña actual.'
                    return render(request,'FitApp/errorClub.html',{'error':error})
            else:
                error = u'Debe ingresar contraseña y confirmar contraseña.'
                return render(request,'FitApp/errorClub.html',{'error':error})
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def editClub(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            clubID = request.POST['club']
            club = Club.objects.get(id=clubID)
            nombre = request.POST['nombre']
            fechaIncorporacion = request.POST['fechaIncorporacion']
            try:
                RFC = request.POST['RFC']
            except MultiValueDictKeyError:
                RFC = '...'
            try:
                banco = request.POST['banco']
            except MultiValueDictKeyError:
                banco = '...'
            try:
                tarjetahabiente = request.POST['tarjetahabiente']
            except MultiValueDictKeyError:
                tarjetahabiente = '...'
            try:
                numCuenta = request.POST['numCuenta']
            except MultiValueDictKeyError:
                numCuenta = '...'
            try:
                paginaWeb = request.POST['paginaWeb']
            except MultiValueDictKeyError:
                paginaWeb = '...'
            try:
                facebook = request.POST['facebook']
            except MultiValueDictKeyError:
                facebook = '...'
            try:
                instagram = request.POST['instagram']
            except MultiValueDictKeyError:
                instagram = '...'
            try:
                twitter = request.POST['twitter']
            except MultiValueDictKeyError:
                twitter = '...'
            estatus = int(request.POST['estatus'])
            if estatus == 1:
                activado = True
            elif estatus == 0:
                activado = False
            try:
                codigoClub = request.POST['codigoClub']
            except MultiValueDictKeyError:
                codigoClub = '...'
            try:
                codigoRepresentante = request.POST['codigoRepresentante']
            except MultiValueDictKeyError:
                codigoRepresentante = '...'
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            correo = request.POST['correo']
            try:
                foto = request.FILES['foto']
            except MultiValueDictKeyError:
                foto = False
            club.nombre = nombre
            club.fechaIncorporacion = fechaIncorporacion
            club.RFC = RFC
            club.banco = banco
            club.tarjetahabiente = tarjetahabiente
            club.numCuenta = numCuenta
            club.paginaWeb = paginaWeb
            club.facebook = facebook
            club.instagram = instagram
            club.twitter = twitter
            club.activado = activado
            club.codigoClub = codigoClub
            club.codigoRepresentante = codigoRepresentante
            club.direccion = direccion
            club.telefono = telefono
            correoActual = club.correo
            if not correo == correoActual:
                club.correo = correo
                user = club.user
                user.username = correo
                user.email = correo
                user.save()
            club.save()
            if foto:
                fotoActual = club.foto.name
                if fotoActual == 'default/club.png':
                    club.foto = foto
                    club.save()
                else:
                    os.remove(club.foto.path)
                    club.foto = foto
                    club.save()
            return HttpResponseRedirect('/homeAdminClubes/')
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def deleteClub(request,club_id):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            club = Club.objects.get(id=club_id)
        except Club.DoesNotExist:
            club = False
        if club:
            fotoActual = club.foto.name
            if not fotoActual == 'default/club.png':
                os.remove(club.foto.path)
            club.delete()
            return HttpResponseRedirect('/homeAdminClubes/')
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def addActividadHorario(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            actividadClubID = request.POST['actividadClub']
            actividadClub = ActividadClub.objects.get(id=actividadClubID)
            horaInicio = request.POST['horaInicio']
            horaFin = request.POST['horaFin']
            try:
                lunes = request.POST['lunes']
            except MultiValueDictKeyError:
                lunes = False
            try:
                martes = request.POST['martes']
            except MultiValueDictKeyError:
                martes = False
            try:
                miercoles = request.POST['miercoles']
            except MultiValueDictKeyError:
                miercoles = False
            try:
                jueves = request.POST['jueves']
            except MultiValueDictKeyError:
                jueves = False
            try:
                viernes = request.POST['viernes']
            except MultiValueDictKeyError:
                viernes = False
            try:
                sabado = request.POST['sabado']
            except MultiValueDictKeyError:
                sabado = False
            try:
                domingo = request.POST['domingo']
            except MultiValueDictKeyError:
                domingo = False
            if not lunes and not martes and not miercoles and not jueves and not viernes and not sabado and not domingo:
                error = u'Debes seleccionar al menos un día de la semana para el horario a registrar.'
                return render(request,'FitApp/errorHorarioActividad.html',{'error':error,'club':actividadClub.sucursal.club})
            repetido = False
            try:
                repetido = ActividadHorario.objects.get(actividadClub=actividadClub,horaInicio=horaInicio,horaFin=horaFin,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo)
            except ActividadHorario.DoesNotExist:
                repetido = False
            if not repetido:
                actividadHorario = ActividadHorario(actividadClub=actividadClub,horaInicio=horaInicio,horaFin=horaFin,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo)
                actividadHorario.save()
                url = '/homeAdminClubes/'+str(actividadClub.sucursal.club.id)+'/Sucursales/'
                return HttpResponseRedirect(url)
            else:
                error = u'Ya hay un registro de horario para esta actividad con los mismos datos, favor de verificar.'
                return render(request,'FitApp/errorHorarioActividad.html',{'error':error,'club':actividadClub.sucursal.club})
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def editActividadHorario(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            actividadHorarioID = request.POST['actividadHorario']
            actividadHorario = ActividadHorario.objects.get(id=actividadHorarioID)
            horaInicio = request.POST['horaInicio']
            horaFin = request.POST['horaFin']
            try:
                lunes = request.POST['lunes']
            except MultiValueDictKeyError:
                lunes = False
            try:
                martes = request.POST['martes']
            except MultiValueDictKeyError:
                martes = False
            try:
                miercoles = request.POST['miercoles']
            except MultiValueDictKeyError:
                miercoles = False
            try:
                jueves = request.POST['jueves']
            except MultiValueDictKeyError:
                jueves = False
            try:
                viernes = request.POST['viernes']
            except MultiValueDictKeyError:
                viernes = False
            try:
                sabado = request.POST['sabado']
            except MultiValueDictKeyError:
                sabado = False
            try:
                domingo = request.POST['domingo']
            except MultiValueDictKeyError:
                domingo = False
            actividadHorario.horaInicio = horaInicio
            actividadHorario.horaFin = horaFin
            actividadHorario.lunes = lunes
            actividadHorario.martes = martes
            actividadHorario.miercoles = miercoles
            actividadHorario.jueves = jueves
            actividadHorario.viernes = viernes
            actividadHorario.sabado = sabado
            actividadHorario.domingo = domingo
            actividadHorario.save()
            url = '/homeAdminClubes/'+str(actividadHorario.actividadClub.sucursal.club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def deleteActividadHorario(request,actividadHorario_id):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            actividadHorario = ActividadHorario.objects.get(id=actividadHorario_id)
        except ActividadHorario.DoesNotExist:
            actividadHorario = False
        if actividadHorario:
            idClub = actividadHorario.actividadClub.sucursal.club.id
            actividadHorario.delete()
            url = '/homeAdminClubes/'+str(idClub)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def homeAdminClubSucursales(request,club_id):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            club = Club.objects.get(id=club_id)
        except Club.DoesNotExist:
            club = False
        if club:
            form = cropFotoClub(instance=club)
            dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
            try:
                sucursalesT = Sucursal.objects.filter(club=club)
            except Sucursal.DoesNotExist:
                sucursalesT = False
            try:
                sucursales = Sucursal.objects.filter(club=club).order_by('id')
            except Sucursal.DoesNotExist:
                sucursales = False
            page = request.GET.get('page', 1)
            paginator = Paginator(sucursales,50)
            try:
                sucursales = paginator.page(page)
            except PageNotAnInteger:
                sucursales = paginator.page(1)
            except EmptyPage:
                sucursales = paginator.page(paginator.num_pages)
            sucursalDatos = []
            sucursalFotos = []
            sucursalHorario = []
            sucursalCiudades = []
            clubServicios = []
            clubServiciosDisponbles = []
            clubActividades = []
            clubActividadesDisponibles = []
            sucursalRegistrosHorario = []
            sucursalMensualidadMasPorcentaje = []
            sucursalDiadMasPorcentaje = []
            if sucursales:
                for s in sucursales:
                    mensualidad = s.mensualidad
                    dia = s.dia
                    quincePorciento = (dia*15)/100
                    diaMasCincoPCT = dia + quincePorciento
                    cincoPorciento = (mensualidad*5)/100
                    mensualidadMasCincoPCT = mensualidad + cincoPorciento
                    sucursalMensualidadMasPorcentaje.append((s,mensualidadMasCincoPCT))
                    sucursalDiadMasPorcentaje.append((s,cincoPorciento))
                    try:
                        usuarios = Usuario.objects.filter(sucursal=s)
                    except Usuario.DoesNotExist:
                        usuarios = False
                    try:
                        fotos = Foto.objects.filter(sucursal=s)
                    except Foto.DoesNotExist:
                        fotos = False
                    if fotos:
                        sucursalFotos.append((s,fotos))
                    else:
                        sucursalFotos.append((s,None))
                    try:
                        horario = Horario.objects.get(sucursal=s)
                    except Horario.DoesNotExist:
                        horario = False
                    if horario:
                        sucursalHorario.append((s,horario))
                    else:
                        sucursalHorario.append((s,None))
                    if not usuarios and not fotos and not horario:
                        sucursalDatos.append((s,False))
                    else:
                        sucursalDatos.append((s,True))
                    if horario:
                        tipo = horario.tipo
                        if dias:
                            for d in dias:
                                if tipo == u'Corrido':
                                    try:
                                        registros = RegistroHorario.objects.get(sucursal=s,dia=d)
                                    except RegistroHorario.DoesNotExist:
                                        registros = False
                                    if registros:
                                        sucursalRegistrosHorario.append((s,d,tipo,registros))
                                    else:
                                        sucursalRegistrosHorario.append((s,d,tipo,None))
                                else:
                                    try:
                                        registros = RegistroHorario.objects.filter(sucursal=s,dia=d)
                                    except RegistroHorario.DoesNotExist:
                                        registros = False
                                    if registros:
                                        sucursalRegistrosHorario.append((s,d,tipo,registros))
                                    else:
                                        sucursalRegistrosHorario.append((s,d,tipo,None))
                    try:
                        ciudades = Ciudad.objects.filter(estado=s.estado)
                    except Ciudad.DoesNotExist:
                        ciudades = False
                    if ciudades:
                        sucursalCiudades.append((s,ciudades))
                    else:
                        sucursalCiudades.append((s,None))
                    try:
                        relacionesServ = ServicioClub.objects.filter(sucursal=s)
                    except ServicioClub.DoesNotExist:
                        relacionesServ = False
                    if relacionesServ:
                        clubServicios.append((s,relacionesServ))
                    else:
                        clubServicios.append((s,None))
                    try:
                        relacionesAct = ActividadClub.objects.filter(sucursal=s)
                    except ActividadClub.DoesNotExist:
                        relacionesAct = False
                    if relacionesAct:
                        clubActividades.append((s,relacionesAct))
                    else:
                        clubActividades.append((s,None))
            try:
                estados = Estado.objects.all()
            except Estado.DoesNotExist:
                estados = False
            try:
                actividadesHorarios = ActividadHorario.objects.all()
            except ActividadHorario.DoesNotExist:
                actividadesHorarios = False
            try:
                clubActividadesT = ActividadClub.objects.all()
            except ActividadClub.DoesNotExist:
                clubActividadesT = False
            clubActividadHorarios = []
            if clubActividadesT:
                for cAct in clubActividadesT:
                    try:
                        horarios = ActividadHorario.objects.filter(actividadClub=cAct)
                    except ActividadHorario.DoesNotExist:
                        horarios = False
                    numHorarios = 0
                    if horarios:
                        numHorarios = len(horarios)
                        clubActividadHorarios.append((cAct,horarios,numHorarios))
                    else:
                        clubActividadHorarios.append((cAct,None,numHorarios))
            try:
                servicios = Servicio.objects.all()
            except Servicio.DoesNotExist:
                servicios = False
            try:
                actividades = Actividad.objects.all()
            except Actividad.DoesNotExist:
                actividades
            if clubServicios:
                for sucursal,serviciosSel in clubServicios:
                    if not serviciosSel == None:
                        listaSSel = []
                        for s in serviciosSel:
                            listaSSel.append(s.servicio.id)
                        listaS = []
                        if servicios:
                            for s in servicios:
                                listaS.append(s.id)
                        serviciosDisponbles = [elem for elem in listaS if elem not in listaSSel]
                        serviciosDisponblesDos = []
                        if serviciosDisponbles:
                            for s in serviciosDisponbles:
                                try:
                                    srv = Servicio.objects.get(id=s)
                                except Servicio.DoesNotExist:
                                    srv = False
                                if srv:
                                    serviciosDisponblesDos.append(srv)
                        clubServiciosDisponbles.append((sucursal,serviciosDisponblesDos))
                    else:
                        clubServiciosDisponbles.append((sucursal,servicios))
            if clubActividades:
                for sucursal,actividadesSel in clubActividades:
                    if not actividadesSel == None:
                        listaASel = []
                        for a in actividadesSel:
                            listaASel.append(a.actividad.id)
                        listaA = []
                        if actividades:
                            for a in actividades:
                                listaA.append(a.id)
                        actividadesDisponibles = [elem for elem in listaA if elem not in listaASel]
                        actividadesDisponiblesDos = []
                        if actividadesDisponibles:
                            for a in actividadesDisponibles:
                                try:
                                    act = Actividad.objects.get(id=a)
                                except Actividad.DoesNotExist:
                                    act = False
                                if act:
                                    actividadesDisponiblesDos.append(act)
                        clubActividadesDisponibles.append((sucursal,actividadesDisponiblesDos))
                    else:
                        clubActividadesDisponibles.append((sucursal,actividades))
            try:
                registrosH = RegistroHorario.objects.all()
            except RegistroHorario.DoesNotExist:
                registrosH = False
            return render(request,'FitApp/homeAdminClubSucursales.html',{'form':form,'dias':dias,'club':club,'sucursales':sucursales,'sucursalesT':sucursalesT,'sucursalDatos':sucursalDatos,'sucursalFotos':sucursalFotos,'estados':estados,'sucursalCiudades':sucursalCiudades,'servicios':servicios,'actividades':actividades,'clubServicios':clubServicios,'clubServiciosDisponbles':clubServiciosDisponbles,'clubActividades':clubActividades,'clubActividadesDisponibles':clubActividadesDisponibles,'clubActividadHorarios':clubActividadHorarios,'actividadesHorarios':actividadesHorarios,'clubActividadesT':clubActividadesT,'sucursalHorario':sucursalHorario,'sucursalRegistrosHorario':sucursalRegistrosHorario,'registrosH':registrosH,'sucursalMensualidadMasPorcentaje':sucursalMensualidadMasPorcentaje})
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def homeAdminClubDetallesSucursales(request,sucursal_id):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            sucursales = Sucursal.objects.get(id=sucursal_id)
        except Sucursal.DoesNotExist:
            sucursales = False
        if sucursales:
            form = cropLogoSucursal(instance=sucursales)
            dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
            sucursalDatos = []
            sucursalFotos = []
            sucursalHorario = []
            sucursalCiudades = []
            clubServicios = []
            clubServiciosDisponbles = []
            clubActividades = []
            clubActividadesDisponibles = []
            sucursalRegistrosHorario = []
            sucursalMensualidadMasPorcentaje = []
            sucursalDiadMasPorcentaje = []
            mensualidad = sucursales.mensualidad
            cincoPorciento = (mensualidad*5)/100
            mensualidadMasCincoPCT = mensualidad + cincoPorciento
            mensualidadMasCincoPCT = round(mensualidadMasCincoPCT,2)
            sucursalMensualidadMasPorcentaje.append((sucursales,mensualidadMasCincoPCT))
            dia = sucursales.dia
            quincePorciento = (dia*15)/100
            diaMasCincoPCT = dia + quincePorciento
            diaMasCincoPCT = round(diaMasCincoPCT,2)
            sucursalDiadMasPorcentaje.append((sucursales,diaMasCincoPCT))
            try:
                usuarios = Usuario.objects.filter(sucursal=sucursales)
            except Usuario.DoesNotExist:
                usuarios = False
            try:
                fotos = Foto.objects.filter(sucursal=sucursales)
            except Foto.DoesNotExist:
                fotos = False
            if fotos:
                sucursalFotos.append((sucursales,fotos))
            else:
                sucursalFotos.append((sucursales,None))
            try:
                horario = Horario.objects.get(sucursal=sucursales)
            except Horario.DoesNotExist:
                horario = False
            if horario:
                sucursalHorario.append((sucursales,horario))
            else:
                sucursalHorario.append((sucursales,None))
            if not usuarios and not fotos and not horario:
                sucursalDatos.append((sucursales,False))
            else:
                sucursalDatos.append((sucursales,True))
            if horario:
                tipo = horario.tipo
                if dias:
                    for d in dias:
                        if tipo == u'Corrido':
                            try:
                                registros = RegistroHorario.objects.get(sucursal=sucursales,dia=d)
                            except RegistroHorario.DoesNotExist:
                                registros = False
                            if registros:
                                sucursalRegistrosHorario.append((sucursales,d,tipo,registros))
                            else:
                                sucursalRegistrosHorario.append((sucursales,d,tipo,None))
                        else:
                            try:
                                registros = RegistroHorario.objects.filter(sucursal=sucursales,dia=d)
                            except RegistroHorario.DoesNotExist:
                                registros = False
                            if registros:
                                sucursalRegistrosHorario.append((sucursales,d,tipo,registros))
                            else:
                                sucursalRegistrosHorario.append((sucursales,d,tipo,None))
            try:
                ciudades = Ciudad.objects.filter(estado=sucursales.estado)
            except Ciudad.DoesNotExist:
                ciudades = False
            if ciudades:
                sucursalCiudades.append((sucursales,ciudades))
            else:
                sucursalCiudades.append((sucursales,None))
            try:
                relacionesServ = ServicioClub.objects.filter(sucursal=sucursales)
            except ServicioClub.DoesNotExist:
                relacionesServ = False
            if relacionesServ:
                clubServicios.append((sucursales,relacionesServ))
            else:
                clubServicios.append((sucursales,None))
            try:
                relacionesAct = ActividadClub.objects.filter(sucursal=sucursales)
            except ActividadClub.DoesNotExist:
                relacionesAct = False
            if relacionesAct:
                clubActividades.append((sucursales,relacionesAct))
            else:
                clubActividades.append((sucursales,None))
            try:
                estados = Estado.objects.all()
            except Estado.DoesNotExist:
                estados = False
            try:
                actividadesHorarios = ActividadHorario.objects.all()
            except ActividadHorario.DoesNotExist:
                actividadesHorarios = False
            try:
                clubActividadesT = ActividadClub.objects.all()
            except ActividadClub.DoesNotExist:
                clubActividadesT = False
            clubActividadHorarios = []
            if clubActividadesT:
                for cAct in clubActividadesT:
                    try:
                        horarios = ActividadHorario.objects.filter(actividadClub=cAct)
                    except ActividadHorario.DoesNotExist:
                        horarios = False
                    numHorarios = 0
                    if horarios:
                        numHorarios = len(horarios)
                        clubActividadHorarios.append((cAct,horarios,numHorarios))
                    else:
                        clubActividadHorarios.append((cAct,None,numHorarios))
            try:
                servicios = Servicio.objects.all()
            except Servicio.DoesNotExist:
                servicios = False
            try:
                actividades = Actividad.objects.all()
            except Actividad.DoesNotExist:
                actividades
            if clubServicios:
                for sucursal,serviciosSel in clubServicios:
                    if not serviciosSel == None:
                        listaSSel = []
                        for s in serviciosSel:
                            listaSSel.append(s.servicio.id)
                        listaS = []
                        if servicios:
                            for s in servicios:
                                listaS.append(s.id)
                        serviciosDisponbles = [elem for elem in listaS if elem not in listaSSel]
                        serviciosDisponblesDos = []
                        if serviciosDisponbles:
                            for s in serviciosDisponbles:
                                try:
                                    srv = Servicio.objects.get(id=s)
                                except Servicio.DoesNotExist:
                                    srv = False
                                if srv:
                                    serviciosDisponblesDos.append(srv)
                        clubServiciosDisponbles.append((sucursal,serviciosDisponblesDos))
                    else:
                        clubServiciosDisponbles.append((sucursal,servicios))
            if clubActividades:
                for sucursal,actividadesSel in clubActividades:
                    if not actividadesSel == None:
                        listaASel = []
                        for a in actividadesSel:
                            listaASel.append(a.actividad.id)
                        listaA = []
                        if actividades:
                            for a in actividades:
                                listaA.append(a.id)
                        actividadesDisponibles = [elem for elem in listaA if elem not in listaASel]
                        actividadesDisponiblesDos = []
                        if actividadesDisponibles:
                            for a in actividadesDisponibles:
                                try:
                                    act = Actividad.objects.get(id=a)
                                except Actividad.DoesNotExist:
                                    act = False
                                if act:
                                    actividadesDisponiblesDos.append(act)
                        clubActividadesDisponibles.append((sucursal,actividadesDisponiblesDos))
                    else:
                        clubActividadesDisponibles.append((sucursal,actividades))
            try:
                registrosH = RegistroHorario.objects.all()
            except RegistroHorario.DoesNotExist:
                registrosH = False
            print clubServicios
            return render(request,'FitApp/homeAdminClubDetallesSucursales.html',{'dias':dias,'sucursales':sucursales,'sucursalDatos':sucursalDatos,'sucursalFotos':sucursalFotos,'estados':estados,'sucursalCiudades':sucursalCiudades,'servicios':servicios,'actividades':actividades,'clubServicios':clubServicios,'clubServiciosDisponbles':clubServiciosDisponbles,'clubActividades':clubActividades,'clubActividadesDisponibles':clubActividadesDisponibles,'clubActividadHorarios':clubActividadHorarios,'actividadesHorarios':actividadesHorarios,'clubActividadesT':clubActividadesT,'sucursalHorario':sucursalHorario,'sucursalRegistrosHorario':sucursalRegistrosHorario,'registrosH':registrosH,'sucursalMensualidadMasPorcentaje':sucursalMensualidadMasPorcentaje,'sucursalDiadMasPorcentaje':sucursalDiadMasPorcentaje,'form':form,'usuarios':usuarios})
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

class ReporteClubSucursales(View):
    def get(self,request,club_id):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                club = Club.objects.get(id=club_id)
            except Club.DoesNotExist:
                club = False
            if club:
                try:
                    sucursales = Sucursal.objects.filter(club=club)
                except Sucursal.DoesNotExist:
                    sucursales = False
                if sucursales:
                    filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                    wb = xlsxwriter.Workbook(filename)
                    center = wb.add_format({'align':'center'})
                    format = wb.add_format({'align':'center'})
                    format.set_text_wrap()
                    gris = wb.add_format({'font_color':'#9e9e9e'})
                    header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                    body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                    sheet = wb.add_worksheet(u'Sucursales')
                    sheet.write(0,0,u'ID',header)
                    sheet.write(0,1,u'NOMBRE',header)
                    sheet.write(0,2,u'DESCRIPCION',header)
                    sheet.write(0,3,u'TIPS',header)
                    sheet.write(0,4,u'EMAIL',header)
                    sheet.write(0,5,u'TELÉFONO',header)
                    sheet.write(0,6,u'ESTADO',header)
                    sheet.write(0,7,u'CIUDAD',header)
                    sheet.write(0,8,u'MUNICIPIO',header)
                    sheet.write(0,9,u'CALLE',header)
                    sheet.write(0,10,u'Nº EXT',header)
                    sheet.write(0,11,u'Nº INT',header)
                    sheet.write(0,12,u'COLONIA',header)
                    sheet.write(0,13,u'C.P.',header)
                    sheet.write(0,14,u'CALIFICACIÓN',header)
                    sheet.write(0,15,u'IBEACON',header)
                    sheet.write(0,16,u'MÁXIMO',header)
                    sheet.write(0,17,u'MÍNIMO',header)
                    sheet.write(0,18,u'ESTATUS',header)
                    sheet.write(0,19,u'FOTO',header)
                    sheet.write(0,20,u'SALDO',header)
                    sheet.write(0,21,u'MENSUALIDAD',header)
                    sheet.write(0,22,u'DÍA',header)
                    sheet.write(0,23,u'PORCENTAJE CLIENTE',header)
                    sheet.write(0,24,u'PORCENTAJE USER',header)
                    sheet.write(0,25,u'LATITUD',header)
                    sheet.write(0,26,u'LONGITUD',header)
                    sheet.set_column('A:A', 20)
                    sheet.set_column('B:B', 20)
                    sheet.set_column('C:C', 50)
                    sheet.set_column('D:D', 50)
                    sheet.set_column('E:E', 50)
                    sheet.set_column('F:F', 50)
                    sheet.set_column('G:G', 50)
                    sheet.set_column('H:H', 50)
                    sheet.set_column('I:I', 50)
                    sheet.set_column('J:J', 50)
                    sheet.set_column('K:K', 50)
                    sheet.set_column('L:L', 50)
                    sheet.set_column('M:M', 50)
                    sheet.set_column('N:N', 50)
                    sheet.set_column('O:O', 50)
                    sheet.set_column('P:P', 50)
                    sheet.set_column('Q:Q', 50)
                    sheet.set_column('R:R', 50)
                    sheet.set_column('S:S', 50)
                    sheet.set_column('T:T', 50)
                    sheet.set_column('U:U', 50)
                    sheet.set_column('V:V', 50)
                    sheet.set_column('W:W', 50)
                    sheet.set_column('X:X', 50)
                    sheet.set_column('Y:Y', 50)
                    sheet.set_column('Z:Z', 50)
                    sheet.set_column('AA:AA', 50)
                    sheet.protect()
                    row = 0
                    for s in sucursales:
                        row += 1
                        estatus = ''
                        if s.activa == True:
                            estatus = 'Activo'
                        else:
                            estatus = 'Inactivo'
                        foto = 'https://www.fitory.com/media/'+s.logo.name
                        sheet.write(row,0,s.id,body)
                        sheet.write(row,1,s.nombre,body)
                        sheet.write(row,2,s.descripcion,body)
                        sheet.write(row,3,s.tips,body)
                        sheet.write(row,4,s.correo,body)
                        sheet.write(row,5,s.telefono,body)
                        sheet.write(row,6,s.estado.nombre,body)
                        sheet.write(row,7,s.ciudad.nombre,body)
                        sheet.write(row,8,s.municipio,body)
                        sheet.write(row,9,s.calle,body)
                        sheet.write(row,10,s.numExt,body)
                        sheet.write(row,11,s.numInt,body)
                        sheet.write(row,12,s.colonia,body)
                        sheet.write(row,13,s.cp,body)
                        sheet.write(row,14,s.calificacion,body)
                        sheet.write(row,15,s.ibeacon,body)
                        sheet.write(row,16,s.maximo,body)
                        sheet.write(row,17,s.minimo,body)
                        sheet.write(row,18,estatus,body)
                        sheet.write(row,19,foto,body)
                        sheet.write(row,20,s.saldo,body)
                        sheet.write(row,21,s.mensualidad,body)
                        sheet.write(row,22,s.dia,body)
                        sheet.write(row,23,s.porcentajeCliente,body)
                        sheet.write(row,24,s.porcentajeUser,body)
                        sheet.write(row,25,s.latitud,body)
                        sheet.write(row,26,s.longitud,body)
                    wb.close()
                    return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

class ReporteSucursalServicios(View):
    def get(self,request,club_id,sucursal_id):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                club = Club.objects.get(id=club_id)
            except Club.DoesNotExist:
                club = False
            if club:
                try:
                    sucursal = Sucursal.objects.filter(id=sucursal_id,club=club)
                except Sucursal.DoesNotExist:
                    sucursal = False
                if sucursal:
                    try:
                        servicios = ServicioClub.objects.filter(sucursal=sucursal)
                    except ServicioClub.DoesNotExist:
                        servicios = False
                    if servicios:
                        filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                        wb = xlsxwriter.Workbook(filename)
                        center = wb.add_format({'align':'center'})
                        format = wb.add_format({'align':'center'})
                        format.set_text_wrap()
                        gris = wb.add_format({'font_color':'#9e9e9e'})
                        header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                        body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                        sheet = wb.add_worksheet(u'Servicios')
                        sheet.write(0,0,u'ID',header)
                        sheet.write(0,1,u'NOMBRE',header)
                        sheet.write(0,2,u'ICONO',header)
                        sheet.set_column('A:A', 20)
                        sheet.set_column('B:B', 20)
                        sheet.set_column('C:C', 50)
                        sheet.protect()
                        row = 0
                        for s in servicios:
                            row += 1
                            icono = 'https://www.fitory.com/media/'+s.servicio.icono.name
                            sheet.write(row,0,s.id,body)
                            sheet.write(row,1,s.servicio.nombre,body)
                            sheet.write(row,2,icono,body)
                        wb.close()
                        return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    else:
                        respuesta = 'Sin resultados.'
                        return HttpResponse(respuesta, content_type="text/plain")
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

class ReporteSucursalActividades(View):
    def get(self,request,club_id,sucursal_id):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                club = Club.objects.get(id=club_id)
            except Club.DoesNotExist:
                club = False
            if club:
                try:
                    sucursal = Sucursal.objects.filter(id=sucursal_id,club=club)
                except Sucursal.DoesNotExist:
                    sucursal = False
                if sucursal:
                    try:
                        actividades = ActividadClub.objects.filter(sucursal=sucursal)
                    except ActividadClub.DoesNotExist:
                        actividades = False
                    if actividades:
                        filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                        wb = xlsxwriter.Workbook(filename)
                        center = wb.add_format({'align':'center'})
                        format = wb.add_format({'align':'center'})
                        format.set_text_wrap()
                        gris = wb.add_format({'font_color':'#9e9e9e'})
                        header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                        body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                        sheet = wb.add_worksheet(u'Servicios')
                        sheet.write(0,0,u'ID',header)
                        sheet.write(0,1,u'NOMBRE',header)
                        sheet.write(0,2,u'ICONO',header)
                        sheet.set_column('A:A', 20)
                        sheet.set_column('B:B', 20)
                        sheet.set_column('C:C', 50)
                        sheet.protect()
                        row = 0
                        for a in actividades:
                            row += 1
                            icono = 'https://www.fitory.com/media/'+a.actividad.icono.name
                            sheet.write(row,0,a.id,body)
                            sheet.write(row,1,a.actividad.nombre,body)
                            sheet.write(row,2,icono,body)
                        wb.close()
                        return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    else:
                        respuesta = 'Sin resultados.'
                        return HttpResponse(respuesta, content_type="text/plain")
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

class ReporteSucursalActividadHorarios(View):
    def get(self,request,club_id,sucursal_id,actividad_id):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                club = Club.objects.get(id=club_id)
            except Club.DoesNotExist:
                club = False
            if club:
                try:
                    sucursal = Sucursal.objects.filter(id=sucursal_id,club=club)
                except Sucursal.DoesNotExist:
                    sucursal = False
                if sucursal:
                    try:
                        actividad = ActividadClub.objects.filter(id=actividad_id,sucursal=sucursal)
                    except ActividadClub.DoesNotExist:
                        actividad = False
                    if actividad:
                        try:
                            horarios = ActividadHorario.objects.filter(actividadClub=actividad)
                        except ActividadHorario.DoesNotExist:
                            horarios = False
                        if horarios:
                            filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                            wb = xlsxwriter.Workbook(filename)
                            center = wb.add_format({'align':'center'})
                            format = wb.add_format({'align':'center'})
                            format.set_text_wrap()
                            gris = wb.add_format({'font_color':'#9e9e9e'})
                            header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                            body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                            sheet = wb.add_worksheet(u'Horarios')
                            sheet.write(0,0,u'ID',header)
                            sheet.write(0,1,u'HORA INICIO',header)
                            sheet.write(0,2,u'HORA FIN',header)
                            sheet.write(0,3,u'LUNES',header)
                            sheet.write(0,4,u'MARTES',header)
                            sheet.write(0,5,u'MIÉRCOLES',header)
                            sheet.write(0,6,u'JUEVES',header)
                            sheet.write(0,7,u'VIERNES',header)
                            sheet.write(0,8,u'SÁBADO',header)
                            sheet.write(0,9,u'DOMINGO',header)
                            sheet.set_column('A:A', 20)
                            sheet.set_column('B:B', 20)
                            sheet.set_column('C:C', 20)
                            sheet.set_column('D:D', 20)
                            sheet.set_column('E:E', 20)
                            sheet.set_column('F:F', 20)
                            sheet.set_column('G:G', 20)
                            sheet.set_column('H:H', 20)
                            sheet.set_column('I:I', 20)
                            sheet.set_column('J:J', 20)
                            sheet.protect()
                            row = 0
                            for h in horarios:
                                row += 1
                                lunes = ''
                                if h.lunes == True:
                                    lunes = 'Si'
                                else:
                                    lunes = 'No'
                                lmartes= ''
                                if h.martes == True:
                                    martes = 'Si'
                                else:
                                    martes = 'No'
                                miercoles= ''
                                if h.miercoles == True:
                                    miercoles = 'Si'
                                else:
                                    miercoles = 'No'
                                jueves= ''
                                if h.jueves == True:
                                    jueves = 'Si'
                                else:
                                    jueves = 'No'
                                viernes = ''
                                if h.viernes == True:
                                    viernes = 'Si'
                                else:
                                    viernes = 'No'
                                sabado = ''
                                if h.sabado == True:
                                    sabado = 'Si'
                                else:
                                    sabado = 'No'
                                domingo= ''
                                if h.domingo== True:
                                    domingo= 'Si'
                                else:
                                    domingo= 'No'
                                inicio = h.horaInicio.strftime('%I:%M %p')
                                final = h.horaFin.strftime('%I:%M %p')
                                sheet.write(row,0,h.id,body)
                                sheet.write(row,1,inicio,body)
                                sheet.write(row,2,final,body)
                                sheet.write(row,3,lunes,body)
                                sheet.write(row,4,martes,body)
                                sheet.write(row,5,miercoles,body)
                                sheet.write(row,6,jueves,body)
                                sheet.write(row,7,viernes,body)
                                sheet.write(row,8,sabado,body)
                                sheet.write(row,9,domingo,body)
                            wb.close()
                            return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                        else:
                            respuesta = 'Sin resultados.'
                            return HttpResponse(respuesta, content_type="text/plain")
                    else:
                        respuesta = 'Sin resultados.'
                        return HttpResponse(respuesta, content_type="text/plain")
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

class ReporteSucursalHorario(View):
    def get(self,request,club_id,sucursal_id):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                club = Club.objects.get(id=club_id)
            except Club.DoesNotExist:
                club = False
            if club:
                try:
                    sucursal = Sucursal.objects.filter(id=sucursal_id,club=club)
                except Sucursal.DoesNotExist:
                    sucursal = False
                if sucursal:
                    try:
                        horario = Horario.objects.get(sucursal=sucursal)
                    except Horario.DoesNotExist:
                        horario = False
                    sucursalRegistrosHorario = []
                    if horario:
                        tipo = horario.tipo
                        dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
                        if dias:
                            for d in dias:
                                if tipo == u'Corrido':
                                    try:
                                        registros = RegistroHorario.objects.get(sucursal=sucursal,dia=d)
                                    except RegistroHorario.DoesNotExist:
                                        registros = False
                                    if registros:
                                        sucursalRegistrosHorario.append((sucursal,d,tipo,registros))
                                    else:
                                        sucursalRegistrosHorario.append((sucursal,d,tipo,None))
                                else:
                                    try:
                                        registros = RegistroHorario.objects.filter(sucursal=sucursal,dia=d)
                                    except RegistroHorario.DoesNotExist:
                                        registros = False
                                    if registros:
                                        sucursalRegistrosHorario.append((sucursal,d,tipo,registros))
                                    else:
                                        sucursalRegistrosHorario.append((sucursal,d,tipo,None))
                        if sucursalRegistrosHorario:
                            if horario.tipo == 'Corrido':
                                filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                                wb = xlsxwriter.Workbook(filename)
                                center = wb.add_format({'align':'center'})
                                format = wb.add_format({'align':'center'})
                                format.set_text_wrap()
                                gris = wb.add_format({'font_color':'#9e9e9e'})
                                header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                                body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                                sheet = wb.add_worksheet(u'Horario')
                                sheet.write(0,0,u'DÍA',header)
                                sheet.write(0,1,u'APERTURA',header)
                                sheet.write(0,2,u'CIERRE',header)
                                sheet.set_column('A:A', 20)
                                sheet.set_column('B:B', 20)
                                sheet.set_column('C:C', 20)
                                sheet.protect()
                                row = 0
                                for suc,dia,tipo,registros in sucursalRegistrosHorario:
                                    row += 1
                                    sheet.write(row,0,dia,body)
                                    if registros:
                                        sheet.write(row,1,registros.apertura.strftime('%I:%M %p'),body)
                                        sheet.write(row,2,registros.cierre.strftime('%I:%M %p'),body)
                                    else:
                                        sheet.write(row,1,u'-',body)
                                        sheet.write(row,2,u'-',body)
                                wb.close()
                                return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                            else:
                                filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                                wb = xlsxwriter.Workbook(filename)
                                center = wb.add_format({'align':'center'})
                                format = wb.add_format({'align':'center'})
                                format.set_text_wrap()
                                gris = wb.add_format({'font_color':'#9e9e9e'})
                                header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                                body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                                sheet = wb.add_worksheet(u'Horario')
                                sheet.write(0,0,u'DÍA',header)
                                sheet.write(0,1,u'APERTUTA',header)
                                sheet.write(0,2,u'CIERRE',header)
                                sheet.write(0,3,u'APERTURA',header)
                                sheet.write(0,4,u'CIERRE',header)
                                sheet.set_column('A:A', 20)
                                sheet.set_column('B:B', 20)
                                sheet.set_column('C:C', 20)
                                sheet.set_column('D:D', 20)
                                sheet.set_column('E:E', 20)
                                sheet.protect()
                                row = 0
                                for suc,dia,tipo,registros in sucursalRegistrosHorario:
                                    row += 1
                                    sheet.write(row,0,dia,body)
                                    if registros:
                                        reg1 = registros[0]
                                        reg2 = registros[1]
                                        sheet.write(row,1,reg1.apertura.strftime('%I:%M %p'),body)
                                        sheet.write(row,2,reg1.cierre.strftime('%I:%M %p'),body)
                                        sheet.write(row,3,reg2.apertura.strftime('%I:%M %p'),body)
                                        sheet.write(row,4,reg2.cierre.strftime('%I:%M %p'),body)
                                    else:
                                        sheet.write(row,1,u'-',body)
                                        sheet.write(row,2,u'-',body)
                                        sheet.write(row,3,u'-',body)
                                        sheet.write(row,4,u'-',body)
                                wb.close()
                                return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                        else:
                            respuesta = 'Sin resultados.'
                            return HttpResponse(respuesta, content_type="text/plain")
                    else:
                        respuesta = 'Sin resultados.'
                        return HttpResponse(respuesta, content_type="text/plain")
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

class ReporteSucursalFotos(View):
    def get(self,request,club_id,sucursal_id):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                club = Club.objects.get(id=club_id)
            except Club.DoesNotExist:
                club = False
            if club:
                try:
                    sucursal = Sucursal.objects.filter(id=sucursal_id,club=club)
                except Sucursal.DoesNotExist:
                    sucursal = False
                if sucursal:
                    try:
                        fotos = Foto.objects.filter(sucursal=sucursal)
                    except Foto.DoesNotExist:
                        fotos = False
                    if fotos:
                        filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                        wb = xlsxwriter.Workbook(filename)
                        center = wb.add_format({'align':'center'})
                        format = wb.add_format({'align':'center'})
                        format.set_text_wrap()
                        gris = wb.add_format({'font_color':'#9e9e9e'})
                        header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                        body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                        sheet = wb.add_worksheet(u'Fotos')
                        sheet.write(0,0,u'ID',header)
                        sheet.write(0,1,u'FOTO',header)
                        sheet.set_column('A:A', 20)
                        sheet.set_column('B:B', 80)
                        sheet.protect()
                        row = 0
                        for f in fotos:
                            row += 1
                            foto = 'https://www.fitory.com/media/'+f.archivo.name
                            sheet.write(row,0,f.id,body)
                            sheet.write(row,1,foto,body)
                        wb.close()
                        return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    else:
                        respuesta = 'Sin resultados.'
                        return HttpResponse(respuesta, content_type="text/plain")
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

class ReporteSucursalUsuarios(View):
    def get(self,request,club_id,sucursal_id):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                club = Club.objects.get(id=club_id)
            except Club.DoesNotExist:
                club = False
            if club:
                try:
                    sucursal = Sucursal.objects.filter(id=sucursal_id,club=club)
                except Sucursal.DoesNotExist:
                    sucursal = False
                if sucursal:
                    try:
                        usuarios = Usuario.objects.filter(sucursal=sucursal)
                    except Usuario.DoesNotExist:
                        usuarios = False
                    if usuarios:
                        filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                        wb = xlsxwriter.Workbook(filename)
                        center = wb.add_format({'align':'center'})
                        format = wb.add_format({'align':'center'})
                        format.set_text_wrap()
                        gris = wb.add_format({'font_color':'#9e9e9e'})
                        header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                        body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                        sheet = wb.add_worksheet(u'Usuarios')
                        sheet.write(0,0,u'ID',header)
                        sheet.write(0,1,u'NOMBRE',header)
                        sheet.write(0,2,u'EMAIL',header)
                        sheet.write(0,3,u'ACEPTÓ TYC',header)
                        sheet.write(0,4,u'FECHA TYC',header)
                        sheet.write(0,5,u'ESTATUS',header)
                        sheet.set_column('A:A', 20)
                        sheet.set_column('B:B', 40)
                        sheet.set_column('C:C', 40)
                        sheet.set_column('D:D', 20)
                        sheet.set_column('E:E', 20)
                        sheet.set_column('F:F', 20)
                        sheet.protect()
                        row = 0
                        for u in usuarios:
                            row += 1
                            estatus = ''
                            if u.activo == True:
                                estatus = 'Activo'
                            else:
                                estatus = 'Inactivo'
                            acepto = ''
                            if u.Legal == True:
                                acepto = 'Si'
                            else:
                                acepto = 'No'
                            fechaAcepto = ''
                            if u.fechaLegal:
                                fechaAcepto = u.fechaLegal.strftime('%d-%m-%Y')
                            else:
                                fechaAcepto = '-'
                            sheet.write(row,0,u.id,body)
                            sheet.write(row,1,u.nombre,body)
                            sheet.write(row,2,u.user.email,body)
                            sheet.write(row,3,acepto,body)
                            sheet.write(row,4,fechaAcepto,body)
                            sheet.write(row,5,estatus,body)
                        wb.close()
                        return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    else:
                        respuesta = 'Sin resultados.'
                        return HttpResponse(respuesta, content_type="text/plain")
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

def addSucursal(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            clubID = request.POST['club']
            club = Club.objects.get(id=clubID)
            nombre = request.POST['nombre']
            try:
                descripcion = request.POST['descripcion']
            except MultiValueDictKeyError:
                descripcion = None
            try:
                tips = request.POST['tips']
            except MultiValueDictKeyError:
                tips = None
            correo = request.POST['correo']
            telefono = request.POST['telefono']
            estadoID = request.POST['estado']
            estado = Estado.objects.get(id=estadoID)
            ciudadID = request.POST['ciudad']
            ciudad = Ciudad.objects.get(id=ciudadID,estado=estado)
            municipio = request.POST['municipio']
            calle = request.POST['calle']
            numExt = request.POST['numExt']
            try:
                numInt = request.POST['numInt']
            except MultiValueDictKeyError:
                numInt = '...'
            colonia = request.POST['colonia']
            cp = request.POST['cp']
            try:
                logo = request.FILES['logo']
            except MultiValueDictKeyError:
                logo = False
            try:
                latitud = request.POST['latitud']
            except MultiValueDictKeyError:
                latitud = '25.4595197'
            try:
                longitud = request.POST['longitud']
            except MultiValueDictKeyError:
                longitud = '-100.9819936'
            try:
                servicios = request.POST.getlist('servicios')
            except MultiValueDictKeyError:
                servicios = False
            try:
                actividades = request.POST.getlist('actividades')
            except MultiValueDictKeyError:
                actividades = False
            mensualidad = request.POST['mensualidad']
            repetido = False
            try:
                repetido = Sucursal.objects.get(club=club,nombre=nombre,correo=correo,telefono=telefono,estado=estado,ciudad=ciudad,municipio=municipio,calle=calle,numExt=numExt,numInt=numInt,colonia=colonia,cp=cp,latitud=latitud,longitud=longitud)
            except Sucursal.DoesNotExist:
                repetido = False
            if not repetido:
                if logo:
                    sucursal = Sucursal(club=club,nombre=nombre,descripcion=descripcion,tips=tips,correo=correo,telefono=telefono,estado=estado,ciudad=ciudad,municipio=municipio,calle=calle,numExt=numExt,numInt=numInt,colonia=colonia,cp=cp,logo=logo,latitud=latitud,longitud=longitud,mensualidad=mensualidad)
                    sucursal.save()
                else:
                    sucursal = Sucursal(club=club,nombre=nombre,descripcion=descripcion,tips=tips,correo=correo,telefono=telefono,estado=estado,ciudad=ciudad,municipio=municipio,calle=calle,numExt=numExt,numInt=numInt,colonia=colonia,cp=cp,latitud=latitud,longitud=longitud,mensualidad=mensualidad)
                    sucursal.save()
                if servicios:
                    for s in servicios:
                        try:
                            servicio = Servicio.objects.get(id=s)
                        except Servicio.DoesNotExist:
                            servicio = False
                        if servicio:
                            try:
                                relacion = ServicioClub.objects.get(sucursal=sucursal,servicio=servicio)
                            except ServicioClub.DoesNotExist:
                                relacion = False
                            if not relacion:
                                relacionNueva = ServicioClub(sucursal=sucursal,servicio=servicio)
                                relacionNueva.save()
                if actividades:
                    for a in actividades:
                        try:
                            actividad = Actividad.objects.get(id=a)
                        except Actividad.DoesNotExist:
                            actividad = False
                        if actividad:
                            try:
                                relacion = ActividadClub.objects.get(sucursal=sucursal,actividad=actividad)
                            except ActividadClub.DoesNotExist:
                                relacion = False
                            if not relacion:
                                relacionNueva = ActividadClub(sucursal=sucursal,actividad=actividad)
                                relacionNueva.save()
                idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(club.id)
                namePlan = "Mensualidad Sucursal "+sucursal.nombre+", Club "+club.nombre
                amountCentavos = int(float(mensualidad))*100
                try:
                    planConektaSucursal = conekta.Plan.find(idPlan)
                except:
                    planConektaSucursal = False
                if not planConektaSucursal:
                    conekta.Plan.create({
                        "id":idPlan,
                        "name":namePlan,
                        "amount":amountCentavos,
                        "currency":"MXN",
                        "interval":"month",
                        "frequency":1,
                        "trial_period_days":0,
                        "expiry_count":1
                    })
                url = '/homeAdminClubes/'+str(club.id)+'/Sucursales/'
                return HttpResponseRedirect(url)
            else:
                error = u'Ya existe una sucursal con la misma información'
                return render(request,'FitApp/errorSucursal.html',{'error':error,'club':club})
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def editSucursal(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            nombre = request.POST['nombre']
            try:
                descripcion = request.POST['descripcion']
            except MultiValueDictKeyError:
                descripcion = None
            try:
                tips = request.POST['tips']
            except MultiValueDictKeyError:
                tips = None
            correo = request.POST['correo']
            telefono = request.POST['telefono']
            estadoID = request.POST['estado']
            # estado = Estado.objects.get(id=estadoID)
            # ciudadID = request.POST['ciudad']
            # ciudad = Ciudad.objects.get(id=ciudadID,estado=estado)
            municipio = request.POST['municipio']
            calle = request.POST['calle']
            numExt = request.POST['numExt']
            try:
                numInt = request.POST['numInt']
            except MultiValueDictKeyError:
                numInt = '...'
            diaGratis = request.POST['diaGratis']
            colonia = request.POST['colonia']
            cp = request.POST['cp']
            try:
                logo = request.FILES['logo']
            except MultiValueDictKeyError:
                logo = False
            try:
                latitud = request.POST['latitud']
            except MultiValueDictKeyError:
                latitud = '...'
            try:
                longitud = request.POST['longitud']
            except MultiValueDictKeyError:
                longitud = '...'
            # try:
            #     servicios = request.POST.getlist('servicios')
            # except MultiValueDictKeyError:
            #     servicios = False
            # try:
            #     actividades = request.POST.getlist('actividades')
            # except MultiValueDictKeyError:
            #     actividades = False
            try:
                ibeacon = request.POST['ibeacon']
            except MultiValueDictKeyError:
                ibeacon = None
            maximo = request.POST['maximo']
            minimo = request.POST['minimo']
            mensualidad = request.POST['mensualidad']
            dia = request.POST['dia']
            try:
                estatus = request.POST['estatus']
            except MultiValueDictKeyError:
                estatus = False
            print estatus
            if estatus == "True":
                sucursal.activa = True
            else:
                sucursal.activa = False
            sucursal.nombre = nombre
            sucursal.descripcion = descripcion
            sucursal.tips = tips
            correoActual = sucursal.correo
            if not correo == correoActual:
                sucursal.correo = correo
                sucursal.save()
            sucursal.telefono = telefono
            # sucursal.estado = estado
            sucursal.municipio = municipio
            sucursal.calle = calle
            sucursal.numExt = numExt
            sucursal.numInt = numInt
            sucursal.colonia = colonia
            sucursal.cp = cp
            sucursal.latitud = latitud
            sucursal.longitud = longitud
            sucursal.ibeacon = ibeacon
            sucursal.maximo = maximo
            sucursal.minimo = minimo
            sucursal.mensualidad = mensualidad
            sucursal.dia = dia
            sucursal.diasPruebas = diaGratis
            sucursal.save()
            idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id)
            namePlan = "Mensualidad Sucursal "+nombre+", Club "+sucursal.club.nombre
            amountCentavos = int(float(mensualidad))*100
            try:
                planConektaSucursal = conekta.Plan.find(idPlan)
            except:
                planConektaSucursal = False
            if planConektaSucursal:
                planConektaSucursal.update({
                    "name":namePlan,
                    "amount":amountCentavos
                })
            # if logo:
            #     logoActual = sucursal.logo.name
            #     if logoActual == 'default/logo.jpg':
            #         sucursal.logo = logo
            #         sucursal.save()
            #     else:
            #         os.remove(sucursal.logo.path)
            #         sucursal.logo = logo
            #         sucursal.save() d
            try:
                horario = Horario.objects.get(sucursal=sucursal)
            except Horario.DoesNotExist:
                horario = False
            if horario:
                numDiasActual = horario.numDias
                mensualidad = Dec(mensualidad)
                calculo = (mensualidad)/(numDiasActual*4)
                calculoComision = (10*calculo)/100
                totalDia = calculo + calculoComision
                sucursal.dia = Dec(totalDia)
                sucursal.save()
            idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id)
            namePlan = "Mensualidad Sucursal "+sucursal.nombre+", Club "+sucursal.club.nombre
            amountCentavos = int(float(mensualidad))*100
            try:
                planConektaSucursal = conekta.Plan.find(idPlan)
            except:
                planConektaSucursal = False
            if not planConektaSucursal:
                conekta.Plan.create({
                    "id":idPlan,
                    "name":namePlan,
                    "amount":amountCentavos,
                    "currency":"MXN",
                    "interval":"month",
                    "frequency":1,
                    "trial_period_days":0,
                    "expiry_count":1
                })
            else:
                planConektaSucursal.update({
                    "id": idPlan,
                    "name": namePlan,
                    "amount": amountCentavos
                })
            url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def editEstatusSucursal(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            estatus = int(request.POST['estatus'])
            if estatus == 1:
                sucursal.activa = True
            else:
                sucursal.activa = False
            sucursal.save()
            url = '/homeAdminClubes/'+str(sucursal.club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def CambiarLogoSucursalAdmin(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                logo = request.FILES['logo']
            except MultiValueDictKeyError:
                logo = False
            if logo:
                logoActual = sucursal.logo.name
                if logoActual == 'default/logo.jpg':
                    sucursal.logo = logo
                    sucursal.save()
                else:
                    os.remove(sucursal.logo.path)
                    sucursal.logo = logo
                    sucursal.save()
            sucursal.save()
            url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def ServiciosSucursalAdmin(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                servicios = request.POST.getlist('servicios')
            except MultiValueDictKeyError:
                servicios = False
            serviciosSeleccionados = []
            serviciosNoSeleccionados = []
            if servicios:
                for s in servicios:
                    try:
                        servicio = Servicio.objects.get(id=s)
                    except Servicio.DoesNotExist:
                        servicio = False
                    if servicio:
                        serviciosSeleccionados.append(servicio.id)
                        try:
                            relacion = ServicioClub.objects.get(sucursal=sucursal,servicio=servicio)
                        except ServicioClub.DoesNotExist:
                            relacion = False
                        if not relacion:
                            relacionNueva = ServicioClub(sucursal=sucursal,servicio=servicio)
                            relacionNueva.save()
                serviciosTodos = []
                try:
                    serviciosT = Servicio.objects.all()
                except Servicio.DoesNotExist:
                    serviciosT = False
                if serviciosT:
                    for s in serviciosT:
                        serviciosTodos.append(s.id)
                serviciosNoSeleccionados = [elem for elem in serviciosTodos if elem not in serviciosSeleccionados]
                if serviciosNoSeleccionados:
                    for s in serviciosNoSeleccionados:
                        try:
                            servicio = Servicio.objects.get(id=s)
                        except Servicio.DoesNotExist:
                            servicio = False
                        if servicio:
                            try:
                                relacion = ServicioClub.objects.get(sucursal=sucursal,servicio=servicio)
                            except ServicioClub.DoesNotExist:
                                relacion = False
                            if relacion:
                                relacion.delete()
            else:
                try:
                    relaciones = ServicioClub.objects.filter(sucursal=sucursal)
                except ServicioClub.DoesNotExist:
                    relaciones = False
                if relaciones:
                    for r in relaciones:
                        r.delete()
            url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def ActividadesSucursalAdmin(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                actividades = request.POST.getlist('actividades')
            except MultiValueDictKeyError:
                actividades = False
            actividadesSeleccionadas = []
            actividadesNoSeleccionadas = []
            if actividades:
                for a in actividades:
                    try:
                        actividad = Actividad.objects.get(id=a)
                    except Actividad.DoesNotExist:
                        actividad = False
                    if actividad:
                        actividadesSeleccionadas.append(actividad.id)
                        try:
                            relacion = ActividadClub.objects.get(sucursal=sucursal,actividad=actividad)
                        except ActividadClub.DoesNotExist:
                            relacion = False
                        if not relacion:
                            relacionNueva = ActividadClub(sucursal=sucursal,actividad=actividad)
                            relacionNueva.save()
                actividadesTodas = []
                try:
                    actividadesT = Actividad.objects.all()
                except Actividad.DoesNotExist:
                    actividadesT = False
                if actividadesT:
                    for a in actividadesT:
                        actividadesTodas.append(a.id)
                actividadesNoSeleccionadas = [elem for elem in actividadesTodas if elem not in actividadesSeleccionadas]
                if actividadesNoSeleccionadas:
                    for a in actividadesNoSeleccionadas:
                        try:
                            actividad = Actividad.objects.get(id=a)
                        except Actividad.DoesNotExist:
                            actividad = False
                        if actividad:
                            try:
                                relacion = ActividadClub.objects.get(sucursal=sucursal,actividad=actividad)
                            except ActividadClub.DoesNotExist:
                                relacion = False
                            if relacion:
                                relacion.delete()
            else:
                try:
                    relaciones = ActividadClub.objects.filter(sucursal=sucursal)
                except ActividadClub.DoesNotExist:
                    relaciones = False
                if relaciones:
                    for r in relaciones:
                        r.delete()
            url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def recortarFotoSucursalFormulario(request,club_id,sucursal_id):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            club = Club.objects.get(id=club_id)
        except Club.DoesNotExist:
            club = False
        if club:
            try:
                sucursal = Sucursal.objects.get(id=sucursal_id,club=club)
            except Sucursal.DoesNotExist:
                sucursal = False
            if sucursal:
                form = cropLogoSucursal(instance=sucursal)
                return render(request,'FitApp/homeAdminClubSucursalRecortarFoto.html',{'club':club,'sucursal':sucursal,'form':form})
            else:
                url = '/homeAdminClubes/'+str(club.id)+'/Sucursales/'
                return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def recortarFotoSucursal(request):
    if request.user.is_staff and request.user.is_authenticated:
        sucursalID = request.POST['sucursal']
        sucursal = Sucursal.objects.get(id=sucursalID)
        form = cropLogoSucursal(instance=sucursal)
        if request.method == "POST":
            form = cropLogoSucursal(request.POST,request.FILES,instance=sucursal)
            if form.is_valid():
                thumbnailer = get_thumbnailer(sucursal.logo)
                thumbnailer.delete_thumbnails()
                logo = form.cleaned_data['logo']
                if logo:
                    sucursal.logo = logo
                    sucursal.logocrop = 0
                logocrop = form.cleaned_data['logocrop']
                sucursal.logocrop = logocrop
                sucursal.save()
                thumbnail_url = get_thumbnailer(sucursal.logo).get_thumbnail({'size': (200, 200),'box': sucursal.logocrop,'crop': True,'detail': True,}).url
                cropURL = thumbnail_url
                sucursal.cropURL = cropURL
                sucursal.save()
                url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
                return HttpResponseRedirect(url)
            else:
                url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
                return HttpResponseRedirect(url)
        else:
            url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
            return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect('/loginAdmin/')

def deleteSucursal(request,sucursal_id):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            sucursal = Sucursal.objects.get(id=sucursal_id)
        except Sucursal.DoesNotExist:
            sucursal = False
        if sucursal:
            club = sucursal.club
            logoActual = sucursal.logo.name
            if not logoActual == 'default/logo.jpg':
                os.remove(sucursal.logo.path)
            idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id)
            try:
                planConekta = conekta.Plan.find(idPlan)
            except:
                planConekta = False
            if planConekta:
                planConekta.delete()
            try:
                fotos = Foto.objects.filter(sucursal=sucursal)
            except Foto.DoesNotExist:
                fotos = False
            if fotos:
                for f in fotos:
                    os.remove(f.archivo.path)
                    f.delete()
            try:
                usuarios = Usuario.objects.filter(sucursal=sucursal)
            except Usuario.DoesNotExist:
                usuarios = False
            if usuarios:
                for u in usuarios:
                    user = u.user
                    user.delete()
                    u.delete()
            sucursal.delete()
            url = '/homeAdminClubes/'+str(club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        return HttpResponseRedirect('/loginAdmin/')

def addHorarioSucursal(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            repetido = False
            errores = []
            try:
                repetido = Horario.objects.get(sucursal=sucursal)
            except Horario.DoesNotExist:
                repetido = False
            if not repetido:
                lunes = False
                martes = False
                miercoles = False
                jueves = False
                viernes = False
                sabado = False
                domingo = False
                if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                    error = 'Debe seleccionar al menos un día en el horario.'
                    return render(request,'FitApp/errorHorarioSucursal.html',{'error':error,'club':sucursal.club})
                else:
                    if lunesCheck:
                        lunes = True
                    else:
                        lunes = False
                    if martesCheck:
                        martes = True
                    else:
                        martes = False
                    if miercolesCheck:
                        miercoles = True
                    else:
                        miercoles = False
                    if juevesCheck:
                        jueves = True
                    else:
                        jueves = False
                    if viernesCheck:
                        viernes = True
                    else:
                        viernes = False
                    if sabadoCheck:
                        sabado = True
                    else:
                        sabado = False
                    if domingoCheck:
                        domingo = True
                    else:
                        domingo = False
                    tipoHorario = int(request.POST['tipoHorario'])
                    tipo = ''
                    if tipoHorario == 1:
                        tipo = u'Corrido'
                    else:
                        tipo = u'Mixto'
                    horario = Horario(sucursal=sucursal,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo,numDias=numDias,tipo=tipo)
                    horario.save()
                    if lunes:
                        dia = u'Lunes'
                        apertura = request.POST['lunesA']
                        cierre = request.POST['lunesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Lunes con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if martes:
                        dia = u'Martes'
                        apertura = request.POST['martesA']
                        cierre = request.POST['martesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Martes con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if miercoles:
                        dia = u'Miércoles'
                        apertura = request.POST['miercolesA']
                        cierre = request.POST['miercolesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Miércoles con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if jueves:
                        dia = u'Jueves'
                        apertura = request.POST['juevesA']
                        cierre = request.POST['juevesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Jueves con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if viernes:
                        dia = u'Viernes'
                        apertura = request.POST['viernesA']
                        cierre = request.POST['viernesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Viernes con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if sabado:
                        dia = u'Sábado'
                        apertura = request.POST['sabadoA']
                        cierre = request.POST['sabadoC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Sábado con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if domingo:
                        dia = u'Domingo'
                        apertura = request.POST['domingoA']
                        cierre = request.POST['domingoC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Domingo con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                if not errores:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    numDiasActual = horarioSuc.numDias
                    mensualidad = sucursal.mensualidad
                    calculo = (mensualidad)/(numDiasActual*4)
                    calculoComision = (10*calculo)/100
                    totalDia = calculo + calculoComision
                    sucursal.dia = Dec(totalDia)
                    sucursal.save()
                    url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
                    return HttpResponseRedirect(url)
                else:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    horarioSuc.delete()
                    error = 'Ha ocurrido uno o más errores al momento de registrar el horario, favor de revisarlos.'
                    return render(request,'FitApp/errorHorarioSucursalVarios.html',{'error':error,'errores':json.dumps(errores),'club':horarioSuc.sucursal.club})
            else:
                error = 'Esta sucursal ya tiene un horario, registrado, si quieres editarlo usa el formulario de edición.'
                return render(request,'FitApp/errorHorarioSucursal.html',{'error':error,'club':sucursal.club})
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def addHorarioMixtoSucursal(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            repetido = False
            errores = []
            try:
                repetido = Horario.objects.get(sucursal=sucursal)
            except Horario.DoesNotExist:
                repetido = False
            if not repetido:
                lunes = False
                martes = False
                miercoles = False
                jueves = False
                viernes = False
                sabado = False
                domingo = False
                if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                    error = 'Debe seleccionar al menos un día en el horario.'
                    return render(request,'FitApp/errorHorarioSucursal.html',{'error':error,'club':sucursal.club})
                else:
                    if lunesCheck:
                        lunes = True
                    else:
                        lunes = False
                    if martesCheck:
                        martes = True
                    else:
                        martes = False
                    if miercolesCheck:
                        miercoles = True
                    else:
                        miercoles = False
                    if juevesCheck:
                        jueves = True
                    else:
                        jueves = False
                    if viernesCheck:
                        viernes = True
                    else:
                        viernes = False
                    if sabadoCheck:
                        sabado = True
                    else:
                        sabado = False
                    if domingoCheck:
                        domingo = True
                    else:
                        domingo = False
                    tipoHorario = int(request.POST['tipoHorario'])
                    tipo = ''
                    if tipoHorario == 1:
                        tipo = u'Corrido'
                    else:
                        tipo = u'Mixto'
                    horario = Horario(sucursal=sucursal,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo,numDias=numDias,tipo=tipo)
                    horario.save()
                    if lunes:
                        dia = u'Lunes'
                        apertura1 = request.POST['lunesA1']
                        cierre1 = request.POST['lunesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Lunes con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['lunesA2']
                        cierre2 = request.POST['lunesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Lunes con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if martes:
                        dia = u'Martes'
                        apertura1 = request.POST['martesA1']
                        cierre1 = request.POST['martesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Martes con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['martesA2']
                        cierre2 = request.POST['martesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Martes con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if miercoles:
                        dia = u'Miércoles'
                        apertura1 = request.POST['miercolesA1']
                        cierre1 = request.POST['miercolesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Miércoles con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['miercolesA2']
                        cierre2 = request.POST['miercolesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Miércoles con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if jueves:
                        dia = u'Jueves'
                        apertura1 = request.POST['juevesA1']
                        cierre1 = request.POST['juevesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Jueves con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['juevesA2']
                        cierre2 = request.POST['juevesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Jueves con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if viernes:
                        dia = u'Viernes'
                        apertura1 = request.POST['viernesA1']
                        cierre1 = request.POST['viernesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Viernes con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['viernesA2']
                        cierre2 = request.POST['viernesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Viernes con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if sabado:
                        dia = u'Sábado'
                        apertura1 = request.POST['sabadoA1']
                        cierre1 = request.POST['sabadoC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Sábado con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['sabadoA2']
                        cierre2 = request.POST['sabadoC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Sábado con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if domingo:
                        dia = u'Domingo'
                        apertura1 = request.POST['domingoA1']
                        cierre1 = request.POST['domingoC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Domingo con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['domingoA2']
                        cierre2 = request.POST['domingoC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Domingo con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                if not errores:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    numDiasActual = horarioSuc.numDias
                    mensualidad = sucursal.mensualidad
                    calculo = (mensualidad)/(numDiasActual*4)
                    calculoComision = (10*calculo)/100
                    totalDia = calculo + calculoComision
                    sucursal.dia = Dec(totalDia)
                    sucursal.save()
                    url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
                    return HttpResponseRedirect(url)
                else:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    horarioSuc.delete()
                    error = 'Ha ocurrido uno o más errores al momento de registrar el horario, favor de revisarlos.'
                    return render(request,'FitApp/errorHorarioSucursalVarios.html',{'error':error,'errores':json.dumps(errores),'club':horarioSuc.sucursal.club})
            else:
                error = 'Esta sucursal ya tiene un horario, registrado, si quieres editarlo usa el formulario de edición.'
                return render(request,'FitApp/errorHorarioSucursal.html',{'error':error,'club':sucursal.club})
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def editHorarioSucursal(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            horarioID = request.POST['horario']
            horario = Horario.objects.get(id=horarioID)
            sucursal = horario.sucursal
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                error = 'Debe seleccionar al menos un día en el horario.'
                return render(request,'FitApp/errorHorarioSucursal.html',{'error':error,'club':horario.sucursal.club})
            lunes = False
            martes = False
            miercoles = False
            jueves = False
            viernes = False
            sabado = False
            domingo = False
            if lunesCheck:
                lunes = True
            else:
                lunes = False
            if martesCheck:
                martes = True
            else:
                martes = False
            if miercolesCheck:
                miercoles = True
            else:
                miercoles = False
            if juevesCheck:
                jueves = True
            else:
                jueves = False
            if viernesCheck:
                viernes = True
            else:
                viernes = False
            if sabadoCheck:
                sabado = True
            else:
                sabado = False
            if domingoCheck:
                domingo = True
            else:
                domingo = False
            horario.lunes = lunes
            horario.martes = martes
            horario.miercoles = miercoles
            horario.jueves = jueves
            horario.viernes = viernes
            horario.sabado = sabado
            horario.domingo = domingo
            horario.numDias = numDias
            horario.save()
            if lunesCheck:
                dia = u'Lunes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['lunesA']
                    cierre = request.POST['lunesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Lunes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if martesCheck:
                dia = u'Martes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['martesA']
                    cierre = request.POST['martesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Martes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if miercolesCheck:
                dia = u'Miércoles'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['miercolesA']
                    cierre = request.POST['miercolesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Miércoles'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if juevesCheck:
                dia = u'Jueves'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['juevesA']
                    cierre = request.POST['juevesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Jueves'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if viernesCheck:
                dia = u'Viernes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['viernesA']
                    cierre = request.POST['viernesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Viernes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if sabadoCheck:
                dia = u'Sábado'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['sabadoA']
                    cierre = request.POST['sabadoC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Sábado'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if domingoCheck:
                dia = u'Domingo'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['domingoA']
                    cierre = request.POST['domingoC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Domingo'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            horarioSuc = Horario.objects.get(id=horarioID)
            sucursal = horarioSuc.sucursal
            numDiasActual = horarioSuc.numDias
            mensualidad = sucursal.mensualidad
            calculo = (mensualidad)/(numDiasActual*4)
            calculoComision = (10*calculo)/100
            totalDia = calculo + calculoComision
            sucursal.dia = Dec(totalDia)
            sucursal.save()
            url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def editHorarioMixtoSucursal(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            horarioID = request.POST['horario']
            horario = Horario.objects.get(id=horarioID)
            sucursal = horario.sucursal
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                error = 'Debe seleccionar al menos un día en el horario.'
                return render(request,'FitApp/errorHorarioSucursal.html',{'error':error,'club':horario.sucursal.club})
            lunes = False
            martes = False
            miercoles = False
            jueves = False
            viernes = False
            sabado = False
            domingo = False
            if lunesCheck:
                lunes = True
            else:
                lunes = False
            if martesCheck:
                martes = True
            else:
                martes = False
            if miercolesCheck:
                miercoles = True
            else:
                miercoles = False
            if juevesCheck:
                jueves = True
            else:
                jueves = False
            if viernesCheck:
                viernes = True
            else:
                viernes = False
            if sabadoCheck:
                sabado = True
            else:
                sabado = False
            if domingoCheck:
                domingo = True
            else:
                domingo = False
            horario.lunes = lunes
            horario.martes = martes
            horario.miercoles = miercoles
            horario.jueves = jueves
            horario.viernes = viernes
            horario.sabado = sabado
            horario.domingo = domingo
            horario.numDias = numDias
            horario.save()
            if lunesCheck:
                dia = u'Lunes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['lunesA1']
                    cierre1 = request.POST['lunesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['lunesA2']
                    cierre2 = request.POST['lunesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Lunes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if martesCheck:
                dia = u'Martes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['martesA1']
                    cierre1 = request.POST['martesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['martesA2']
                    cierre2 = request.POST['martesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Martes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if miercolesCheck:
                dia = u'Miércoles'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['miercolesA1']
                    cierre1 = request.POST['miercolesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['miercolesA2']
                    cierre2 = request.POST['miercolesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Miércoles'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if juevesCheck:
                dia = u'Jueves'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['juevesA1']
                    cierre1 = request.POST['juevesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['juevesA2']
                    cierre2 = request.POST['juevesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Jueves'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if viernesCheck:
                dia = u'Viernes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['viernesA1']
                    cierre1 = request.POST['viernesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['viernesA2']
                    cierre2 = request.POST['viernesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Viernes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if sabadoCheck:
                dia = u'Sábado'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['sabadoA1']
                    cierre1 = request.POST['sabadoC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['sabadoA2']
                    cierre2 = request.POST['sabadoC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Sábado'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if domingoCheck:
                dia = u'Domingo'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['domingoA1']
                    cierre1 = request.POST['domingoC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['domingoA2']
                    cierre2 = request.POST['domingoC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Domingo'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            horarioSuc = Horario.objects.get(id=horarioID)
            sucursal = horarioSuc.sucursal
            numDiasActual = horarioSuc.numDias
            mensualidad = sucursal.mensualidad
            calculo = (mensualidad)/(numDiasActual*4)
            calculoComision = (10*calculo)/100
            totalDia = calculo + calculoComision
            sucursal.dia = Dec(totalDia)
            sucursal.save()
            url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def editRegistroHorario(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            registroHorarioID = request.POST['registroHorario']
            registroHorario = RegistroHorario.objects.get(id=registroHorarioID)
            apertura = request.POST['apertura']
            cierre = request.POST['cierre']
            registroHorario.apertura = apertura
            registroHorario.cierre = cierre
            registroHorario.save()
            sucursal = registroHorario.sucursal
            url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def deleteHorarioSucursal(request,horario_id):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            horario = Horario.objects.get(id=horario_id)
        except Horario.DoesNotExist:
            horario = False
        if horario:
            club = horario.sucursal.club
            sucursal = horario.sucursal
            horario.delete()
            sucursal.dia = 0
            sucursal.save()
            try:
                registros = RegistroHorario.objects.filter(sucursal=sucursal)
            except RegistroHorario.DoesNotExist:
                registros = False
            if registros:
                for r in registros:
                    r.delete()
            url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def addFotoSucursal(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                foto = request.FILES['foto']
            except MultiValueDictKeyError:
                foto = False
            if foto:
                for f in request.FILES.getlist('foto'):
                    newFoto = Foto(sucursal=sucursal,archivo=f)
                    newFoto.save()
                url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
                return HttpResponseRedirect(url)
            else:
                error = 'Se requiere subir al menos una imagen.'
                return render(request,'FitApp/errorFotoSucursal.html',{'error':error,'club':sucursal.club})
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def deleteFotoSucursal(request,foto_id):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            foto = Foto.objects.get(id=foto_id)
        except Foto.DoesNotExist:
            foto = False
        if foto:
            club = foto.sucursal.club
            fotoActual = foto.archivo.name
            if not fotoActual == 'default/foto.png':
                os.remove(foto.archivo.path)
            foto.delete()
            url = '/homeAdminClubesDetallesSucursal/'+str(foto.sucursal.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def sucursalUsuarios(request,club_id,sucursal_id):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            club = Club.objects.get(id=club_id)
        except Club.DoesNotExist:
            club = False
        if club:
            try:
                sucursal = Sucursal.objects.get(id=sucursal_id,club=club)
            except Sucursal.DoesNotExist:
                sucursal = False
            if sucursal:
                try:
                    usuarios = Usuario.objects.filter(sucursal=sucursal).order_by('id')
                except Usuario.DoesNotExist:
                    usuarios = False
                page = request.GET.get('page', 1)
                paginator = Paginator(usuarios,50)
                try:
                    usuarios = paginator.page(page)
                except PageNotAnInteger:
                    usuarios = paginator.page(1)
                except EmptyPage:
                    usuarios = paginator.page(paginator.num_pages)
                return render(request,'FitApp/homeAdminClubSucursalUsuarios.html',{'club':sucursal.club,'sucursal':sucursal,'usuarios':usuarios})
            else:
                return HttpResponseRedirect('/homeAdminClubes/')
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def addUsuario(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            nombre = request.POST['nombre']
            correo = request.POST['correo']
            password = request.POST['password']
            mailUsado = False
            try:
                mailUsado = User.objects.get(email=correo)
            except User.DoesNotExist:
                mailUsado = False
            if not mailUsado:
                user = User.objects.create_user(username=correo,email=correo)
                user.set_password(password)
                user.save()
                repetido = False
                try:
                    repetido = Usuario.objects.get(user=user,sucursal=sucursal,nombre=nombre)
                except Usuario.DoesNotExist:
                    repetido = False
                if not repetido:
                    usuario = Usuario(user=user,sucursal=sucursal,nombre=nombre,activo=True)
                    usuario.save()
                    url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
                    return HttpResponseRedirect(url)
                else:
                    error = u'Este usuario ya existe.'
                    return render(request,'FitApp/errorUsuario.html',{'error':error,'club':sucursal.club,'sucursal':sucursal})
            else:
                error = u'Este correo ya esta en uso, favor de utilizar uno diferente.'
                return render(request,'FitApp/errorUsuario.html',{'error':error,'club':sucursal.club,'sucursal':sucursal})
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def editUsuario(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            usuarioID = request.POST['usuario']
            usuario = Usuario.objects.get(id=usuarioID)
            nombre = request.POST['nombre']
            correo = request.POST['correo']
            try:
                password = request.POST['password']
            except MultiValueDictKeyError:
                password = False
            try:
                confirmarPassword = request.POST['confirmarPassword']
            except MultiValueDictKeyError:
                confirmarPassword = False
            try:
                activo = request.POST['activo']
            except MultiValueDictKeyError:
                activo = False
            usuario.nombre = nombre
            usuario.activo = activo
            usuario.save()
            user = usuario.user
            emailActual = user.email
            if not correo == emailActual:
                user.username = correo
                user.email = correo
                user.save()
            if password and confirmarPassword:
                if not password == confirmarPassword:
                    user.set_password(confirmarPassword)
                    user.save()
                else:
                    error = u'La contraseña nueva no debe ser igual a la contraseña actual.'
                    return render(request,'FitApp/errorUsuario.html',{'error':error,'club':usuario.sucursal.club,'sucursal':usuario.sucursal})
            url = '/homeAdminClubesDetallesSucursal/'+str(usuario.sucursal.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def deleteUsuario(request,usuario_id):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            usuario = False
        if usuario:
            user = usuario.user
            club = usuario.sucursal.club
            sucursal = usuario.sucursal
            user.delete()
            usuario.delete()
            url = '/homeAdminClubesDetallesSucursal/'+str(sucursal.id)+'/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeAdminClubes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def getCiudades(request,estado_id):
    if request.is_ajax() and request.method == 'POST':
        estado = Estado.objects.get(id=estado_id)
        cat_ciudades = {}
        try:
            ciudades = Ciudad.objects.filter(estado=estado)
        except Ciudad.DoesNotExist:
            ciudades = False
        if ciudades:
            for c in ciudades:
                cat_ciudades[c.id] = c.nombre
        return HttpResponse(json.dumps(cat_ciudades), content_type="application/json")
    else:
        cat_ciudades = {'None':None}
        return HttpResponse(json.dumps(cat_ciudades), content_type="application/json")

def pagosSucursalAdmin(request):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            sucursales = Sucursal.objects.filter(activa=True)
        except Sucursal.DoesNotExist:
            sucursales = False
        try:
            pagos = PagoSucursal.objects.all().order_by('-fecha')
        except PagoSucursal.DoesNotExist:
            pagos = False
        try:
            pagosT = PagoSucursal.objects.all()
        except PagoSucursal.DoesNotExist:
            pagosT = False
        page = request.GET.get('page', 1)
        paginator = Paginator(pagos,50)
        try:
            pagos = paginator.page(page)
        except PageNotAnInteger:
            pagos = paginator.page(1)
        except EmptyPage:
            pagos = paginator.page(paginator.num_pages)
        return render(request,'FitApp/homeAdminPagosSucursales.html',{'sucursales':sucursales,'pagos':pagos,'pagosT':pagosT})
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

class ReportePagosSucursal(View):
    def get(self,request):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                sucursales = Sucursal.objects.filter(activa=True)
            except Sucursal.DoesNotExist:
                sucursales = False
            if sucursales:
                try:
                    pagos = PagoSucursal.objects.all().order_by('-fecha')
                except PagoSucursal.DoesNotExist:
                    pagos = False
                if pagos:
                    filename = "Reporte_Pagos_Sucursal.xlsx"
                    wb = xlsxwriter.Workbook(filename)
                    center = wb.add_format({'align':'center'})
                    format = wb.add_format({'align':'center'})
                    format.set_text_wrap()
                    gris = wb.add_format({'font_color':'#9e9e9e'})
                    header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                    body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                    sheet = wb.add_worksheet(u'Pagos a Sucursales')
                    sheet.write(0,0,u'ID',header)
                    sheet.write(0,1,u'CLUB',header)
                    sheet.write(0,2,u'SUCURSAL',header)
                    sheet.write(0,3,u'CANTIDAD',header)
                    sheet.write(0,4,u'FECHA',header)
                    sheet.write(0,5,u'Nº RASTREO',header)
                    sheet.set_column('A:A', 20)
                    sheet.set_column('B:B', 20)
                    sheet.set_column('C:C', 20)
                    sheet.set_column('D:D', 20)
                    sheet.set_column('E:E', 20)
                    sheet.set_column('F:F', 20)
                    sheet.protect()
                    row = 0
                    for p in pagos:
                        row += 1
                        sheet.write(row,0,p.id,body)
                        sheet.write(row,1,p.sucursal.club.nombre,body)
                        sheet.write(row,2,p.sucursal.nombre,body)
                        sheet.write(row,3,'$'+str(p.pagar),body)
                        sheet.write(row,4,p.fecha.strftime('%d-%m-%Y'),body)
                        if p.numRastreo:
                            numRastreo = p.numRastreo
                        else:
                            numRastreo = ''
                        sheet.write(row,5,numRastreo,body)
                    wb.close()
                    return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

def addPagoSucursal(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            try:
                sucursalID = request.POST['sucursal']
            except MultiValueDictKeyError:
                error = u'Favor de seleccionar una sucursal.'
                return render(request,'FitApp/errorPagoSucursal.html',{'error':error})
            sucursal = Sucursal.objects.get(id=sucursalID)
            pagar = Dec(request.POST['pagar'])
            fecha = request.POST['fecha']
            try:
                numRastreo = request.POST['numRastreo']
            except MultiValueDictKeyError:
                numRastreo = None
            try:
                confirmar = request.POST['confirmar']
            except MultiValueDictKeyError:
                confirmar = False
            if confirmar:
                saldoActual = Dec(sucursal.saldo)
                if pagar <= saldoActual:
                    pago = PagoSucursal(sucursal=sucursal,pagar=pagar,fecha=fecha,numRastreo=numRastreo)
                    pago.save()
                    saldoNuevo = saldoActual - pagar
                    sucursal.saldo = saldoNuevo
                    sucursal.save()
                    return HttpResponseRedirect('/homeAdminPagosSucursal/')
                else:
                    error = u'El pago es superior al monto del saldo de esta sucursal.'
                    return render(request,'FitApp/errorPagoSucursal.html',{'error':error})
            else:
                return HttpResponseRedirect('/homeAdminPagosSucursal/')
        else:
            return HttpResponseRedirect('/homeAdminPagosSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def deletePagoSucursal(request,pago_id):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            pago = PagoSucursal.objects.get(id=pago_id)
        except PagoSucursal.DoesNotExist:
            pago = False
        if pago:
            pagar = Dec(pago.pagar)
            sucursal = pago.sucursal
            saldoActual = Dec(sucursal.saldo)
            nuevoSaldo = saldoActual + pagar
            pago.delete()
            sucursal.saldo = nuevoSaldo
            sucursal.save()
            return HttpResponseRedirect('/homeAdminPagosSucursal/')
        else:
            return HttpResponseRedirect('/homeAdminPagosSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def clientesAdmin(request):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            clientesT = Cliente.objects.all()
        except Cliente.DoesNotExist:
            clientesT = False
        try:
            clientes = Cliente.objects.all().order_by('id')
        except Cliente.DoesNotExist:
            clientes = False
        page = request.GET.get('page', 1)
        paginator = Paginator(clientes,50)
        try:
            clientes = paginator.page(page)
        except PageNotAnInteger:
            clientes = paginator.page(1)
        except EmptyPage:
            clientes = paginator.page(paginator.num_pages)
        return render(request,'FitApp/homeAdminClientes.html',{'clientes':clientes,'clientesT':clientesT})
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

class ReporteClientes(View):
    def get(self,request):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                clientes = Cliente.objects.all()
            except Cliente.DoesNotExist:
                clientes = False
            if clientes:
                filename = "Reporte_Apertura_Cierre_Sucursal.xlsx"
                wb = xlsxwriter.Workbook(filename)
                center = wb.add_format({'align':'center'})
                format = wb.add_format({'align':'center'})
                format.set_text_wrap()
                gris = wb.add_format({'font_color':'#9e9e9e'})
                header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                sheet = wb.add_worksheet(u'Clientes')
                sheet.write(0,0,u'ID',header)
                sheet.write(0,1,u'NOMBRE',header)
                sheet.write(0,2,u'APELLIDO',header)
                sheet.write(0,3,u'TELÉFONO',header)
                sheet.write(0,4,u'CORREO',header)
                sheet.write(0,5,u'GENERO',header)
                sheet.write(0,6,u'FECHA INGRESO',header)
                sheet.write(0,7,u'SALUD',header)
                sheet.write(0,8,u'CONVIVIR',header)
                sheet.write(0,9,u'VERME BIEN',header)
                sheet.write(0,10,u'DIVERSIÓN',header)
                sheet.write(0,11,u'ESTADO',header)
                sheet.write(0,12,u'CIUDAD',header)
                sheet.write(0,13,u'UBICACIÓN',header)
                sheet.write(0,14,u'BLUETOOTH',header)
                sheet.write(0,15,u'FOTO',header)
                sheet.set_column('A:A', 20)
                sheet.set_column('B:B', 50)
                sheet.set_column('C:C', 50)
                sheet.set_column('D:D', 50)
                sheet.set_column('E:E', 50)
                sheet.set_column('F:F', 50)
                sheet.set_column('G:G', 50)
                sheet.set_column('H:H', 20)
                sheet.set_column('I:I', 20)
                sheet.set_column('J:J', 20)
                sheet.set_column('K:K', 20)
                sheet.set_column('L:L', 50)
                sheet.set_column('M:M', 50)
                sheet.set_column('N:N', 20)
                sheet.set_column('O:O', 20)
                sheet.set_column('P:P', 70)
                sheet.protect()
                row = 0
                for c in clientes:
                    row += 1
                    salud = ''
                    if c.salud == True:
                        salud = 'Si'
                    else:
                        salud = 'No'
                    convivir = ''
                    if c.convivir == True:
                        convivir = 'Si'
                    else:
                        convivir = 'No'
                    vermeBien = ''
                    if c.vermeBien == True:
                        vermeBien = 'Si'
                    else:
                        vermeBien = 'No'
                    diversion = ''
                    if c.diversion == True:
                        diversion = 'Si'
                    else:
                        diversion = 'No'
                    bluetooth = ''
                    if c.bluetooth == True:
                        bluetooth = 'Si'
                    else:
                        bluetooth = 'No'
                    ubicacion = ''
                    if c.ubicacion == True:
                        ubicacion = 'Si'
                    else:
                        ubicacion = 'No'
                    genero = ''
                    if c.hombre == True and c.mujer == False:
                        genero = 'Hombre'
                    else:
                        genero = 'Mujer'
                    estado = ''
                    if c.estado:
                        estado = c.estado.nombre
                    else:
                        estado = '-'
                    ciudad = ''
                    if c.ciudad:
                        ciudad = c.ciudad.nombre
                    else:
                        ciudad = '-'
                    foto = 'https://www.fitory.com/media/'+c.foto.name
                    sheet.write(row,0,c.id,body)
                    sheet.write(row,1,c.nombre,body)
                    sheet.write(row,2,c.apellido,body)
                    sheet.write(row,3,c.telefono,body)
                    sheet.write(row,4,c.user.email,body)
                    sheet.write(row,5,genero,body)
                    sheet.write(row,6,c.fechaIngreso.strftime('%d-%m-%Y'),body)
                    sheet.write(row,7,salud,body)
                    sheet.write(row,8,convivir,body)
                    sheet.write(row,9,vermeBien,body)
                    sheet.write(row,10,diversion,body)
                    sheet.write(row,11,estado,body)
                    sheet.write(row,12,ciudad,body)
                    sheet.write(row,13,ubicacion,body)
                    sheet.write(row,14,bluetooth,body)
                    sheet.write(row,15,foto,body)
                wb.close()
                return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

def homeAdminReportes(request):
    if request.user.is_staff and request.user.is_authenticated:
        try:
            clubes = Club.objects.all().order_by('nombre')
        except Club.DoesNotExist:
            clubes = False
        arreglo = []
        try:
            subscripciones = Subscripcion.objects.all()
        except Subscripcion.DoesNotExist:
            subscripciones = False
        try:
            sesiones = Sesion.objects.all()
        except Sesion.DoesNotExist:
            sesiones = False
        if subscripciones:
            for s in subscripciones:
                id = s.id
                club = s.sucursal.club
                sucursal = s.sucursal
                cliente = s.cliente
                servicio = 'Mensual'
                total = s.totalCobrar
                fechaCaducidad = s.fechaRenovacion
                sesionesRestantes = 'NA'
                if s.activa == True:
                    estatus = 'Activa'
                else:
                    estatus = 'Inactiva'
                arr = {
                    'id':id,
                    'club':club,
                    'sucursal':sucursal,
                    'cliente':cliente,
                    'servicio':servicio,
                    'total':total,
                    'fechaCaducidad':fechaCaducidad,
                    'sesionesRestantes':sesionesRestantes,
                    'estatus':estatus
                }
                arreglo.append(arr)
        if sesiones:
            for s in sesiones:
                id = s.id
                club = s.sucursal.club
                sucursal = s.sucursal
                cliente = s.cliente
                servicio = 'Diario'
                total = s.total
                fechaCaducidad = s.caducidad
                sesionesRestantes = s.sesionesRestantes
                if s.activo == True:
                    estatus = 'Activa'
                else:
                    estatus = 'Inactiva'
                arr = {
                    'id':id,
                    'club':club,
                    'sucursal':sucursal,
                    'cliente':cliente,
                    'servicio':servicio,
                    'total':total,
                    'fechaCaducidad':fechaCaducidad,
                    'sesionesRestantes':sesionesRestantes,
                    'estatus':estatus
                }
                arreglo.append(arr)
        page = request.GET.get('page', 1)
        paginator = Paginator(arreglo,50)
        try:
            arreglo = paginator.page(page)
        except PageNotAnInteger:
            arreglo = paginator.page(1)
        except EmptyPage:
            arreglo = paginator.page(paginator.num_pages)
        return render(request,'FitApp/homeAdminReportes.html',{'clubes':clubes,'arreglo':arreglo})
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def filtrarReporteNuevo(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            inicio = request.POST['inicio']
            final = request.POST['final']
            inicioF = datetime.strptime(inicio,'%Y-%m-%d')
            finalF = datetime.strptime(final,'%Y-%m-%d')
            if inicioF > finalF:
                error = u'Fecha de inicio no puede ser mayor a la fecha final.'
                return render(request,'FitApp/errorFiltroReporte.html',{'error':error})
            else:
                try:
                    clubID = int(request.POST['club'])
                except MultiValueDictKeyError:
                    clubID = False
                try:
                    servicio = int(request.POST['servicio'])
                except MultiValueDictKeyError:
                    servicio = False
                try:
                    estatus = int(request.POST['estatus'])
                except MultiValueDictKeyError:
                    estatus = False
                arreglo = []
                if not clubID and not servicio and not estatus:#000
                    print('Sin filtro')
                    try:
                        subscripciones = Subscripcion.objects.filter(fechaRenovacion__range=(inicio,final))
                    except Subscripcion.DoesNotExist:
                        subscripciones = False
                    try:
                        sesiones = Sesion.objects.filter(caducidad__range=(inicio,final))
                    except Sesion.DoesNotExist:
                        sesiones = False
                    if subscripciones:
                        for s in subscripciones:
                            id = s.id
                            club = s.sucursal.club
                            sucursal = s.sucursal
                            cliente = s.cliente
                            servicio = 'Mensual'
                            total = s.totalCobrar
                            fechaCaducidad = s.fechaRenovacion
                            sesionesRestantes = 'NA'
                            if s.activa == True:
                                estatus = 'Activa'
                            else:
                                estatus = 'Inactiva'
                            arr = {
                                'id':id,
                                'club':club,
                                'sucursal':sucursal,
                                'cliente':cliente,
                                'servicio':servicio,
                                'total':total,
                                'fechaCaducidad':fechaCaducidad,
                                'sesionesRestantes':sesionesRestantes,
                                'estatus':estatus
                            }
                            arreglo.append(arr)
                    if sesiones:
                        for s in sesiones:
                            id = s.id
                            club = s.sucursal.club
                            sucursal = s.sucursal
                            cliente = s.cliente
                            servicio = 'Diario'
                            total = s.total
                            fechaCaducidad = s.caducidad
                            sesionesRestantes = s.sesionesRestantes
                            if s.activo == True:
                                estatus = 'Activa'
                            else:
                                estatus = 'Inactiva'
                            arr = {
                                'id':id,
                                'club':club,
                                'sucursal':sucursal,
                                'cliente':cliente,
                                'servicio':servicio,
                                'total':total,
                                'fechaCaducidad':fechaCaducidad,
                                'sesionesRestantes':sesionesRestantes,
                                'estatus':estatus
                            }
                            arreglo.append(arr)
                elif not clubID and not servicio and estatus:#001
                    print('Filtrar por estatus')
                    if estatus == 1:
                        activo = True
                        activa = True
                    elif estatus == 2:
                        activo = False
                        activa = False
                    try:
                        subscripciones = Subscripcion.objects.filter(fechaRenovacion__range=(inicio,final),activa=activa)
                    except Subscripcion.DoesNotExist:
                        subscripciones = False
                    try:
                        sesiones = Sesion.objects.filter(caducidad__range=(inicio,final),activo=activo)
                    except Sesion.DoesNotExist:
                        sesiones = False
                    if subscripciones:
                        for s in subscripciones:
                            id = s.id
                            club = s.sucursal.club
                            sucursal = s.sucursal
                            cliente = s.cliente
                            servicio = 'Mensual'
                            total = s.totalCobrar
                            fechaCaducidad = s.fechaRenovacion
                            sesionesRestantes = 'NA'
                            if s.activa == True:
                                estatus = 'Activa'
                            else:
                                estatus = 'Inactiva'
                            arr = {
                                'id':id,
                                'club':club,
                                'sucursal':sucursal,
                                'cliente':cliente,
                                'servicio':servicio,
                                'total':total,
                                'fechaCaducidad':fechaCaducidad,
                                'sesionesRestantes':sesionesRestantes,
                                'estatus':estatus
                            }
                            arreglo.append(arr)
                    if sesiones:
                        for s in sesiones:
                            id = s.id
                            club = s.sucursal.club
                            sucursal = s.sucursal
                            cliente = s.cliente
                            servicio = 'Diario'
                            total = s.total
                            fechaCaducidad = s.caducidad
                            sesionesRestantes = s.sesionesRestantes
                            if s.activo == True:
                                estatus = 'Activa'
                            else:
                                estatus = 'Inactiva'
                            arr = {
                                'id':id,
                                'club':club,
                                'sucursal':sucursal,
                                'cliente':cliente,
                                'servicio':servicio,
                                'total':total,
                                'fechaCaducidad':fechaCaducidad,
                                'sesionesRestantes':sesionesRestantes,
                                'estatus':estatus
                            }
                            arreglo.append(arr)
                elif not clubID and servicio and not estatus:#010
                    print('Filtrar por servicio')
                    if servicio == 1:
                        try:
                            subscripciones = Subscripcion.objects.filter(fechaRenovacion__range=(inicio,final))
                        except Subscripcion.DoesNotExist:
                            subscripciones = False
                        if subscripciones:
                            for s in subscripciones:
                                id = s.id
                                club = s.sucursal.club
                                sucursal = s.sucursal
                                cliente = s.cliente
                                servicio = 'Mensual'
                                total = s.totalCobrar
                                fechaCaducidad = s.fechaRenovacion
                                sesionesRestantes = 'NA'
                                if s.activa == True:
                                    estatus = 'Activa'
                                else:
                                    estatus = 'Inactiva'
                                arr = {
                                    'id':id,
                                    'club':club,
                                    'sucursal':sucursal,
                                    'cliente':cliente,
                                    'servicio':servicio,
                                    'total':total,
                                    'fechaCaducidad':fechaCaducidad,
                                    'sesionesRestantes':sesionesRestantes,
                                    'estatus':estatus
                                }
                                arreglo.append(arr)
                    elif servicio == 2:
                        try:
                            sesiones = Sesion.objects.filter(caducidad__range=(inicio,final))
                        except Sesion.DoesNotExist:
                            sesiones = False
                        if sesiones:
                            for s in sesiones:
                                id = s.id
                                club = s.sucursal.club
                                sucursal = s.sucursal
                                cliente = s.cliente
                                servicio = 'Diario'
                                total = s.total
                                fechaCaducidad = s.caducidad
                                sesionesRestantes = s.sesionesRestantes
                                if s.activo == True:
                                    estatus = 'Activa'
                                else:
                                    estatus = 'Inactiva'
                                arr = {
                                    'id':id,
                                    'club':club,
                                    'sucursal':sucursal,
                                    'cliente':cliente,
                                    'servicio':servicio,
                                    'total':total,
                                    'fechaCaducidad':fechaCaducidad,
                                    'sesionesRestantes':sesionesRestantes,
                                    'estatus':estatus
                                }
                                arreglo.append(arr)
                elif not clubID and servicio and estatus:#011
                    print('Filtrar por servicio y estatus')
                    if estatus == 1:
                        activo = True
                        activa = True
                    elif estatus == 2:
                        activo = False
                        activa = False
                    if servicio == 1:
                        try:
                            subscripciones = Subscripcion.objects.filter(fechaRenovacion__range=(inicio,final),activa=activa)
                        except Subscripcion.DoesNotExist:
                            subscripciones = False
                        if subscripciones:
                            for s in subscripciones:
                                id = s.id
                                club = s.sucursal.club
                                sucursal = s.sucursal
                                cliente = s.cliente
                                servicio = 'Mensual'
                                total = s.totalCobrar
                                fechaCaducidad = s.fechaRenovacion
                                sesionesRestantes = 'NA'
                                if s.activa == True:
                                    estatus = 'Activa'
                                else:
                                    estatus = 'Inactiva'
                                arr = {
                                    'id':id,
                                    'club':club,
                                    'sucursal':sucursal,
                                    'cliente':cliente,
                                    'servicio':servicio,
                                    'total':total,
                                    'fechaCaducidad':fechaCaducidad,
                                    'sesionesRestantes':sesionesRestantes,
                                    'estatus':estatus
                                }
                                arreglo.append(arr)
                    elif servicio == 2:
                        try:
                            sesiones = Sesion.objects.filter(caducidad__range=(inicio,final),activo=activo)
                        except Sesion.DoesNotExist:
                            sesiones = False
                        if sesiones:
                            for s in sesiones:
                                id = s.id
                                club = s.sucursal.club
                                sucursal = s.sucursal
                                cliente = s.cliente
                                servicio = 'Diario'
                                total = s.total
                                fechaCaducidad = s.caducidad
                                sesionesRestantes = s.sesionesRestantes
                                if s.activo == True:
                                    estatus = 'Activa'
                                else:
                                    estatus = 'Inactiva'
                                arr = {
                                    'id':id,
                                    'club':club,
                                    'sucursal':sucursal,
                                    'cliente':cliente,
                                    'servicio':servicio,
                                    'total':total,
                                    'fechaCaducidad':fechaCaducidad,
                                    'sesionesRestantes':sesionesRestantes,
                                    'estatus':estatus
                                }
                                arreglo.append(arr)
                elif clubID and not servicio and not estatus:#100
                    print('Filtrar por club')
                    club = Club.objects.get(id=clubID)
                    try:
                        subscripciones = Subscripcion.objects.filter(sucursal__club=club,fechaRenovacion__range=(inicio,final))
                    except Subscripcion.DoesNotExist:
                        subscripciones = False
                    try:
                        sesiones = Sesion.objects.filter(sucursal__club=club,caducidad__range=(inicio,final))
                    except Sesion.DoesNotExist:
                        sesiones = False
                    if subscripciones:
                        for s in subscripciones:
                            id = s.id
                            club = s.sucursal.club
                            sucursal = s.sucursal
                            cliente = s.cliente
                            servicio = 'Mensual'
                            total = s.totalCobrar
                            fechaCaducidad = s.fechaRenovacion
                            sesionesRestantes = 'NA'
                            if s.activa == True:
                                estatus = 'Activa'
                            else:
                                estatus = 'Inactiva'
                            arr = {
                                'id':id,
                                'club':club,
                                'sucursal':sucursal,
                                'cliente':cliente,
                                'servicio':servicio,
                                'total':total,
                                'fechaCaducidad':fechaCaducidad,
                                'sesionesRestantes':sesionesRestantes,
                                'estatus':estatus
                            }
                            arreglo.append(arr)
                    if sesiones:
                        for s in sesiones:
                            id = s.id
                            club = s.sucursal.club
                            sucursal = s.sucursal
                            cliente = s.cliente
                            servicio = 'Diario'
                            total = s.total
                            fechaCaducidad = s.caducidad
                            sesionesRestantes = s.sesionesRestantes
                            if s.activo == True:
                                estatus = 'Activa'
                            else:
                                estatus = 'Inactiva'
                            arr = {
                                'id':id,
                                'club':club,
                                'sucursal':sucursal,
                                'cliente':cliente,
                                'servicio':servicio,
                                'total':total,
                                'fechaCaducidad':fechaCaducidad,
                                'sesionesRestantes':sesionesRestantes,
                                'estatus':estatus
                            }
                            arreglo.append(arr)
                elif clubID and not servicio and estatus:#101
                    print('Filtrar por club y estatus')
                    club = Club.objects.get(id=clubID)
                    if estatus == 1:
                        activo = True
                        activa = True
                    elif estatus == 2:
                        activo = False
                        activa = False
                    try:
                        subscripciones = Subscripcion.objects.filter(sucursal__club=club,fechaRenovacion__range=(inicio,final),activa=activa)
                    except Subscripcion.DoesNotExist:
                        subscripciones = False
                    try:
                        sesiones = Sesion.objects.filter(sucursal__club=club,caducidad__range=(inicio,final),activo=activo)
                    except Sesion.DoesNotExist:
                        sesiones = False
                    if subscripciones:
                        for s in subscripciones:
                            id = s.id
                            club = s.sucursal.club
                            sucursal = s.sucursal
                            cliente = s.cliente
                            servicio = 'Mensual'
                            total = s.totalCobrar
                            fechaCaducidad = s.fechaRenovacion
                            sesionesRestantes = 'NA'
                            if s.activa == True:
                                estatus = 'Activa'
                            else:
                                estatus = 'Inactiva'
                            arr = {
                                'id':id,
                                'club':club,
                                'sucursal':sucursal,
                                'cliente':cliente,
                                'servicio':servicio,
                                'total':total,
                                'fechaCaducidad':fechaCaducidad,
                                'sesionesRestantes':sesionesRestantes,
                                'estatus':estatus
                            }
                            arreglo.append(arr)
                    if sesiones:
                        for s in sesiones:
                            id = s.id
                            club = s.sucursal.club
                            sucursal = s.sucursal
                            cliente = s.cliente
                            servicio = 'Diario'
                            total = s.total
                            fechaCaducidad = s.caducidad
                            sesionesRestantes = s.sesionesRestantes
                            if s.activo == True:
                                estatus = 'Activa'
                            else:
                                estatus = 'Inactiva'
                            arr = {
                                'id':id,
                                'club':club,
                                'sucursal':sucursal,
                                'cliente':cliente,
                                'servicio':servicio,
                                'total':total,
                                'fechaCaducidad':fechaCaducidad,
                                'sesionesRestantes':sesionesRestantes,
                                'estatus':estatus
                            }
                            arreglo.append(arr)
                elif clubID and servicio and not estatus:#110
                    print('Filtrar por club y servicio')
                    club = Club.objects.get(id=clubID)
                    if servicio == 1:
                        try:
                            subscripciones = Subscripcion.objects.filter(sucursal__club=club,fechaRenovacion__range=(inicio,final))
                        except Subscripcion.DoesNotExist:
                            subscripciones = False
                        if subscripciones:
                            for s in subscripciones:
                                id = s.id
                                club = s.sucursal.club
                                sucursal = s.sucursal
                                cliente = s.cliente
                                servicio = 'Mensual'
                                total = s.totalCobrar
                                fechaCaducidad = s.fechaRenovacion
                                sesionesRestantes = 'NA'
                                if s.activa == True:
                                    estatus = 'Activa'
                                else:
                                    estatus = 'Inactiva'
                                arr = {
                                    'id':id,
                                    'club':club,
                                    'sucursal':sucursal,
                                    'cliente':cliente,
                                    'servicio':servicio,
                                    'total':total,
                                    'fechaCaducidad':fechaCaducidad,
                                    'sesionesRestantes':sesionesRestantes,
                                    'estatus':estatus
                                }
                                arreglo.append(arr)
                    elif servicio == 2:
                        try:
                            sesiones = Sesion.objects.filter(sucursal__club=club,caducidad__range=(inicio,final))
                        except Sesion.DoesNotExist:
                            sesiones = False
                        if sesiones:
                            for s in sesiones:
                                id = s.id
                                club = s.sucursal.club
                                sucursal = s.sucursal
                                cliente = s.cliente
                                servicio = 'Diario'
                                total = s.total
                                fechaCaducidad = s.caducidad
                                sesionesRestantes = s.sesionesRestantes
                                if s.activo == True:
                                    estatus = 'Activa'
                                else:
                                    estatus = 'Inactiva'
                                arr = {
                                    'id':id,
                                    'club':club,
                                    'sucursal':sucursal,
                                    'cliente':cliente,
                                    'servicio':servicio,
                                    'total':total,
                                    'fechaCaducidad':fechaCaducidad,
                                    'sesionesRestantes':sesionesRestantes,
                                    'estatus':estatus
                                }
                                arreglo.append(arr)
                elif clubID and servicio and estatus:#111
                    print('Filtrar por club, servicio y estatus')
                    club = Club.objects.get(id=clubID)
                    if estatus == 1:
                        activo = True
                        activa = True
                    elif estatus == 2:
                        activo = False
                        activa = False
                    if servicio == 1:
                        print('Filtrar solo subscripciones del club '+str(club.nombre)+' donde activa es '+str(activa))
                        try:
                            subscripciones = Subscripcion.objects.filter(sucursal__club=club,fechaRenovacion__range=(inicio,final),activa=activa)
                        except Subscripcion.DoesNotExist:
                            subscripciones = False
                        print(subscripciones)
                        if subscripciones:
                            for s in subscripciones:
                                id = s.id
                                club = s.sucursal.club
                                sucursal = s.sucursal
                                cliente = s.cliente
                                servicio = 'Mensual'
                                total = s.totalCobrar
                                fechaCaducidad = s.fechaRenovacion
                                sesionesRestantes = 'NA'
                                if s.activa == True:
                                    estatus = 'Activa'
                                else:
                                    estatus = 'Inactiva'
                                arr = {
                                    'id':id,
                                    'club':club,
                                    'sucursal':sucursal,
                                    'cliente':cliente,
                                    'servicio':servicio,
                                    'total':total,
                                    'fechaCaducidad':fechaCaducidad,
                                    'sesionesRestantes':sesionesRestantes,
                                    'estatus':estatus
                                }
                                arreglo.append(arr)
                    elif servicio == 2:
                        print('Filtrar solo sesiones del club '+str(club.nombre)+' donde activa es '+str(activa))
                        try:
                            sesiones = Sesion.objects.filter(sucursal__club=club,caducidad__range=(inicio,final),activo=activo)
                        except Sesion.DoesNotExist:
                            sesiones = False
                        print(sesiones)
                        if sesiones:
                            for s in sesiones:
                                id = s.id
                                club = s.sucursal.club
                                sucursal = s.sucursal
                                cliente = s.cliente
                                servicio = 'Diario'
                                total = s.total
                                fechaCaducidad = s.caducidad
                                sesionesRestantes = s.sesionesRestantes
                                if s.activo == True:
                                    estatus = 'Activa'
                                else:
                                    estatus = 'Inactiva'
                                arr = {
                                    'id':id,
                                    'club':club,
                                    'sucursal':sucursal,
                                    'cliente':cliente,
                                    'servicio':servicio,
                                    'total':total,
                                    'fechaCaducidad':fechaCaducidad,
                                    'sesionesRestantes':sesionesRestantes,
                                    'estatus':estatus
                                }
                                arreglo.append(arr)
                return render(request,'FitApp/homeAdminReporteResultado.html',{'arreglo':arreglo,'inicioF':inicioF,'finalF':finalF})
        else:
            return HttpResponseRedirect('/homeAdminReportes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

def filtrarReporte(request):
    if request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            inicio = request.POST['inicio']
            final = request.POST['final']
            inicioF = datetime.strptime(inicio,'%Y-%m-%d')
            finalF = datetime.strptime(final,'%Y-%m-%d')
            if inicioF > finalF:
                error = u'Fecha de inicio no puede ser mayor a la fecha final.'
                return render(request,'FitApp/errorFiltroReporte.html',{'error':error})
            else:
                try:
                    clubes = Club.objects.all().order_by('id')
                except Club.DoesNotExist:
                    clubes = False
                clubSucursales = []
                if clubes:
                    for c in clubes:
                        try:
                            sucursales = Sucursal.objects.filter(club=c)
                        except Sucursal.DoesNotExist:
                            sucursales = False
                        if sucursales:
                            clubSucursales.append((c,sucursales))
                        else:
                            clubSucursales.append((c,None))
                return render(request,'FitApp/homeAdminFiltroReporte.html',{'inicioF':inicioF,'finalF':finalF,'clubSucursales':clubSucursales})
        else:
            return HttpResponseRedirect('/homeAdminReportes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')
        
def filtrarReporteSucursalSubscripciones(request,sucursal_id,inicio,final):
    if request.user.is_staff and request.user.is_authenticated:
        inicioF = datetime.strptime(inicio,'%Y-%m-%d')
        finalF = datetime.strptime(final,'%Y-%m-%d')
        try:
            sucursal = Sucursal.objects.get(id=sucursal_id)
        except Sucursal.DoesNotExist:
            sucursal = False
        if sucursal:
            try:
                subscripciones = Subscripcion.objects.filter(sucursal=sucursal,fechaRenovacion__range=(inicio,final))
            except Subscripcion.DoesNotExist:
                subscripciones = False
            return render(request,'FitApp/homeAdminFiltroReporteSucursalSubscripciones.html',{'sucursal':sucursal,'subscripciones':subscripciones,'inicio':inicio,'final':final,'inicioF':inicioF,'finalF':finalF})
        else:
            return HttpResponseRedirect('/homeAdminReportes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

class ReporteSucursalSubscripciones(View):
    def get(self,request,sucursal_id,inicio,final):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                sucursal = Sucursal.objects.get(id=sucursal_id)
            except Sucursal.DoesNotExist:
                sucursal = False
            if sucursal:
                try:
                    subscripciones = Subscripcion.objects.filter(sucursal=sucursal,fechaRenovacion__range=(inicio,final))
                except Subscripcion.DoesNotExist:
                    subscripciones = False
                if subscripciones:
                    filename = "Reporte_Pagos_Sucursal.xlsx"
                    wb = xlsxwriter.Workbook(filename)
                    center = wb.add_format({'align':'center'})
                    format = wb.add_format({'align':'center'})
                    format.set_text_wrap()
                    gris = wb.add_format({'font_color':'#9e9e9e'})
                    header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                    body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                    sheet = wb.add_worksheet(u'Subscripciones')
                    sheet.write(0,0,u'ID',header)
                    sheet.write(0,1,u'CLIENTE',header)
                    sheet.write(0,2,u'TOTAL A COBRAR',header)
                    sheet.write(0,3,u'TOTAL GYM',header)
                    sheet.write(0,4,u'FECHA SUBSCRIPCION',header)
                    sheet.write(0,5,u'FECHA RENOVACION',header)
                    sheet.write(0,6,u'ESTATUS',header)
                    sheet.set_column('A:A', 20)
                    sheet.set_column('B:B', 30)
                    sheet.set_column('C:C', 30)
                    sheet.set_column('D:D', 30)
                    sheet.set_column('E:E', 30)
                    sheet.set_column('F:F', 30)
                    sheet.set_column('G:G', 30)
                    sheet.protect()
                    row = 0
                    for s in subscripciones:
                        row += 1
                        estatus = ''
                        if s.activa == True:
                            estatus = 'Activa'
                        else:
                            estatus = 'Inactiva'
                        sheet.write(row,0,s.id,body)
                        sheet.write(row,1,s.cliente.nombre+' '+s.cliente.apellido,body)
                        sheet.write(row,2,s.totalCobrar,body)
                        sheet.write(row,3,s.totalGym,body)
                        sheet.write(row,4,s.fechaSubscripcion.strftime('%d-%m-%Y'),body)
                        sheet.write(row,5,s.fechaRenovacion.strftime('%d-%m-%Y'),body)
                        sheet.write(row,6,estatus,body)
                    wb.close()
                    return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

def filtrarReporteSucursalSesiones(request,sucursal_id,inicio,final):
    if request.user.is_staff and request.user.is_authenticated:
        inicioF = datetime.strptime(inicio,'%Y-%m-%d')
        finalF = datetime.strptime(final,'%Y-%m-%d')
        try:
            sucursal = Sucursal.objects.get(id=sucursal_id)
        except Sucursal.DoesNotExist:
            sucursal = False
        if sucursal:
            try:
                sesiones = Sesion.objects.filter(sucursal=sucursal,caducidad__range=(inicio,final))
            except Sesion.DoesNotExist:
                sesiones = False
            return render(request,'FitApp/homeAdminFiltroReporteSucursalSesiones.html',{'sucursal':sucursal,'sesiones':sesiones,'inicio':inicio,'final':final,'inicioF':inicioF,'finalF':finalF})
        else:
            return HttpResponseRedirect('/homeAdminReportes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

class ReporteSucursalSesiones(View):
    def get(self,request,sucursal_id,inicio,final):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                sucursal = Sucursal.objects.get(id=sucursal_id)
            except Sucursal.DoesNotExist:
                sucursal = False
            if sucursal:
                try:
                    sesiones = Sesion.objects.filter(sucursal=sucursal,caducidad__range=(inicio,final))
                except Sesion.DoesNotExist:
                    sesiones = False
                if sesiones:
                    filename = "Reporte_Pagos_Sucursal.xlsx"
                    wb = xlsxwriter.Workbook(filename)
                    center = wb.add_format({'align':'center'})
                    format = wb.add_format({'align':'center'})
                    format.set_text_wrap()
                    gris = wb.add_format({'font_color':'#9e9e9e'})
                    header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                    body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                    sheet = wb.add_worksheet(u'Subscripciones')
                    sheet.write(0,0,u'ID',header)
                    sheet.write(0,1,u'CLIENTE',header)
                    sheet.write(0,2,u'TOTAL',header)
                    sheet.write(0,3,u'SESIONES',header)
                    sheet.write(0,4,u'SESIONES RESTANTES',header)
                    sheet.write(0,5,u'FECHA CADUCIDAD',header)
                    sheet.write(0,6,u'ESTATUS',header)
                    sheet.set_column('A:A', 20)
                    sheet.set_column('B:B', 30)
                    sheet.set_column('C:C', 30)
                    sheet.set_column('D:D', 30)
                    sheet.set_column('E:E', 30)
                    sheet.set_column('F:F', 30)
                    sheet.set_column('G:G', 30)
                    sheet.protect()
                    row = 0
                    for s in sesiones:
                        row += 1
                        estatus = ''
                        if s.activo == True:
                            estatus = 'Activo'
                        else:
                            estatus = 'Inactivo'
                        sheet.write(row,0,s.id,body)
                        sheet.write(row,1,s.cliente.nombre+' '+s.cliente.apellido,body)
                        sheet.write(row,2,s.total,body)
                        sheet.write(row,3,s.sesiones,body)
                        sheet.write(row,4,s.sesionesRestantes,body)
                        sheet.write(row,5,s.caducidad.strftime('%d-%m-%Y'),body)
                        sheet.write(row,6,estatus,body)
                    wb.close()
                    return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

def filtrarReporteSucursalVisitas(request,sucursal_id,inicio,final):
    if request.user.is_staff and request.user.is_authenticated:
        inicioF = datetime.strptime(inicio,'%Y-%m-%d')
        finalF = datetime.strptime(final,'%Y-%m-%d')
        try:
            sucursal = Sucursal.objects.get(id=sucursal_id)
        except Sucursal.DoesNotExist:
            sucursal = False
        if sucursal:
            try:
                visitas = Visita.objects.filter(sucursal=sucursal,fecha__range=(inicio,final))
            except Visita.DoesNotExist:
                visitas = False
            return render(request,'FitApp/homeAdminFiltroReporteSucursalVisitas.html',{'sucursal':sucursal,'visitas':visitas,'inicio':inicio,'final':final,'inicioF':inicioF,'finalF':finalF})
        else:
            return HttpResponseRedirect('/homeAdminReportes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginAdmin/')

class ReporteSucursalVisitas(View):
    def get(self,request,sucursal_id,inicio,final):
        if request.user.is_staff and request.user.is_authenticated:
            try:
                sucursal = Sucursal.objects.get(id=sucursal_id)
            except Sucursal.DoesNotExist:
                sucursal = False
            if sucursal:
                try:
                    visitas = Visita.objects.filter(sucursal=sucursal,fecha__range=(inicio,final))
                except Visita.DoesNotExist:
                    visitas = False
                if visitas:
                    filename = "Reporte_Pagos_Sucursal.xlsx"
                    wb = xlsxwriter.Workbook(filename)
                    center = wb.add_format({'align':'center'})
                    format = wb.add_format({'align':'center'})
                    format.set_text_wrap()
                    gris = wb.add_format({'font_color':'#9e9e9e'})
                    header = wb.add_format({'font_color':'white','align': 'center','fg_color': '#3f3f3f'})
                    body = wb.add_format({'font_color':'black','align': 'center','fg_color': '#ededed','border':1,'border_color':'#ffffff'})
                    sheet = wb.add_worksheet(u'Subscripciones')
                    sheet.write(0,0,u'ID',header)
                    sheet.write(0,1,u'CLIENTE',header)
                    sheet.write(0,2,u'FECHA',header)
                    sheet.write(0,3,u'HORA',header)
                    sheet.set_column('A:A', 20)
                    sheet.set_column('B:B', 30)
                    sheet.set_column('C:C', 30)
                    sheet.set_column('D:D', 30)
                    sheet.protect()
                    row = 0
                    for v in visitas:
                        row += 1
                        sheet.write(row,0,v.id,body)
                        sheet.write(row,1,v.cliente.nombre+' '+v.cliente.apellido,body)
                        sheet.write(row,2,v.fecha.strftime('%d-%m-%Y'),body)
                        sheet.write(row,3,v.hora.strftime('%I:%M %p'),body)
                    wb.close()
                    return HttpResponse(open(filename,'r').read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                else:
                    respuesta = 'Sin resultados.'
                    return HttpResponse(respuesta, content_type="text/plain")
            else:
                respuesta = 'Sin resultados.'
                return HttpResponse(respuesta, content_type="text/plain")
        else:
            respuesta = 'Sin resultados.'
            return HttpResponse(respuesta, content_type="text/plain")

def logoutAdmin(request):
    logout(request)
    return HttpResponseRedirect('/loginAdmin/')

def loginClub(request):
	next = request.GET.get('next', '/homeClub/')
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if not request.user.is_staff:
					return HttpResponseRedirect('/homeClub/')
				else:
					return render(request,'FitApp/loginClub.html',{'message':'User does not exist'})
			else:
				return HttpResponse("Inactive user.")
		else:
			return render(request,'FitApp/loginClub.html',{'message':'User does not exist'})
	if request.user.is_authenticated():
		if not request.user.is_staff:
			return HttpResponseRedirect('/homeClub/')
		else:
			return render(request,'FitApp/loginClub.html',{'message':'User does not exist'})
	return render(request,'FitApp/loginClub.html')

def homeClub(request):
    if not request.user.is_staff and request.user.is_authenticated:
    	user = request.user
        try:
            club = Club.objects.get(user=user)
        except Club.DoesNotExist:
            club = False
        if club:
            return render(request,'FitApp/homeClub.html',{'user':user,'club':club})
        else:
            logout(request)
            return HttpResponseRedirect('/loginClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def checkTerminosClub(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            club_id = request.POST['club']
            try:
                aceptar = request.POST['aceptar']
            except MultiValueDictKeyError:
                aceptar = False
            if aceptar:
                try:
                    club = Club.objects.get(id=club_id)
                except Club.DoesNotExist:
                    club = False
                if club:
                    hoy = date.today()
                    club.Legal = True
                    club.fechaLegal = hoy
                    club.save()
                    return HttpResponseRedirect('/homeClub/')
                else:
                    return HttpResponseRedirect('/homeClub/')
            else:
                return HttpResponseRedirect('/homeClub/')
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        return HttpResponseRedirect('/loginClub/')

def clubPerfil(request):
    if not request.user.is_staff and request.user.is_authenticated:
    	user = request.user
        try:
            club = Club.objects.get(user=user)
        except Club.DoesNotExist:
            club = False
        if club:
            form = cropFotoClub(instance=club)
            return render(request,'FitApp/homeClubPerfil.html',{'user':user,'club':club,'form':form})
        else:
            logout(request)
            return HttpResponseRedirect('/loginClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def recortarFotoClub2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        clubID = request.POST['club']
        club = Club.objects.get(id=clubID)
        form = cropFotoClub(instance=club)
        if request.method == "POST":
            form = cropFotoClub(request.POST,request.FILES,instance=club)
            if form.is_valid():
                thumbnailer = get_thumbnailer(club.foto)
                thumbnailer.delete_thumbnails()
                foto = form.cleaned_data['foto']
                if foto:
					club.foto = foto
					club.fotocrop = 0
                fotocrop = form.cleaned_data['fotocrop']
                club.fotocrop = fotocrop
                club.save()
                thumbnail_url = get_thumbnailer(club.foto).get_thumbnail({'size': (200, 200),'box': club.fotocrop,'crop': True,'detail': True,}).url
                cropURL = thumbnail_url
                club.cropURL = cropURL
                club.save()
                url = '/homeClub/Perfil/'
                return HttpResponseRedirect(url)
            else:
                url = '/homeClub/Perfil/'
                return HttpResponseRedirect(url)
        else:
            url = '/homeClub/Perfil/'
            return HttpResponseRedirect(url)
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def editClub2(request):
    if not request.user.is_staff and request.user.is_authenticated:
    	if request.method == "POST":
            clubID = request.POST['club']
            club = Club.objects.get(id=clubID)
            nombre = request.POST['nombre']
            try:
                RFC = request.POST['RFC']
            except MultiValueDictKeyError:
                RFC = '...'
            try:
                banco = request.POST['banco']
            except MultiValueDictKeyError:
                banco = '...'
            try:
                tarjetahabiente = request.POST['tarjetahabiente']
            except MultiValueDictKeyError:
                tarjetahabiente = '...'
            try:
                numCuenta = request.POST['numCuenta']
            except MultiValueDictKeyError:
                numCuenta = '...'
            try:
                paginaWeb = request.POST['paginaWeb']
            except MultiValueDictKeyError:
                paginaWeb = '...'
            try:
                facebook = request.POST['facebook']
            except MultiValueDictKeyError:
                facebook = '...'
            try:
                instagram = request.POST['instagram']
            except MultiValueDictKeyError:
                instagram = '...'
            try:
                twitter = request.POST['twitter']
            except MultiValueDictKeyError:
                twitter = '...'
            try:
                codigoClub = request.POST['codigoClub']
            except MultiValueDictKeyError:
                codigoClub = '...'
            try:
                codigoRepresentante = request.POST['codigoRepresentante']
            except MultiValueDictKeyError:
                codigoRepresentante = '...'
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            correo = request.POST['correo']
            try:
                foto = request.FILES['foto']
            except MultiValueDictKeyError:
                foto = False
            club.nombre = nombre
            club.RFC = RFC
            club.banco = banco
            club.tarjetahabiente = tarjetahabiente
            club.numCuenta = numCuenta
            club.paginaWeb = paginaWeb
            club.facebook = facebook
            club.instagram = instagram
            club.twitter = twitter
            club.codigoClub = codigoClub
            club.codigoRepresentante = codigoRepresentante
            club.direccion = direccion
            club.telefono = telefono
            correoActual = club.correo
            if not correo == correoActual:
                club.correo = correo
                user = club.user
                user.username = correo
                user.email = correo
                user.save()
            club.save()
            if foto:
                fotoActual = club.foto.name
                if fotoActual == 'default/club.png':
                    club.foto = foto
                    club.save()
                else:
                    os.remove(club.foto.path)
                    club.foto = foto
                    club.save()
            return HttpResponseRedirect('/homeClub/Perfil/')
        else:
            return HttpResponseRedirect('/homeClub/Perfil/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def clubSucursales(request,club_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            club = Club.objects.get(id=club_id)
        except Club.DoesNotExist:
            club = False
        if club:
            dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
            try:
                sucursalesT = Sucursal.objects.filter(club=club)
            except Sucursal.DoesNotExist:
                sucursalesT = False
            try:
                sucursales = Sucursal.objects.filter(club=club).order_by('id')
            except Sucursal.DoesNotExist:
                sucursales = False
            page = request.GET.get('page', 1)
            paginator = Paginator(sucursales,50)
            try:
                sucursales = paginator.page(page)
            except PageNotAnInteger:
                sucursales = paginator.page(1)
            except EmptyPage:
                sucursales = paginator.page(paginator.num_pages)
            sucursalDatos = []
            sucursalFotos = []
            sucursalHorario = []
            sucursalCiudades = []
            clubServicios = []
            clubServiciosDisponbles = []
            clubActividades = []
            clubActividadesDisponibles = []
            sucursalRegistrosHorario = []
            sucursalUsuarios = []
            if sucursales:
                for s in sucursales:
                    try:
                        usuarios = Usuario.objects.filter(sucursal=s)
                    except Usuario.DoesNotExist:
                        usuarios = False
                    try:
                        fotos = Foto.objects.filter(sucursal=s)
                    except Foto.DoesNotExist:
                        fotos = False
                    if fotos:
                        sucursalFotos.append((s,fotos))
                    else:
                        sucursalFotos.append((s,None))
                    try:
                        horario = Horario.objects.get(sucursal=s)
                    except Horario.DoesNotExist:
                        horario = False
                    if horario:
                        sucursalHorario.append((s,horario))
                    else:
                        sucursalHorario.append((s,None))
                    if not usuarios and not fotos and not horario:
                        sucursalDatos.append((s,False))
                    else:
                        sucursalDatos.append((s,True))
                    if horario:
                        tipo = horario.tipo
                        if dias:
                            for d in dias:
                                if tipo == u'Corrido':
                                    try:
                                        registros = RegistroHorario.objects.get(sucursal=s,dia=d)
                                    except RegistroHorario.DoesNotExist:
                                        registros = False
                                    if registros:
                                        sucursalRegistrosHorario.append((s,d,tipo,registros))
                                    else:
                                        sucursalRegistrosHorario.append((s,d,tipo,None))
                                else:
                                    try:
                                        registros = RegistroHorario.objects.filter(sucursal=s,dia=d)
                                    except RegistroHorario.DoesNotExist:
                                        registros = False
                                    if registros:
                                        sucursalRegistrosHorario.append((s,d,tipo,registros))
                                    else:
                                        sucursalRegistrosHorario.append((s,d,tipo,None))
                    try:
                        ciudades = Ciudad.objects.filter(estado=s.estado)
                    except Ciudad.DoesNotExist:
                        ciudades = False
                    if ciudades:
                        sucursalCiudades.append((s,ciudades))
                    else:
                        sucursalCiudades.append((s,None))
                    try:
                        relacionesServ = ServicioClub.objects.filter(sucursal=s)
                    except ServicioClub.DoesNotExist:
                        relacionesServ = False
                    if relacionesServ:
                        clubServicios.append((s,relacionesServ))
                    else:
                        clubServicios.append((s,None))
                    try:
                        relacionesAct = ActividadClub.objects.filter(sucursal=s)
                    except ActividadClub.DoesNotExist:
                        relacionesAct = False
                    if relacionesAct:
                        clubActividades.append((s,relacionesAct))
                    else:
                        clubActividades.append((s,None))
            try:
                estados = Estado.objects.all()
            except Estado.DoesNotExist:
                estados = False
            try:
                actividadesHorarios = ActividadHorario.objects.all()
            except ActividadHorario.DoesNotExist:
                actividadesHorarios = False
            try:
                clubActividadesT = ActividadClub.objects.all()
            except ActividadClub.DoesNotExist:
                clubActividadesT = False
            clubActividadHorarios = []
            if clubActividadesT:
                for cAct in clubActividadesT:
                    try:
                        horarios = ActividadHorario.objects.filter(actividadClub=cAct)
                    except ActividadHorario.DoesNotExist:
                        horarios = False
                    numHorarios = 0
                    if horarios:
                        numHorarios = len(horarios)
                        clubActividadHorarios.append((cAct,horarios,numHorarios))
                    else:
                        clubActividadHorarios.append((cAct,None,numHorarios))
            try:
                servicios = Servicio.objects.all()
            except Servicio.DoesNotExist:
                servicios = False
            try:
                actividades = Actividad.objects.all()
            except Actividad.DoesNotExist:
                actividades
            if clubServicios:
                for sucursal,serviciosSel in clubServicios:
                    if not serviciosSel == None:
                        listaSSel = []
                        for s in serviciosSel:
                            listaSSel.append(s.servicio.id)
                        listaS = []
                        if servicios:
                            for s in servicios:
                                listaS.append(s.id)
                        serviciosDisponbles = [elem for elem in listaS if elem not in listaSSel]
                        serviciosDisponblesDos = []
                        if serviciosDisponbles:
                            for s in serviciosDisponbles:
                                try:
                                    srv = Servicio.objects.get(id=s)
                                except Servicio.DoesNotExist:
                                    srv = False
                                if srv:
                                    serviciosDisponblesDos.append(srv)
                        clubServiciosDisponbles.append((sucursal,serviciosDisponblesDos))
                    else:
                        clubServiciosDisponbles.append((sucursal,servicios))
            if clubActividades:
                for sucursal,actividadesSel in clubActividades:
                    if not actividadesSel == None:
                        listaASel = []
                        for a in actividadesSel:
                            listaASel.append(a.actividad.id)
                        listaA = []
                        if actividades:
                            for a in actividades:
                                listaA.append(a.id)
                        actividadesDisponibles = [elem for elem in listaA if elem not in listaASel]
                        actividadesDisponiblesDos = []
                        if actividadesDisponibles:
                            for a in actividadesDisponibles:
                                try:
                                    act = Actividad.objects.get(id=a)
                                except Actividad.DoesNotExist:
                                    act = False
                                if act:
                                    actividadesDisponiblesDos.append(act)
                        clubActividadesDisponibles.append((sucursal,actividadesDisponiblesDos))
                    else:
                        clubActividadesDisponibles.append((sucursal,actividades))
            try:
                registrosH = RegistroHorario.objects.all()
            except RegistroHorario.DoesNotExist:
                registrosH = False
            return render(request,'FitApp/homeClubSucursales.html',{'dias':dias,'club':club,'sucursales':sucursales,'sucursalesT':sucursalesT,'sucursalDatos':sucursalDatos,'sucursalFotos':sucursalFotos,'estados':estados,'sucursalCiudades':sucursalCiudades,'servicios':servicios,'actividades':actividades,'clubServicios':clubServicios,'clubServiciosDisponbles':clubServiciosDisponbles,'clubActividades':clubActividades,'clubActividadesDisponibles':clubActividadesDisponibles,'clubActividadHorarios':clubActividadHorarios,'actividadesHorarios':actividadesHorarios,'clubActividadesT':clubActividadesT,'sucursalHorario':sucursalHorario,'sucursalRegistrosHorario':sucursalRegistrosHorario,'registrosH':registrosH})
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def addSucursal2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            clubID = request.POST['club']
            club = Club.objects.get(id=clubID)
            nombre = request.POST['nombre']
            try:
                descripcion = request.POST['descripcion']
            except MultiValueDictKeyError:
                descripcion = None
            try:
                tips = request.POST['tips']
            except MultiValueDictKeyError:
                tips = None
            correo = request.POST['correo']
            telefono = request.POST['telefono']
            estadoID = request.POST['estado']
            estado = Estado.objects.get(id=estadoID)
            ciudadID = request.POST['ciudad']
            ciudad = Ciudad.objects.get(id=ciudadID,estado=estado)
            municipio = request.POST['municipio']
            calle = request.POST['calle']
            numExt = request.POST['numExt']
            try:
                numInt = request.POST['numInt']
            except MultiValueDictKeyError:
                numInt = '...'
            colonia = request.POST['colonia']
            cp = request.POST['cp']
            try:
                logo = request.FILES['logo']
            except MultiValueDictKeyError:
                logo = False
            try:
                latitud = request.POST['latitud']
            except MultiValueDictKeyError:
                latitud = '25.4595197'
            try:
                longitud = request.POST['longitud']
            except MultiValueDictKeyError:
                longitud = '-100.9819936'
            try:
                servicios = request.POST.getlist('servicios')
            except MultiValueDictKeyError:
                servicios = False
            try:
                actividades = request.POST.getlist('actividades')
            except MultiValueDictKeyError:
                actividades = False
            mensualidad = request.POST['mensualidad']
            repetido = False
            try:
                repetido = Sucursal.objects.get(club=club,nombre=nombre,correo=correo,telefono=telefono,estado=estado,ciudad=ciudad,municipio=municipio,calle=calle,numExt=numExt,numInt=numInt,colonia=colonia,cp=cp,latitud=latitud,longitud=longitud)
            except Sucursal.DoesNotExist:
                repetido = False
            if not repetido:
                if logo:
                    sucursal = Sucursal(club=club,nombre=nombre,descripcion=descripcion,tips=tips,correo=correo,telefono=telefono,estado=estado,ciudad=ciudad,municipio=municipio,calle=calle,numExt=numExt,numInt=numInt,colonia=colonia,cp=cp,logo=logo,latitud=latitud,longitud=longitud,mensualidad=mensualidad)
                    sucursal.save()
                else:
                    sucursal = Sucursal(club=club,nombre=nombre,descripcion=descripcion,tips=tips,correo=correo,telefono=telefono,estado=estado,ciudad=ciudad,municipio=municipio,calle=calle,numExt=numExt,numInt=numInt,colonia=colonia,cp=cp,latitud=latitud,longitud=longitud,mensualidad=mensualidad)
                    sucursal.save()
                if servicios:
                    for s in servicios:
                        try:
                            servicio = Servicio.objects.get(id=s)
                        except Servicio.DoesNotExist:
                            servicio = False
                        if servicio:
                            try:
                                relacion = ServicioClub.objects.get(sucursal=sucursal,servicio=servicio)
                            except ServicioClub.DoesNotExist:
                                relacion = False
                            if not relacion:
                                relacionNueva = ServicioClub(sucursal=sucursal,servicio=servicio)
                                relacionNueva.save()
                if actividades:
                    for a in actividades:
                        try:
                            actividad = Actividad.objects.get(id=a)
                        except Actividad.DoesNotExist:
                            actividad = False
                        if actividad:
                            try:
                                relacion = ActividadClub.objects.get(sucursal=sucursal,actividad=actividad)
                            except ActividadClub.DoesNotExist:
                                relacion = False
                            if not relacion:
                                relacionNueva = ActividadClub(sucursal=sucursal,actividad=actividad)
                                relacionNueva.save()
                idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(club.id)
                namePlan = "Mensualidad Sucursal "+sucursal.nombre+", Club "+club.nombre
                amountCentavos = int(float(mensualidad))*100
                try:
                    planConektaSucursal = conekta.Plan.find(idPlan)
                except:
                    planConektaSucursal = False
                if not planConektaSucursal:
                    conekta.Plan.create({
                        "id":idPlan,
                        "name":namePlan,
                        "amount":amountCentavos,
                        "currency":"MXN",
                        "interval":"month",
                        "frequency":1,
                        "trial_period_days":0,
                        "expiry_count":1
                    })
                url = '/homeClub/'+str(club.id)+'/Sucursales/'
                return HttpResponseRedirect(url)
            else:
                error = u'Ya existe una sucursal con la misma información'
                return render(request,'FitApp/errorSucursal.html',{'error':error,'club':club})
        else:
            logout(request)
            return HttpResponseRedirect('/homeClub/')
    else:
        return HttpResponseRedirect('/loginClub/')

def editSucursal2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            nombre = request.POST['nombre']
            try:
                descripcion = request.POST['descripcion']
            except MultiValueDictKeyError:
                descripcion = None
            try:
                tips = request.POST['tips']
            except MultiValueDictKeyError:
                tips = None
            correo = request.POST['correo']
            telefono = request.POST['telefono']
            estadoID = request.POST['estado']
            estado = Estado.objects.get(id=estadoID)
            ciudadID = request.POST['ciudad']
            ciudad = Ciudad.objects.get(id=ciudadID,estado=estado)
            municipio = request.POST['municipio']
            calle = request.POST['calle']
            numExt = request.POST['numExt']
            try:
                numInt = request.POST['numInt']
            except MultiValueDictKeyError:
                numInt = '...'
            colonia = request.POST['colonia']
            cp = request.POST['cp']
            try:
                logo = request.FILES['logo']
            except MultiValueDictKeyError:
                logo = False
            try:
                latitud = request.POST['latitud']
            except MultiValueDictKeyError:
                latitud = '...'
            try:
                longitud = request.POST['longitud']
            except MultiValueDictKeyError:
                longitud = '...'
            try:
                servicios = request.POST.getlist('servicios')
            except MultiValueDictKeyError:
                servicios = False
            try:
                actividades = request.POST.getlist('actividades')
            except MultiValueDictKeyError:
                actividades = False
            mensualidad = request.POST['mensualidad']
            dia = request.POST['dia']
            estatus = int(request.POST['estatus'])
            if estatus == 1:
                sucursal.activa = True
            else:
                sucursal.activa = False
            sucursal.nombre = nombre
            sucursal.descripcion = descripcion
            sucursal.tips = tips
            correoActual = sucursal.correo
            if not correo == correoActual:
                sucursal.correo = correo
                sucursal.save()
            sucursal.telefono = telefono
            sucursal.estado = estado
            sucursal.ciudad = ciudad
            sucursal.municipio = municipio
            sucursal.calle = calle
            sucursal.numExt = numExt
            sucursal.numInt = numInt
            sucursal.colonia = colonia
            sucursal.cp = cp
            sucursal.latitud = latitud
            sucursal.longitud = longitud
            sucursal.mensualidad = mensualidad
            sucursal.dia = dia
            sucursal.save()
            idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id)
            namePlan = "Mensualidad Sucursal "+nombre+", Club "+sucursal.club.nombre
            amountCentavos = int(float(mensualidad))*100
            try:
                planConektaSucursal = conekta.Plan.find(idPlan)
            except:
                planConektaSucursal = False
            if planConektaSucursal:
                planConektaSucursal.update({
                    "name":namePlan,
                    "amount":amountCentavos
                })
            if logo:
                logoActual = sucursal.logo.name
                if logoActual == 'default/logo.jpg':
                    sucursal.logo = logo
                    sucursal.save()
                else:
                    os.remove(sucursal.logo.path)
                    sucursal.logo = logo
                    sucursal.save()
            serviciosSeleccionados = []
            serviciosNoSeleccionados = []
            if servicios:
                for s in servicios:
                    try:
                        servicio = Servicio.objects.get(id=s)
                    except Servicio.DoesNotExist:
                        servicio = False
                    if servicio:
                        serviciosSeleccionados.append(servicio.id)
                        try:
                            relacion = ServicioClub.objects.get(sucursal=sucursal,servicio=servicio)
                        except ServicioClub.DoesNotExist:
                            relacion = False
                        if not relacion:
                            relacionNueva = ServicioClub(sucursal=sucursal,servicio=servicio)
                            relacionNueva.save()
                serviciosTodos = []
                try:
                    serviciosT = Servicio.objects.all()
                except Servicio.DoesNotExist:
                    serviciosT = False
                if serviciosT:
                    for s in serviciosT:
                        serviciosTodos.append(s.id)
                serviciosNoSeleccionados = [elem for elem in serviciosTodos if elem not in serviciosSeleccionados]
                if serviciosNoSeleccionados:
                    for s in serviciosNoSeleccionados:
                        try:
                            servicio = Servicio.objects.get(id=s)
                        except Servicio.DoesNotExist:
                            servicio = False
                        if servicio:
                            try:
                                relacion = ServicioClub.objects.get(sucursal=sucursal,servicio=servicio)
                            except ServicioClub.DoesNotExist:
                                relacion = False
                            if relacion:
                                relacion.delete()
            else:
                try:
                    relaciones = ServicioClub.objects.filter(sucursal=sucursal)
                except ServicioClub.DoesNotExist:
                    relaciones = False
                if relaciones:
                    for r in relaciones:
                        r.delete()
            actividadesSeleccionadas = []
            actividadesNoSeleccionadas = []
            if actividades:
                for a in actividades:
                    try:
                        actividad = Actividad.objects.get(id=a)
                    except Actividad.DoesNotExist:
                        actividad = False
                    if actividad:
                        actividadesSeleccionadas.append(actividad.id)
                        try:
                            relacion = ActividadClub.objects.get(sucursal=sucursal,actividad=actividad)
                        except ActividadClub.DoesNotExist:
                            relacion = False
                        if not relacion:
                            relacionNueva = ActividadClub(sucursal=sucursal,actividad=actividad)
                            relacionNueva.save()
                actividadesTodas = []
                try:
                    actividadesT = Actividad.objects.all()
                except Actividad.DoesNotExist:
                    actividadesT = False
                if actividadesT:
                    for a in actividadesT:
                        actividadesTodas.append(a.id)
                actividadesNoSeleccionadas = [elem for elem in actividadesTodas if elem not in actividadesSeleccionadas]
                if actividadesNoSeleccionadas:
                    for a in actividadesNoSeleccionadas:
                        try:
                            actividad = Actividad.objects.get(id=a)
                        except Actividad.DoesNotExist:
                            actividad = False
                        if actividad:
                            try:
                                relacion = ActividadClub.objects.get(sucursal=sucursal,actividad=actividad)
                            except ActividadClub.DoesNotExist:
                                relacion = False
                            if relacion:
                                relacion.delete()
            else:
                try:
                    relaciones = ActividadClub.objects.filter(sucursal=sucursal)
                except ActividadClub.DoesNotExist:
                    relaciones = False
                if relaciones:
                    for r in relaciones:
                        r.delete()
            try:
                horario = Horario.objects.get(sucursal=sucursal)
            except Horario.DoesNotExist:
                horario = False
            if horario:
                numDiasActual = horario.numDias
                mensualidad = Dec(mensualidad)
                calculo = (mensualidad)/(numDiasActual*4)
                calculoComision = (10*calculo)/100
                totalDia = calculo + calculoComision
                sucursal.dia = Dec(totalDia)
                sucursal.save()
            idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id)
            namePlan = "Mensualidad Sucursal "+sucursal.nombre+", Club "+sucursal.club.nombre
            amountCentavos = int(float(mensualidad))*100
            try:
                planConektaSucursal = conekta.Plan.find(idPlan)
            except:
                planConektaSucursal = False
            if not planConektaSucursal:
                conekta.Plan.create({
                    "id":idPlan,
                    "name":namePlan,
                    "amount":amountCentavos,
                    "currency":"MXN",
                    "interval":"month",
                    "frequency":1,
                    "trial_period_days":0,
                    "expiry_count":1
                })
            else:
                planConektaSucursal.update({
                    "id": idPlan,
                    "name": namePlan,
                    "amount": amountCentavos
                })
            url = '/homeClub/'+str(sucursal.club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def editEstatusSucursal2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            estatus = int(request.POST['estatus'])
            if estatus == 1:
                sucursal.activa = True
            else:
                sucursal.activa = False
            sucursal.save()
            url = '/homeClub/'+str(sucursal.club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def recortarFotoSucursalFormulario2(request,club_id,sucursal_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            club = Club.objects.get(id=club_id)
        except Club.DoesNotExist:
            club = False
        if club:
            try:
                sucursal = Sucursal.objects.get(id=sucursal_id,club=club)
            except Sucursal.DoesNotExist:
                sucursal = False
            if sucursal:
                form = cropLogoSucursal(instance=sucursal)
                return render(request,'FitApp/homeClubSucursalRecortarFoto.html',{'club':club,'sucursal':sucursal,'form':form})
            else:
                url = '/homeClub/'+str(club.id)+'/Sucursales/'
                return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def recortarFotoSucursal2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        sucursalID = request.POST['sucursal']
        sucursal = Sucursal.objects.get(id=sucursalID)
        form = cropLogoSucursal(instance=sucursal)
        if request.method == "POST":
            form = cropLogoSucursal(request.POST,request.FILES,instance=sucursal)
            if form.is_valid():
                thumbnailer = get_thumbnailer(sucursal.logo)
                thumbnailer.delete_thumbnails()
                logo = form.cleaned_data['logo']
                if logo:
                    sucursal.logo = logo
                    sucursal.logocrop = 0
                logocrop = form.cleaned_data['logocrop']
                sucursal.logocrop = logocrop
                sucursal.save()
                thumbnail_url = get_thumbnailer(sucursal.logo).get_thumbnail({'size': (200, 200),'box': sucursal.logocrop,'crop': True,'detail': True,}).url
                cropURL = thumbnail_url
                sucursal.cropURL = cropURL
                sucursal.save()
                url = '/homeClub/'+str(sucursal.club.id)+'/Sucursales/'
                return HttpResponseRedirect(url)
            else:
                url = '/homeClub/'+str(sucursal.club.id)+'/Sucursal/'+str(sucursal.id)+'/RecortarLogo/'
                return HttpResponseRedirect(url)
        else:
            url = '/homeClub/'+str(sucursal.club.id)+'/Sucursal/'+str(sucursal.id)+'/RecortarLogo/'
            return HttpResponseRedirect(url)
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def deleteSucursal2(request,sucursal_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            sucursal = Sucursal.objects.get(id=sucursal_id)
        except Sucursal.DoesNotExist:
            sucursal = False
        if sucursal:
            club = sucursal.club
            logoActual = sucursal.logo.name
            if not logoActual == 'default/logo.jpg':
                os.remove(sucursal.logo.path)
            idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id)
            try:
                planConekta = conekta.Plan.find(idPlan)
            except:
                planConekta = False
            if planConekta:
                planConekta.delete()
            try:
                fotos = Foto.objects.filter(sucursal=sucursal)
            except Foto.DoesNotExist:
                fotos = False
            if fotos:
                for f in fotos:
                    os.remove(f.archivo.path)
                    f.delete()
            try:
                usuarios = Usuario.objects.filter(sucursal=sucursal)
            except Usuario.DoesNotExist:
                usuarios = False
            if usuarios:
                for u in usuarios:
                    user = u.user
                    user.delete()
                    u.delete()
            sucursal.delete()
            url = '/homeClub/'+str(club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def addHorarioSucursal2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            repetido = False
            errores = []
            try:
                repetido = Horario.objects.get(sucursal=sucursal)
            except Horario.DoesNotExist:
                repetido = False
            if not repetido:
                lunes = False
                martes = False
                miercoles = False
                jueves = False
                viernes = False
                sabado = False
                domingo = False
                if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                    error = 'Debe seleccionar al menos un día en el horario.'
                    return render(request,'FitApp/errorHorarioSucursal2.html',{'error':error,'club':sucursal.club})
                else:
                    if lunesCheck:
                        lunes = True
                    else:
                        lunes = False
                    if martesCheck:
                        martes = True
                    else:
                        martes = False
                    if miercolesCheck:
                        miercoles = True
                    else:
                        miercoles = False
                    if juevesCheck:
                        jueves = True
                    else:
                        jueves = False
                    if viernesCheck:
                        viernes = True
                    else:
                        viernes = False
                    if sabadoCheck:
                        sabado = True
                    else:
                        sabado = False
                    if domingoCheck:
                        domingo = True
                    else:
                        domingo = False
                    tipoHorario = int(request.POST['tipoHorario'])
                    tipo = ''
                    if tipoHorario == 1:
                        tipo = u'Corrido'
                    else:
                        tipo = u'Mixto'
                    horario = Horario(sucursal=sucursal,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo,numDias=numDias,tipo=tipo)
                    horario.save()
                    if lunes:
                        dia = u'Lunes'
                        apertura = request.POST['lunesA']
                        cierre = request.POST['lunesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Lunes con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if martes:
                        dia = u'Martes'
                        apertura = request.POST['martesA']
                        cierre = request.POST['martesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Martes con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if miercoles:
                        dia = u'Miércoles'
                        apertura = request.POST['miercolesA']
                        cierre = request.POST['miercolesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Miércoles con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if jueves:
                        dia = u'Jueves'
                        apertura = request.POST['juevesA']
                        cierre = request.POST['juevesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Jueves con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if viernes:
                        dia = u'Viernes'
                        apertura = request.POST['viernesA']
                        cierre = request.POST['viernesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Viernes con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if sabado:
                        dia = u'Sábado'
                        apertura = request.POST['sabadoA']
                        cierre = request.POST['sabadoC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Sábado con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if domingo:
                        dia = u'Domingo'
                        apertura = request.POST['domingoA']
                        cierre = request.POST['domingoC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Domingo con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                if not errores:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    numDiasActual = horarioSuc.numDias
                    mensualidad = sucursal.mensualidad
                    calculo = (mensualidad)/(numDiasActual*4)
                    calculoComision = (10*calculo)/100
                    totalDia = calculo + calculoComision
                    sucursal.dia = Dec(totalDia)
                    sucursal.save()
                    url = '/homeClub/'+str(sucursal.club.id)+'/Sucursales/'
                    return HttpResponseRedirect(url)
                else:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    horarioSuc.delete()
                    error = 'Ha ocurrido uno o más errores al momento de registrar el horario, favor de revisarlos.'
                    return render(request,'FitApp/errorHorarioSucursalVarios2.html',{'error':error,'errores':json.dumps(errores),'club':horarioSuc.sucursal.club})
            else:
                error = 'Esta sucursal ya tiene un horario, registrado, si quieres editarlo usa el formulario de edición.'
                return render(request,'FitApp/errorHorarioSucursal2.html',{'error':error,'club':sucursal.club})
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def addHorarioMixtoSucursal2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            repetido = False
            errores = []
            try:
                repetido = Horario.objects.get(sucursal=sucursal)
            except Horario.DoesNotExist:
                repetido = False
            if not repetido:
                lunes = False
                martes = False
                miercoles = False
                jueves = False
                viernes = False
                sabado = False
                domingo = False
                if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                    error = 'Debe seleccionar al menos un día en el horario.'
                    return render(request,'FitApp/errorHorarioSucursal2.html',{'error':error,'club':sucursal.club})
                else:
                    if lunesCheck:
                        lunes = True
                    else:
                        lunes = False
                    if martesCheck:
                        martes = True
                    else:
                        martes = False
                    if miercolesCheck:
                        miercoles = True
                    else:
                        miercoles = False
                    if juevesCheck:
                        jueves = True
                    else:
                        jueves = False
                    if viernesCheck:
                        viernes = True
                    else:
                        viernes = False
                    if sabadoCheck:
                        sabado = True
                    else:
                        sabado = False
                    if domingoCheck:
                        domingo = True
                    else:
                        domingo = False
                    tipoHorario = int(request.POST['tipoHorario'])
                    tipo = ''
                    if tipoHorario == 1:
                        tipo = u'Corrido'
                    else:
                        tipo = u'Mixto'
                    horario = Horario(sucursal=sucursal,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo,numDias=numDias,tipo=tipo)
                    horario.save()
                    if lunes:
                        dia = u'Lunes'
                        apertura1 = request.POST['lunesA1']
                        cierre1 = request.POST['lunesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Lunes con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['lunesA2']
                        cierre2 = request.POST['lunesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Lunes con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if martes:
                        dia = u'Martes'
                        apertura1 = request.POST['martesA1']
                        cierre1 = request.POST['martesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Martes con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['martesA2']
                        cierre2 = request.POST['martesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Martes con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if miercoles:
                        dia = u'Miércoles'
                        apertura1 = request.POST['miercolesA1']
                        cierre1 = request.POST['miercolesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Miércoles con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['miercolesA2']
                        cierre2 = request.POST['miercolesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Miércoles con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if jueves:
                        dia = u'Jueves'
                        apertura1 = request.POST['juevesA1']
                        cierre1 = request.POST['juevesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Jueves con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['juevesA2']
                        cierre2 = request.POST['juevesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Jueves con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if viernes:
                        dia = u'Viernes'
                        apertura1 = request.POST['viernesA1']
                        cierre1 = request.POST['viernesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Viernes con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['viernesA2']
                        cierre2 = request.POST['viernesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Viernes con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if sabado:
                        dia = u'Sábado'
                        apertura1 = request.POST['sabadoA1']
                        cierre1 = request.POST['sabadoC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Sábado con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['sabadoA2']
                        cierre2 = request.POST['sabadoC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Sábado con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if domingo:
                        dia = u'Domingo'
                        apertura1 = request.POST['domingoA1']
                        cierre1 = request.POST['domingoC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Domingo con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['domingoA2']
                        cierre2 = request.POST['domingoC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Domingo con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                if not errores:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    numDiasActual = horarioSuc.numDias
                    mensualidad = sucursal.mensualidad
                    calculo = (mensualidad)/(numDiasActual*4)
                    calculoComision = (10*calculo)/100
                    totalDia = calculo + calculoComision
                    sucursal.dia = Dec(totalDia)
                    sucursal.save()
                    url = '/homeClub/'+str(sucursal.club.id)+'/Sucursales/'
                    return HttpResponseRedirect(url)
                else:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    horarioSuc.delete()
                    error = 'Ha ocurrido uno o más errores al momento de registrar el horario, favor de revisarlos.'
                    return render(request,'FitApp/errorHorarioSucursalVarios2.html',{'error':error,'errores':json.dumps(errores),'club':horarioSuc.sucursal.club})
            else:
                error = 'Esta sucursal ya tiene un horario, registrado, si quieres editarlo usa el formulario de edición.'
                return render(request,'FitApp/errorHorarioSucursal2.html',{'error':error,'club':sucursal.club})
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def editHorarioSucursal2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            horarioID = request.POST['horario']
            horario = Horario.objects.get(id=horarioID)
            sucursal = horario.sucursal
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                error = 'Debe seleccionar al menos un día en el horario.'
                return render(request,'FitApp/errorHorarioSucursal2.html',{'error':error,'club':horario.sucursal.club})
            lunes = False
            martes = False
            miercoles = False
            jueves = False
            viernes = False
            sabado = False
            domingo = False
            if lunesCheck:
                lunes = True
            else:
                lunes = False
            if martesCheck:
                martes = True
            else:
                martes = False
            if miercolesCheck:
                miercoles = True
            else:
                miercoles = False
            if juevesCheck:
                jueves = True
            else:
                jueves = False
            if viernesCheck:
                viernes = True
            else:
                viernes = False
            if sabadoCheck:
                sabado = True
            else:
                sabado = False
            if domingoCheck:
                domingo = True
            else:
                domingo = False
            horario.lunes = lunes
            horario.martes = martes
            horario.miercoles = miercoles
            horario.jueves = jueves
            horario.viernes = viernes
            horario.sabado = sabado
            horario.domingo = domingo
            horario.numDias = numDias
            horario.save()
            if lunesCheck:
                dia = u'Lunes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['lunesA']
                    cierre = request.POST['lunesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Lunes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if martesCheck:
                dia = u'Martes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['martesA']
                    cierre = request.POST['martesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Martes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if miercolesCheck:
                dia = u'Miércoles'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['miercolesA']
                    cierre = request.POST['miercolesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Miércoles'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if juevesCheck:
                dia = u'Jueves'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['juevesA']
                    cierre = request.POST['juevesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Jueves'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if viernesCheck:
                dia = u'Viernes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['viernesA']
                    cierre = request.POST['viernesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Viernes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if sabadoCheck:
                dia = u'Sábado'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['sabadoA']
                    cierre = request.POST['sabadoC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Sábado'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if domingoCheck:
                dia = u'Domingo'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['domingoA']
                    cierre = request.POST['domingoC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Domingo'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            horarioSuc = Horario.objects.get(id=horarioID)
            sucursal = horarioSuc.sucursal
            numDiasActual = horarioSuc.numDias
            mensualidad = sucursal.mensualidad
            calculo = (mensualidad)/(numDiasActual*4)
            calculoComision = (10*calculo)/100
            totalDia = calculo + calculoComision
            sucursal.dia = Dec(totalDia)
            sucursal.save()
            url = '/homeClub/'+str(horario.sucursal.club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def editHorarioMixtoSucursal2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            horarioID = request.POST['horario']
            horario = Horario.objects.get(id=horarioID)
            sucursal = horario.sucursal
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                error = 'Debe seleccionar al menos un día en el horario.'
                return render(request,'FitApp/errorHorarioSucursal2.html',{'error':error,'club':horario.sucursal.club})
            lunes = False
            martes = False
            miercoles = False
            jueves = False
            viernes = False
            sabado = False
            domingo = False
            if lunesCheck:
                lunes = True
            else:
                lunes = False
            if martesCheck:
                martes = True
            else:
                martes = False
            if miercolesCheck:
                miercoles = True
            else:
                miercoles = False
            if juevesCheck:
                jueves = True
            else:
                jueves = False
            if viernesCheck:
                viernes = True
            else:
                viernes = False
            if sabadoCheck:
                sabado = True
            else:
                sabado = False
            if domingoCheck:
                domingo = True
            else:
                domingo = False
            horario.lunes = lunes
            horario.martes = martes
            horario.miercoles = miercoles
            horario.jueves = jueves
            horario.viernes = viernes
            horario.sabado = sabado
            horario.domingo = domingo
            horario.numDias = numDias
            horario.save()
            if lunesCheck:
                dia = u'Lunes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['lunesA1']
                    cierre1 = request.POST['lunesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['lunesA2']
                    cierre2 = request.POST['lunesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Lunes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if martesCheck:
                dia = u'Martes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['martesA1']
                    cierre1 = request.POST['martesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['martesA2']
                    cierre2 = request.POST['martesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Martes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if miercolesCheck:
                dia = u'Miércoles'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['miercolesA1']
                    cierre1 = request.POST['miercolesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['miercolesA2']
                    cierre2 = request.POST['miercolesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Miércoles'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if juevesCheck:
                dia = u'Jueves'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['juevesA1']
                    cierre1 = request.POST['juevesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['juevesA2']
                    cierre2 = request.POST['juevesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Jueves'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if viernesCheck:
                dia = u'Viernes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['viernesA1']
                    cierre1 = request.POST['viernesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['viernesA2']
                    cierre2 = request.POST['viernesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Viernes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if sabadoCheck:
                dia = u'Sábado'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['sabadoA1']
                    cierre1 = request.POST['sabadoC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['sabadoA2']
                    cierre2 = request.POST['sabadoC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Sábado'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if domingoCheck:
                dia = u'Domingo'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['domingoA1']
                    cierre1 = request.POST['domingoC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['domingoA2']
                    cierre2 = request.POST['domingoC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Domingo'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            horarioSuc = Horario.objects.get(id=horarioID)
            sucursal = horarioSuc.sucursal
            numDiasActual = horarioSuc.numDias
            mensualidad = sucursal.mensualidad
            calculo = (mensualidad)/(numDiasActual*4)
            calculoComision = (10*calculo)/100
            totalDia = calculo + calculoComision
            sucursal.dia = Dec(totalDia)
            sucursal.save()
            url = '/homeClub/'+str(horario.sucursal.club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def editRegistroHorario2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            registroHorarioID = request.POST['registroHorario']
            registroHorario = RegistroHorario.objects.get(id=registroHorarioID)
            apertura = request.POST['apertura']
            cierre = request.POST['cierre']
            registroHorario.apertura = apertura
            registroHorario.cierre = cierre
            registroHorario.save()
            sucursal = registroHorario.sucursal
            url = '/homeClub/'+str(sucursal.club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def deleteHorarioSucursal2(request,horario_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            horario = Horario.objects.get(id=horario_id)
        except Horario.DoesNotExist:
            horario = False
        if horario:
            club = horario.sucursal.club
            sucursal = horario.sucursal
            horario.delete()
            sucursal.dia = 0
            sucursal.save()
            try:
                registros = RegistroHorario.objects.filter(sucursal=sucursal)
            except RegistroHorario.DoesNotExist:
                registros = False
            if registros:
                for r in registros:
                    r.delete()
            url = '/homeClub/'+str(club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def addFotoSucursal2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                foto = request.FILES['foto']
            except MultiValueDictKeyError:
                foto = False
            if foto:
                for f in request.FILES.getlist('foto'):
                    newFoto = Foto(sucursal=sucursal,archivo=f)
                    newFoto.save()
                url = '/homeClub/'+str(sucursal.club.id)+'/Sucursales/'
                return HttpResponseRedirect(url)
            else:
                error = 'Se requiere subir al menos una imagen.'
                return render(request,'FitApp/errorFotoSucursal2.html',{'error':error,'club':sucursal.club})
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def deleteFotoSucursal2(request,foto_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            foto = Foto.objects.get(id=foto_id)
        except Foto.DoesNotExist:
            foto = False
        if foto:
            club = foto.sucursal.club
            fotoActual = foto.archivo.name
            if not fotoActual == 'default/foto.png':
                os.remove(foto.archivo.path)
            foto.delete()
            url = '/homeClub/'+str(club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def addActividadHorario2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            actividadClubID = request.POST['actividadClub']
            actividadClub = ActividadClub.objects.get(id=actividadClubID)
            horaInicio = request.POST['horaInicio']
            horaFin = request.POST['horaFin']
            try:
                lunes = request.POST['lunes']
            except MultiValueDictKeyError:
                lunes = False
            try:
                martes = request.POST['martes']
            except MultiValueDictKeyError:
                martes = False
            try:
                miercoles = request.POST['miercoles']
            except MultiValueDictKeyError:
                miercoles = False
            try:
                jueves = request.POST['jueves']
            except MultiValueDictKeyError:
                jueves = False
            try:
                viernes = request.POST['viernes']
            except MultiValueDictKeyError:
                viernes = False
            try:
                sabado = request.POST['sabado']
            except MultiValueDictKeyError:
                sabado = False
            try:
                domingo = request.POST['domingo']
            except MultiValueDictKeyError:
                domingo = False
            if not lunes and not martes and not miercoles and not jueves and not viernes and not sabado and not domingo:
                error = u'Debes seleccionar al menos un día de la semana para el horario a registrar.'
                return render(request,'FitApp/errorHorarioActividad2.html',{'error':error,'club':actividadClub.sucursal.club})
            repetido = False
            try:
                repetido = ActividadHorario.objects.get(actividadClub=actividadClub,horaInicio=horaInicio,horaFin=horaFin,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo)
            except ActividadHorario.DoesNotExist:
                repetido = False
            if not repetido:
                actividadHorario = ActividadHorario(actividadClub=actividadClub,horaInicio=horaInicio,horaFin=horaFin,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo)
                actividadHorario.save()
                url = '/homeClub/'+str(actividadClub.sucursal.club.id)+'/Sucursales/'
                return HttpResponseRedirect(url)
            else:
                error = u'Ya hay un registro de horario para esta actividad con los mismos datos, favor de verificar.'
                return render(request,'FitApp/errorHorarioActividad2.html',{'error':error,'club':actividadClub.sucursal.club})
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def editActividadHorario2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            actividadHorarioID = request.POST['actividadHorario']
            actividadHorario = ActividadHorario.objects.get(id=actividadHorarioID)
            horaInicio = request.POST['horaInicio']
            horaFin = request.POST['horaFin']
            try:
                lunes = request.POST['lunes']
            except MultiValueDictKeyError:
                lunes = False
            try:
                martes = request.POST['martes']
            except MultiValueDictKeyError:
                martes = False
            try:
                miercoles = request.POST['miercoles']
            except MultiValueDictKeyError:
                miercoles = False
            try:
                jueves = request.POST['jueves']
            except MultiValueDictKeyError:
                jueves = False
            try:
                viernes = request.POST['viernes']
            except MultiValueDictKeyError:
                viernes = False
            try:
                sabado = request.POST['sabado']
            except MultiValueDictKeyError:
                sabado = False
            try:
                domingo = request.POST['domingo']
            except MultiValueDictKeyError:
                domingo = False
            actividadHorario.horaInicio = horaInicio
            actividadHorario.horaFin = horaFin
            actividadHorario.lunes = lunes
            actividadHorario.martes = martes
            actividadHorario.miercoles = miercoles
            actividadHorario.jueves = jueves
            actividadHorario.viernes = viernes
            actividadHorario.sabado = sabado
            actividadHorario.domingo = domingo
            actividadHorario.save()
            url = '/homeClub/'+str(actividadHorario.actividadClub.sucursal.club.id)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def deleteActividadHorario2(request,actividadHorario_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            actividadHorario = ActividadHorario.objects.get(id=actividadHorario_id)
        except ActividadHorario.DoesNotExist:
            actividadHorario = False
        if actividadHorario:
            idClub = actividadHorario.actividadClub.sucursal.club.id
            actividadHorario.delete()
            url = '/homeClub/'+str(idClub)+'/Sucursales/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def sucursalUsuarios2(request,club_id,sucursal_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            club = Club.objects.get(id=club_id)
        except Club.DoesNotExist:
            club = False
        if club:
            try:
                sucursal = Sucursal.objects.get(id=sucursal_id,club=club)
            except Sucursal.DoesNotExist:
                sucursal = False
            if sucursal:
                try:
                    usuarios = Usuario.objects.filter(sucursal=sucursal).order_by('id')
                except Usuario.DoesNotExist:
                    usuarios = False
                page = request.GET.get('page', 1)
                paginator = Paginator(usuarios,50)
                try:
                    usuarios = paginator.page(page)
                except PageNotAnInteger:
                    usuarios = paginator.page(1)
                except EmptyPage:
                    usuarios = paginator.page(paginator.num_pages)
                return render(request,'FitApp/homeClubSucursalUsuarios.html',{'club':sucursal.club,'sucursal':sucursal,'usuarios':usuarios})
            else:
                return HttpResponseRedirect('/homeClub/')
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def addUsuario2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            nombre = request.POST['nombre']
            correo = request.POST['correo']
            password = request.POST['password']
            mailUsado = False
            try:
                mailUsado = User.objects.get(email=correo)
            except User.DoesNotExist:
                mailUsado = False
            if not mailUsado:
                user = User.objects.create_user(username=correo,email=correo)
                user.set_password(password)
                user.save()
                repetido = False
                try:
                    repetido = Usuario.objects.get(user=user,sucursal=sucursal,nombre=nombre)
                except Usuario.DoesNotExist:
                    repetido = False
                if not repetido:
                    usuario = Usuario(user=user,sucursal=sucursal,nombre=nombre,activo=True)
                    usuario.save()
                    url = '/homeClub/'+str(sucursal.club.id)+'/Sucursal/'+str(sucursal.id)+'/Usuarios/'
                    return HttpResponseRedirect(url)
                else:
                    error = u'Este usuario ya existe.'
                    return render(request,'FitApp/errorUsuario2.html',{'error':error,'club':sucursal.club,'sucursal':sucursal})
            else:
                error = u'Este correo ya esta en uso, favor de utilizar uno diferente.'
                return render(request,'FitApp/errorUsuario2.html',{'error':error,'club':sucursal.club,'sucursal':sucursal})
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def editUsuario2(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            usuarioID = request.POST['usuario']
            usuario = Usuario.objects.get(id=usuarioID)
            nombre = request.POST['nombre']
            correo = request.POST['correo']
            try:
                password = request.POST['password']
            except MultiValueDictKeyError:
                password = False
            try:
                confirmarPassword = request.POST['confirmarPassword']
            except MultiValueDictKeyError:
                confirmarPassword = False
            try:
                activo = request.POST['activo']
            except MultiValueDictKeyError:
                activo = False
            usuario.nombre = nombre
            usuario.activo = activo
            usuario.save()
            user = usuario.user
            emailActual = user.email
            if not correo == emailActual:
                user.username = correo
                user.email = correo
                user.save()
            if password and confirmarPassword:
                if not password == confirmarPassword:
                    user.set_password(confirmarPassword)
                    user.save()
                else:
                    error = u'La contraseña nueva no puede ser igual a la contraseña actual.'
                    return render(request,'FitApp/errorUsuario2.html',{'error':error,'club':usuario.sucursal.club,'sucursal':usuario.sucursal})
            url = '/homeClub/'+str(usuario.sucursal.club.id)+'/Sucursal/'+str(usuario.sucursal.id)+'/Usuarios/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def deleteUsuario2(request,usuario_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            usuario = False
        if usuario:
            user = usuario.user
            club = usuario.sucursal.club
            sucursal = usuario.sucursal
            user.delete()
            usuario.delete()
            url = '/homeClub/'+str(club.id)+'/Sucursal/'+str(sucursal.id)+'/Usuarios/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def reservacionesClub(request):
    if not request.user.is_staff and request.user.is_authenticated:
        user = request.user
        try:
            club = Club.objects.get(user=user)
        except Club.DoesNotExist:
            club = False
        if club:
            try:
                sucursales = Sucursal.objects.filter(club=club)
            except Sucursal.DoesNotExist:
                sucursales = False
            reservaciones = []
            try:
                sesiones = Sesion.objects.filter(sucursal__club=club)
            except Sesion.DoesNotExist:
                sesiones = False
            if sesiones:
                for s in sesiones:
                    fechaCaducidad = s.caducidad
                    sesiones = int(s.sesiones)
                    sesionesRestantes = int(s.sesionesRestantes)
                    fechaContratacion =  (fechaCaducidad - timedelta(sesiones)).strftime('%d-%m-%Y')
                    fechaCaducidad = s.caducidad.strftime('%d-%m-%Y')
                    res = {
                        'tipo':'Sesiones',
                        'sucursal':s.sucursal,
                        'cliente':s.cliente,
                        'total':s.total,
                        'fechaContratacion':fechaContratacion,
                        'fechaCaducidad':fechaCaducidad,
                        'activo':s.activo,
                    }
                    reservaciones.append(res)
            try:
                subscripciones = Subscripcion.objects.filter(sucursal__club=club)
            except Subscripcion.DoesNotExist:
                subscripciones = False
            if subscripciones:
                for s in subscripciones:
                    fechaCaducidad = s.fechaRenovacion.strftime('%d-%m-%Y')
                    fechaContratacion = s.fechaSubscripcion.strftime('%d-%m-%Y')
                    res = {
                        'tipo':'Subscripción mensual',
                        'sucursal':s.sucursal,
                        'cliente':s.cliente,
                        'total':s.totalCobrar,
                        'totalGym':s.totalGym,
                        'fechaContratacion':fechaContratacion,
                        'fechaCaducidad':fechaCaducidad,
                        'activo':s.activa,
                    }
                    reservaciones.append(res)
            page = request.GET.get('page', 1)
            paginator = Paginator(reservaciones,50)
            try:
                reservaciones = paginator.page(page)
            except PageNotAnInteger:
                reservaciones = paginator.page(1)
            except EmptyPage:
                reservaciones = paginator.page(paginator.num_pages)
            return render(request,'FitApp/homeClubReservaciones.html',{'club':club,'user':user,'reservaciones':reservaciones})
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def pagosClub(request):
    if not request.user.is_staff and request.user.is_authenticated:
        user = request.user
        try:
            club = Club.objects.get(user=user)
        except Club.DoesNotExist:
            club = False
        if club:
            try:
                pagos = PagoSucursal.objects.filter(sucursal__club=club).order_by('-fecha')
            except PagoSucursal.DoesNotExist:
                pagos = False
            page = request.GET.get('page', 1)
            paginator = Paginator(pagos,50)
            try:
                pagos = paginator.page(page)
            except PageNotAnInteger:
                pagos = paginator.page(1)
            except EmptyPage:
                pagos = paginator.page(paginator.num_pages)
            return render(request,'FitApp/homeClubPagos.html',{'club':club,'user':user,'pagos':pagos})
        else:
            return HttpResponseRedirect('/homeClub/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginClub/')

def logoutClub(request):
    logout(request)
    return HttpResponseRedirect('/loginClub/')

def loginSucursal(request):
	next = request.GET.get('next', '/homeSucursal/')
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if not request.user.is_staff:
					return HttpResponseRedirect('/homeSucursal/')
				else:
					return render(request,'FitApp/loginSucursal.html',{'message':'User does not exist'})
			else:
				return HttpResponse("Inactive user.")
		else:
			return render(request,'FitApp/loginSucursal.html',{'message':'User does not exist'})
	if request.user.is_authenticated():
		if not request.user.is_staff:
			return HttpResponseRedirect('/homeSucursal/')
		else:
			return render(request,'FitApp/loginSucursal.html',{'message':'User does not exist'})
	return render(request,'FitApp/loginSucursal.html')

def homeSucursal(request):
    if not request.user.is_staff and request.user.is_authenticated:
    	user = request.user
        try:
            usuario = Usuario.objects.get(user=user)
        except Usuario.DoesNotExist:
            usuario = False
        if usuario:
            sucursal = usuario.sucursal
            return render(request,'FitApp/homeSucursal.html',{'user':user,'usuario':usuario,'sucursal':sucursal})
        else:
            logout(request)
            return HttpResponseRedirect('/loginSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def checkTerminosSucursal(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            usuario_id = request.POST['usuario']
            try:
                aceptar = request.POST['aceptar']
            except MultiValueDictKeyError:
                aceptar = False
            if aceptar:
                try:
                    usuario = Usuario.objects.get(id=usuario_id)
                except Usuario.DoesNotExist:
                    usuario = False
                if usuario:
                    hoy = date.today()
                    usuario.Legal = True
                    usuario.fechaLegal = hoy
                    usuario.save()
                    return HttpResponseRedirect('/homeSucursal/')
                else:
                    return HttpResponseRedirect('/homeSucursal/')
            else:
                return HttpResponseRedirect('/homeSucursal/')
        else:
            return HttpResponseRedirect('/homeSucursal/')
    else:
        return HttpResponseRedirect('/loginSucursal/')

def sucursalPerfil(request):
    if not request.user.is_staff and request.user.is_authenticated:
    	user = request.user
        try:
            usuario = Usuario.objects.get(user=user)
        except Usuario.DoesNotExist:
            usuario = False
        if usuario:
            sucursales = [usuario.sucursal]
            if sucursales:
                dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
                sucursalDatos = []
                sucursalFotos = []
                sucursalHorario = []
                sucursalCiudades = []
                clubServicios = []
                clubServiciosDisponbles = []
                clubActividades = []
                clubActividadesDisponibles = []
                sucursalRegistrosHorario = []
                if sucursales:
                    for s in sucursales:
                        try:
                            fotos = Foto.objects.filter(sucursal=s)
                        except Foto.DoesNotExist:
                            fotos = False
                        if fotos:
                            sucursalDatos.append((s,True))
                            sucursalFotos.append((s,fotos))
                        else:
                            sucursalDatos.append((s,False))
                            sucursalFotos.append((s,None))
                        try:
                            horario = Horario.objects.get(sucursal=s)
                        except Horario.DoesNotExist:
                            horario = False
                        if horario:
                            sucursalHorario.append((s,horario))
                        else:
                            sucursalHorario.append((s,None))
                        if horario:
                            tipo = horario.tipo
                            if dias:
                                for d in dias:
                                    if tipo == u'Corrido':
                                        try:
                                            registros = RegistroHorario.objects.get(sucursal=s,dia=d)
                                        except RegistroHorario.DoesNotExist:
                                            registros = False
                                        if registros:
                                            sucursalRegistrosHorario.append((s,d,tipo,registros))
                                        else:
                                            sucursalRegistrosHorario.append((s,d,tipo,None))
                                    else:
                                        try:
                                            registros = RegistroHorario.objects.filter(sucursal=s,dia=d)
                                        except RegistroHorario.DoesNotExist:
                                            registros = False
                                        if registros:
                                            sucursalRegistrosHorario.append((s,d,tipo,registros))
                                        else:
                                            sucursalRegistrosHorario.append((s,d,tipo,None))
                        try:
                            ciudades = Ciudad.objects.filter(estado=s.estado)
                        except Ciudad.DoesNotExist:
                            ciudades = False
                        if ciudades:
                            sucursalCiudades.append((s,ciudades))
                        else:
                            sucursalCiudades.append((s,None))
                        try:
                            relacionesServ = ServicioClub.objects.filter(sucursal=s)
                        except ServicioClub.DoesNotExist:
                            relacionesServ = False
                        if relacionesServ:
                            clubServicios.append((s,relacionesServ))
                        else:
                            clubServicios.append((s,None))
                        try:
                            relacionesAct = ActividadClub.objects.filter(sucursal=s)
                        except ActividadClub.DoesNotExist:
                            relacionesAct = False
                        if relacionesAct:
                            clubActividades.append((s,relacionesAct))
                        else:
                            clubActividades.append((s,None))
                try:
                    estados = Estado.objects.all()
                except Estado.DoesNotExist:
                    estados = False
                try:
                    actividadesHorarios = ActividadHorario.objects.all()
                except ActividadHorario.DoesNotExist:
                    actividadesHorarios = False
                try:
                    clubActividadesT = ActividadClub.objects.all()
                except ActividadClub.DoesNotExist:
                    clubActividadesT = False
                clubActividadHorarios = []
                if clubActividadesT:
                    for cAct in clubActividadesT:
                        try:
                            horarios = ActividadHorario.objects.filter(actividadClub=cAct)
                        except ActividadHorario.DoesNotExist:
                            horarios = False
                        numHorarios = 0
                        if horarios:
                            numHorarios = len(horarios)
                            clubActividadHorarios.append((cAct,horarios,numHorarios))
                        else:
                            clubActividadHorarios.append((cAct,None,numHorarios))
                try:
                    servicios = Servicio.objects.all()
                except Servicio.DoesNotExist:
                    servicios = False
                try:
                    actividades = Actividad.objects.all()
                except Actividad.DoesNotExist:
                    actividades
                if clubServicios:
                    for sucursal,serviciosSel in clubServicios:
                        if not serviciosSel == None:
                            listaSSel = []
                            for s in serviciosSel:
                                listaSSel.append(s.servicio.id)
                            listaS = []
                            if servicios:
                                for s in servicios:
                                    listaS.append(s.id)
                            serviciosDisponbles = [elem for elem in listaS if elem not in listaSSel]
                            serviciosDisponblesDos = []
                            if serviciosDisponbles:
                                for s in serviciosDisponbles:
                                    try:
                                        srv = Servicio.objects.get(id=s)
                                    except Servicio.DoesNotExist:
                                        srv = False
                                    if srv:
                                        serviciosDisponblesDos.append(srv)
                            clubServiciosDisponbles.append((sucursal,serviciosDisponblesDos))
                        else:
                            clubServiciosDisponbles.append((sucursal,servicios))
                if clubActividades:
                    for sucursal,actividadesSel in clubActividades:
                        if not actividadesSel == None:
                            listaASel = []
                            for a in actividadesSel:
                                listaASel.append(a.actividad.id)
                            listaA = []
                            if actividades:
                                for a in actividades:
                                    listaA.append(a.id)
                            actividadesDisponibles = [elem for elem in listaA if elem not in listaASel]
                            actividadesDisponiblesDos = []
                            if actividadesDisponibles:
                                for a in actividadesDisponibles:
                                    try:
                                        act = Actividad.objects.get(id=a)
                                    except Actividad.DoesNotExist:
                                        act = False
                                    if act:
                                        actividadesDisponiblesDos.append(act)
                            clubActividadesDisponibles.append((sucursal,actividadesDisponiblesDos))
                        else:
                            clubActividadesDisponibles.append((sucursal,actividades))
                try:
                    registrosH = RegistroHorario.objects.all()
                except RegistroHorario.DoesNotExist:
                    registrosH = False
                return render(request,'FitApp/homeSucursalPerfil.html',{'dias':dias,'club':sucursal.club,'sucursales':sucursales,'sucursalDatos':sucursalDatos,'sucursalFotos':sucursalFotos,'estados':estados,'sucursalCiudades':sucursalCiudades,'servicios':servicios,'actividades':actividades,'clubServicios':clubServicios,'clubServiciosDisponbles':clubServiciosDisponbles,'clubActividades':clubActividades,'clubActividadesDisponibles':clubActividadesDisponibles,'clubActividadHorarios':clubActividadHorarios,'actividadesHorarios':actividadesHorarios,'clubActividadesT':clubActividadesT,'sucursalHorario':sucursalHorario,'sucursalRegistrosHorario':sucursalRegistrosHorario,'registrosH':registrosH})
            else:
                return HttpResponseRedirect('/homeSucursal/')
        else:
            logout(request)
            return HttpResponseRedirect('/loginSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def editSucursal3(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            nombre = request.POST['nombre']
            try:
                descripcion = request.POST['descripcion']
            except MultiValueDictKeyError:
                descripcion = None
            try:
                tips = request.POST['tips']
            except MultiValueDictKeyError:
                tips = None
            correo = request.POST['correo']
            telefono = request.POST['telefono']
            estadoID = request.POST['estado']
            estado = Estado.objects.get(id=estadoID)
            ciudadID = request.POST['ciudad']
            ciudad = Ciudad.objects.get(id=ciudadID,estado=estado)
            municipio = request.POST['municipio']
            calle = request.POST['calle']
            numExt = request.POST['numExt']
            try:
                numInt = request.POST['numInt']
            except MultiValueDictKeyError:
                numInt = '...'
            colonia = request.POST['colonia']
            cp = request.POST['cp']
            try:
                logo = request.FILES['logo']
            except MultiValueDictKeyError:
                logo = False
            try:
                latitud = request.POST['latitud']
            except MultiValueDictKeyError:
                latitud = '...'
            try:
                longitud = request.POST['longitud']
            except MultiValueDictKeyError:
                longitud = '...'
            try:
                servicios = request.POST.getlist('servicios')
            except MultiValueDictKeyError:
                servicios = False
            try:
                actividades = request.POST.getlist('actividades')
            except MultiValueDictKeyError:
                actividades = False
            mensualidad = request.POST['mensualidad']
            dia = request.POST['dia']
            sucursal.nombre = nombre
            sucursal.descripcion = descripcion
            sucursal.tips = tips
            correoActual = sucursal.correo
            if not correo == correoActual:
                sucursal.correo = correo
                sucursal.save()
                user = sucursal.user
                user.username = correo
                user.email = correo
                user.save()
            sucursal.telefono = telefono
            sucursal.estado = estado
            sucursal.ciudad = ciudad
            sucursal.municipio = municipio
            sucursal.calle = calle
            sucursal.numExt = numExt
            sucursal.numInt = numInt
            sucursal.colonia = colonia
            sucursal.cp = cp
            sucursal.latitud = latitud
            sucursal.longitud = longitud
            sucursal.mensualidad = mensualidad
            sucursal.dia = dia
            sucursal.save()
            idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id)
            namePlan = "Mensualidad Sucursal "+nombre+", Club "+sucursal.club.nombre
            amountCentavos = int(float(mensualidad))*100
            try:
                planConektaSucursal = conekta.Plan.find(idPlan)
            except:
                planConektaSucursal = False
            if planConektaSucursal:
                planConektaSucursal.update({
                    "name":namePlan,
                    "amount":amountCentavos
                })
            if logo:
                logoActual = sucursal.logo.name
                if logoActual == 'default/logo.jpg':
                    sucursal.logo = logo
                    sucursal.save()
                else:
                    os.remove(sucursal.logo.path)
                    sucursal.logo = logo
                    sucursal.save()
            serviciosSeleccionados = []
            serviciosNoSeleccionados = []
            if servicios:
                for s in servicios:
                    try:
                        servicio = Servicio.objects.get(id=s)
                    except Servicio.DoesNotExist:
                        servicio = False
                    if servicio:
                        serviciosSeleccionados.append(servicio.id)
                        try:
                            relacion = ServicioClub.objects.get(sucursal=sucursal,servicio=servicio)
                        except ServicioClub.DoesNotExist:
                            relacion = False
                        if not relacion:
                            relacionNueva = ServicioClub(sucursal=sucursal,servicio=servicio)
                            relacionNueva.save()
                serviciosTodos = []
                try:
                    serviciosT = Servicio.objects.all()
                except Servicio.DoesNotExist:
                    serviciosT = False
                if serviciosT:
                    for s in serviciosT:
                        serviciosTodos.append(s.id)
                serviciosNoSeleccionados = [elem for elem in serviciosTodos if elem not in serviciosSeleccionados]
                if serviciosNoSeleccionados:
                    for s in serviciosNoSeleccionados:
                        try:
                            servicio = Servicio.objects.get(id=s)
                        except Servicio.DoesNotExist:
                            servicio = False
                        if servicio:
                            try:
                                relacion = ServicioClub.objects.get(sucursal=sucursal,servicio=servicio)
                            except ServicioClub.DoesNotExist:
                                relacion = False
                            if relacion:
                                relacion.delete()
            else:
                try:
                    relaciones = ServicioClub.objects.filter(sucursal=sucursal)
                except ServicioClub.DoesNotExist:
                    relaciones = False
                if relaciones:
                    for r in relaciones:
                        r.delete()
            actividadesSeleccionadas = []
            actividadesNoSeleccionadas = []
            if actividades:
                for a in actividades:
                    try:
                        actividad = Actividad.objects.get(id=a)
                    except Actividad.DoesNotExist:
                        actividad = False
                    if actividad:
                        actividadesSeleccionadas.append(actividad.id)
                        try:
                            relacion = ActividadClub.objects.get(sucursal=sucursal,actividad=actividad)
                        except ActividadClub.DoesNotExist:
                            relacion = False
                        if not relacion:
                            relacionNueva = ActividadClub(sucursal=sucursal,actividad=actividad)
                            relacionNueva.save()
                actividadesTodas = []
                try:
                    actividadesT = Actividad.objects.all()
                except Actividad.DoesNotExist:
                    actividadesT = False
                if actividadesT:
                    for a in actividadesT:
                        actividadesTodas.append(a.id)
                actividadesNoSeleccionadas = [elem for elem in actividadesTodas if elem not in actividadesSeleccionadas]
                if actividadesNoSeleccionadas:
                    for a in actividadesNoSeleccionadas:
                        try:
                            actividad = Actividad.objects.get(id=a)
                        except Actividad.DoesNotExist:
                            actividad = False
                        if actividad:
                            try:
                                relacion = ActividadClub.objects.get(sucursal=sucursal,actividad=actividad)
                            except ActividadClub.DoesNotExist:
                                relacion = False
                            if relacion:
                                relacion.delete()
            else:
                try:
                    relaciones = ActividadClub.objects.filter(sucursal=sucursal)
                except ActividadClub.DoesNotExist:
                    relaciones = False
                if relaciones:
                    for r in relaciones:
                        r.delete()
            try:
                horario = Horario.objects.get(sucursal=sucursal)
            except Horario.DoesNotExist:
                horario = False
            if horario:
                numDiasActual = horario.numDias
                mensualidad = Dec(mensualidad)
                calculo = (mensualidad)/(numDiasActual*4)
                calculoComision = (10*calculo)/100
                totalDia = calculo + calculoComision
                sucursal.dia = Dec(totalDia)
                sucursal.save()
            idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id)
            namePlan = "Mensualidad Sucursal "+sucursal.nombre+", Club "+sucursal.club.nombre
            amountCentavos = int(float(mensualidad))*100
            try:
                planConektaSucursal = conekta.Plan.find(idPlan)
            except:
                planConektaSucursal = False
            if not planConektaSucursal:
                conekta.Plan.create({
                    "id":idPlan,
                    "name":namePlan,
                    "amount":amountCentavos,
                    "currency":"MXN",
                    "interval":"month",
                    "frequency":1,
                    "trial_period_days":0,
                    "expiry_count":1
                })
            else:
                planConektaSucursal.update({
                    "id": idPlan,
                    "name": namePlan,
                    "amount": amountCentavos
                })
            url = '/homeClub/'+str(sucursal.club.id)+'/Sucursales/'
            return HttpResponseRedirect('/homeSucursal/Perfil/')
        else:
            return HttpResponseRedirect('/homeSucursal/Perfil/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def recortarFotoSucursalFormulario3(request):
    if not request.user.is_staff and request.user.is_authenticated:
        user = request.user
        try:
            usuario = Usuario.objects.get(user=user)
        except Usuario.DoesNotExist:
            usuario = False
        if usuario:
            club = usuario.sucursal.club
            sucursal = usuario.sucursal
            form = cropLogoSucursal(instance=sucursal)
            return render(request,'FitApp/homeSucursalRecortarFoto.html',{'user':user,'usuario':usuario,'club':club,'sucursal':sucursal,'form':form})
        else:
            return HttpResponseRedirect('/homeSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def recortarFotoSucursal3(request):
    if not request.user.is_staff and request.user.is_authenticated:
        sucursalID = request.POST['sucursal']
        sucursal = Sucursal.objects.get(id=sucursalID)
        form = cropLogoSucursal(instance=sucursal)
        if request.method == "POST":
            form = cropLogoSucursal(request.POST,request.FILES,instance=sucursal)
            if form.is_valid():
                thumbnailer = get_thumbnailer(sucursal.logo)
                thumbnailer.delete_thumbnails()
                logo = form.cleaned_data['logo']
                if logo:
                    sucursal.logo = logo
                    sucursal.logocrop = 0
                logocrop = form.cleaned_data['logocrop']
                sucursal.logocrop = logocrop
                sucursal.save()
                thumbnail_url = get_thumbnailer(sucursal.logo).get_thumbnail({'size': (200, 200),'box': sucursal.logocrop,'crop': True,'detail': True,}).url
                cropURL = thumbnail_url
                sucursal.cropURL = cropURL
                sucursal.save()
                url = '/homeSucursal/Perfil/'
                return HttpResponseRedirect(url)
            else:
                url = '/homeClub/Sucursal/RecortarLogo/'
                return HttpResponseRedirect(url)
        else:
            url = '/homeClub/Sucursal/RecortarLogo/'
            return HttpResponseRedirect(url)
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def addFotoSucursal3(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                foto = request.FILES['foto']
            except MultiValueDictKeyError:
                foto = False
            if foto:
                for f in request.FILES.getlist('foto'):
                    newFoto = Foto(sucursal=sucursal,archivo=f)
                    newFoto.save()
                return HttpResponseRedirect('/homeSucursal/Perfil/')
            else:
                error = 'Se requiere subir al menos una imagen.'
                return render(request,'FitApp/errorFotoSucursal3.html',{'error':error,'club':sucursal.club})
        else:
            return HttpResponseRedirect('/homeSucursal/Perfil/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def deleteFotoSucursal3(request,foto_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            foto = Foto.objects.get(id=foto_id)
        except Foto.DoesNotExist:
            foto = False
        if foto:
            club = foto.sucursal.club
            fotoActual = foto.archivo.name
            if not fotoActual == 'default/foto.png':
                os.remove(foto.archivo.path)
            foto.delete()
            return HttpResponseRedirect('/homeSucursal/Perfil/')
        else:
            return HttpResponseRedirect('/homeSucursal/Perfil/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def addHorarioSucursal3(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            repetido = False
            errores = []
            try:
                repetido = Horario.objects.get(sucursal=sucursal)
            except Horario.DoesNotExist:
                repetido = False
            if not repetido:
                lunes = False
                martes = False
                miercoles = False
                jueves = False
                viernes = False
                sabado = False
                domingo = False
                if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                    error = 'Debe seleccionar al menos un día en el horario.'
                    return render(request,'FitApp/errorHorarioSucursal3.html',{'error':error,'club':sucursal.club})
                else:
                    if lunesCheck:
                        lunes = True
                    else:
                        lunes = False
                    if martesCheck:
                        martes = True
                    else:
                        martes = False
                    if miercolesCheck:
                        miercoles = True
                    else:
                        miercoles = False
                    if juevesCheck:
                        jueves = True
                    else:
                        jueves = False
                    if viernesCheck:
                        viernes = True
                    else:
                        viernes = False
                    if sabadoCheck:
                        sabado = True
                    else:
                        sabado = False
                    if domingoCheck:
                        domingo = True
                    else:
                        domingo = False
                    tipoHorario = int(request.POST['tipoHorario'])
                    tipo = ''
                    if tipoHorario == 1:
                        tipo = u'Corrido'
                    else:
                        tipo = u'Mixto'
                    horario = Horario(sucursal=sucursal,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo,numDias=numDias,tipo=tipo)
                    horario.save()
                    if lunes:
                        dia = u'Lunes'
                        apertura = request.POST['lunesA']
                        cierre = request.POST['lunesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Lunes con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if martes:
                        dia = u'Martes'
                        apertura = request.POST['martesA']
                        cierre = request.POST['martesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Martes con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if miercoles:
                        dia = u'Miércoles'
                        apertura = request.POST['miercolesA']
                        cierre = request.POST['miercolesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Miércoles con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if jueves:
                        dia = u'Jueves'
                        apertura = request.POST['juevesA']
                        cierre = request.POST['juevesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Jueves con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if viernes:
                        dia = u'Viernes'
                        apertura = request.POST['viernesA']
                        cierre = request.POST['viernesC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Viernes con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if sabado:
                        dia = u'Sábado'
                        apertura = request.POST['sabadoA']
                        cierre = request.POST['sabadoC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Sábado con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                    if domingo:
                        dia = u'Domingo'
                        apertura = request.POST['domingoA']
                        cierre = request.POST['domingoC']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Domingo con la misma apertura y cierre (apertura '+str(apertura)+' y cierre '+str(cierre)+')'
                            errores.append(error)
                if not errores:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    numDiasActual = horarioSuc.numDias
                    mensualidad = sucursal.mensualidad
                    calculo = (mensualidad)/(numDiasActual*4)
                    calculoComision = (10*calculo)/100
                    totalDia = calculo + calculoComision
                    sucursal.dia = Dec(totalDia)
                    sucursal.save()
                    url = '/homeSucursal/Perfil/'
                    return HttpResponseRedirect(url)
                else:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    horarioSuc.delete()
                    error = 'Ha ocurrido uno o más errores al momento de registrar el horario, favor de revisarlos.'
                    return render(request,'FitApp/errorHorarioSucursalVarios3.html',{'error':error,'errores':json.dumps(errores),'club':horarioSuc.sucursal.club})
            else:
                error = 'Esta sucursal ya tiene un horario, registrado, si quieres editarlo usa el formulario de edición.'
                return render(request,'FitApp/errorHorarioSucursal3.html',{'error':error,'club':sucursal.club})
        else:
            return HttpResponseRedirect('/homeSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def addHorarioMixtoSucursal3(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            sucursalID = request.POST['sucursal']
            sucursal = Sucursal.objects.get(id=sucursalID)
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            repetido = False
            errores = []
            try:
                repetido = Horario.objects.get(sucursal=sucursal)
            except Horario.DoesNotExist:
                repetido = False
            if not repetido:
                lunes = False
                martes = False
                miercoles = False
                jueves = False
                viernes = False
                sabado = False
                domingo = False
                if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                    error = 'Debe seleccionar al menos un día en el horario.'
                    return render(request,'FitApp/errorHorarioSucursal3.html',{'error':error,'club':sucursal.club})
                else:
                    if lunesCheck:
                        lunes = True
                    else:
                        lunes = False
                    if martesCheck:
                        martes = True
                    else:
                        martes = False
                    if miercolesCheck:
                        miercoles = True
                    else:
                        miercoles = False
                    if juevesCheck:
                        jueves = True
                    else:
                        jueves = False
                    if viernesCheck:
                        viernes = True
                    else:
                        viernes = False
                    if sabadoCheck:
                        sabado = True
                    else:
                        sabado = False
                    if domingoCheck:
                        domingo = True
                    else:
                        domingo = False
                    tipoHorario = int(request.POST['tipoHorario'])
                    tipo = ''
                    if tipoHorario == 1:
                        tipo = u'Corrido'
                    else:
                        tipo = u'Mixto'
                    horario = Horario(sucursal=sucursal,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo,numDias=numDias,tipo=tipo)
                    horario.save()
                    if lunes:
                        dia = u'Lunes'
                        apertura1 = request.POST['lunesA1']
                        cierre1 = request.POST['lunesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Lunes con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['lunesA2']
                        cierre2 = request.POST['lunesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Lunes con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if martes:
                        dia = u'Martes'
                        apertura1 = request.POST['martesA1']
                        cierre1 = request.POST['martesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Martes con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['martesA2']
                        cierre2 = request.POST['martesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Martes con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if miercoles:
                        dia = u'Miércoles'
                        apertura1 = request.POST['miercolesA1']
                        cierre1 = request.POST['miercolesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Miércoles con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['miercolesA2']
                        cierre2 = request.POST['miercolesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Miércoles con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if jueves:
                        dia = u'Jueves'
                        apertura1 = request.POST['juevesA1']
                        cierre1 = request.POST['juevesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Jueves con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['juevesA2']
                        cierre2 = request.POST['juevesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Jueves con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if viernes:
                        dia = u'Viernes'
                        apertura1 = request.POST['viernesA1']
                        cierre1 = request.POST['viernesC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Viernes con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['viernesA2']
                        cierre2 = request.POST['viernesC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Viernes con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if sabado:
                        dia = u'Sábado'
                        apertura1 = request.POST['sabadoA1']
                        cierre1 = request.POST['sabadoC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Sábado con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['sabadoA2']
                        cierre2 = request.POST['sabadoC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Sábado con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                    if domingo:
                        dia = u'Domingo'
                        apertura1 = request.POST['domingoA1']
                        cierre1 = request.POST['domingoC1']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Domingo con la misma apertura y cierre (apertura '+str(apertura1)+' y cierre '+str(cierre1)+').'
                            errores.append(error)
                        apertura2 = request.POST['domingoA2']
                        cierre2 = request.POST['domingoC2']
                        try:
                            repetido = RegistroHorario.objects.get(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                        except RegistroHorario.DoesNotExist:
                            repetido = False
                        if not repetido:
                            registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                            registro.save()
                        else:
                            error = u'Esta sucursal ya tiene un horario el Domingo con la misma apertura y cierre (apertura '+str(apertura2)+' y cierre '+str(cierre2)+').'
                            errores.append(error)
                if not errores:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    numDiasActual = horarioSuc.numDias
                    mensualidad = sucursal.mensualidad
                    calculo = (mensualidad)/(numDiasActual*4)
                    calculoComision = (10*calculo)/100
                    totalDia = calculo + calculoComision
                    sucursal.dia = Dec(totalDia)
                    sucursal.save()
                    url = '/homeSucursal/Perfil/'
                    return HttpResponseRedirect(url)
                else:
                    horarioSuc = Horario.objects.get(sucursal=sucursal)
                    horarioSuc.delete()
                    error = 'Ha ocurrido uno o más errores al momento de registrar el horario, favor de revisarlos.'
                    return render(request,'FitApp/errorHorarioSucursalVarios3.html',{'error':error,'errores':json.dumps(errores),'club':horarioSuc.sucursal.club})
            else:
                error = 'Esta sucursal ya tiene un horario, registrado, si quieres editarlo usa el formulario de edición.'
                return render(request,'FitApp/errorHorarioSucursal3.html',{'error':error,'club':sucursal.club})
        else:
            return HttpResponseRedirect('/homeSucursal/Perfil/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def editHorarioSucursal3(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            horarioID = request.POST['horario']
            horario = Horario.objects.get(id=horarioID)
            sucursal = horario.sucursal
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                error = 'Debe seleccionar al menos un día en el horario.'
                return render(request,'FitApp/errorHorarioSucursal3.html',{'error':error,'club':horario.sucursal.club})
            lunes = False
            martes = False
            miercoles = False
            jueves = False
            viernes = False
            sabado = False
            domingo = False
            if lunesCheck:
                lunes = True
            else:
                lunes = False
            if martesCheck:
                martes = True
            else:
                martes = False
            if miercolesCheck:
                miercoles = True
            else:
                miercoles = False
            if juevesCheck:
                jueves = True
            else:
                jueves = False
            if viernesCheck:
                viernes = True
            else:
                viernes = False
            if sabadoCheck:
                sabado = True
            else:
                sabado = False
            if domingoCheck:
                domingo = True
            else:
                domingo = False
            horario.lunes = lunes
            horario.martes = martes
            horario.miercoles = miercoles
            horario.jueves = jueves
            horario.viernes = viernes
            horario.sabado = sabado
            horario.domingo = domingo
            horario.numDias = numDias
            horario.save()
            if lunesCheck:
                dia = u'Lunes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['lunesA']
                    cierre = request.POST['lunesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Lunes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if martesCheck:
                dia = u'Martes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['martesA']
                    cierre = request.POST['martesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Martes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if miercolesCheck:
                dia = u'Miércoles'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['miercolesA']
                    cierre = request.POST['miercolesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Miércoles'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if juevesCheck:
                dia = u'Jueves'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['juevesA']
                    cierre = request.POST['juevesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Jueves'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if viernesCheck:
                dia = u'Viernes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['viernesA']
                    cierre = request.POST['viernesC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Viernes'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if sabadoCheck:
                dia = u'Sábado'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['sabadoA']
                    cierre = request.POST['sabadoC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Sábado'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            if domingoCheck:
                dia = u'Domingo'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if not registroHorario:
                    apertura = request.POST['domingoA']
                    cierre = request.POST['domingoC']
                    registro = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura,cierre=cierre)
                    registro.save()
            else:
                dia = u'Domingo'
                try:
                    registroHorario = RegistroHorario.objects.get(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registroHorario = False
                if registroHorario:
                    registroHorario.delete()
            horarioSuc = Horario.objects.get(id=horarioID)
            sucursal = horarioSuc.sucursal
            numDiasActual = horarioSuc.numDias
            mensualidad = sucursal.mensualidad
            calculo = (mensualidad)/(numDiasActual*4)
            calculoComision = (10*calculo)/100
            totalDia = calculo + calculoComision
            sucursal.dia = Dec(totalDia)
            sucursal.save()
            url = '/homeSucursal/Perfil/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def editHorarioMixtoSucursal3(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            horarioID = request.POST['horario']
            horario = Horario.objects.get(id=horarioID)
            sucursal = horario.sucursal
            try:
                lunesCheck = request.POST['lunesCheck']
            except MultiValueDictKeyError:
                lunesCheck = False
            try:
                martesCheck = request.POST['martesCheck']
            except MultiValueDictKeyError:
                martesCheck = False
            try:
                miercolesCheck = request.POST['miercolesCheck']
            except MultiValueDictKeyError:
                miercolesCheck = False
            try:
                juevesCheck = request.POST['juevesCheck']
            except MultiValueDictKeyError:
                juevesCheck = False
            try:
                viernesCheck = request.POST['viernesCheck']
            except MultiValueDictKeyError:
                viernesCheck = False
            try:
                sabadoCheck = request.POST['sabadoCheck']
            except MultiValueDictKeyError:
                sabadoCheck = False
            try:
                domingoCheck = request.POST['domingoCheck']
            except MultiValueDictKeyError:
                domingoCheck = False
            numDias = request.POST['numDias']
            if not lunesCheck and not martesCheck and not miercolesCheck and not juevesCheck and not viernesCheck and not sabadoCheck and not domingoCheck:
                error = 'Debe seleccionar al menos un día en el horario.'
                return render(request,'FitApp/errorHorarioSucursal.html',{'error':error,'club':horario.sucursal.club})
            lunes = False
            martes = False
            miercoles = False
            jueves = False
            viernes = False
            sabado = False
            domingo = False
            if lunesCheck:
                lunes = True
            else:
                lunes = False
            if martesCheck:
                martes = True
            else:
                martes = False
            if miercolesCheck:
                miercoles = True
            else:
                miercoles = False
            if juevesCheck:
                jueves = True
            else:
                jueves = False
            if viernesCheck:
                viernes = True
            else:
                viernes = False
            if sabadoCheck:
                sabado = True
            else:
                sabado = False
            if domingoCheck:
                domingo = True
            else:
                domingo = False
            horario.lunes = lunes
            horario.martes = martes
            horario.miercoles = miercoles
            horario.jueves = jueves
            horario.viernes = viernes
            horario.sabado = sabado
            horario.domingo = domingo
            horario.numDias = numDias
            horario.save()
            if lunesCheck:
                dia = u'Lunes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['lunesA1']
                    cierre1 = request.POST['lunesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['lunesA2']
                    cierre2 = request.POST['lunesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Lunes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if martesCheck:
                dia = u'Martes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['martesA1']
                    cierre1 = request.POST['martesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['martesA2']
                    cierre2 = request.POST['martesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Martes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if miercolesCheck:
                dia = u'Miércoles'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['miercolesA1']
                    cierre1 = request.POST['miercolesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['miercolesA2']
                    cierre2 = request.POST['miercolesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Miércoles'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if juevesCheck:
                dia = u'Jueves'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['juevesA1']
                    cierre1 = request.POST['juevesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['juevesA2']
                    cierre2 = request.POST['juevesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Jueves'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if viernesCheck:
                dia = u'Viernes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['viernesA1']
                    cierre1 = request.POST['viernesC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['viernesA2']
                    cierre2 = request.POST['viernesC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Viernes'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if sabadoCheck:
                dia = u'Sábado'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['sabadoA1']
                    cierre1 = request.POST['sabadoC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['sabadoA2']
                    cierre2 = request.POST['sabadoC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Sábado'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            if domingoCheck:
                dia = u'Domingo'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if not registrosHorario:
                    apertura1 = request.POST['domingoA1']
                    cierre1 = request.POST['domingoC1']
                    registro1 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura1,cierre=cierre1)
                    registro1.save()
                    apertura2 = request.POST['domingoA2']
                    cierre2 = request.POST['domingoC2']
                    registro2 = RegistroHorario(sucursal=sucursal,dia=dia,apertura=apertura2,cierre=cierre2)
                    registro2.save()
            else:
                dia = u'Domingo'
                try:
                    registrosHorario = RegistroHorario.objects.filter(sucursal=sucursal,dia=dia)
                except RegistroHorario.DoesNotExist:
                    registrosHorario = False
                if registrosHorario:
                    for r in registrosHorario:
                        r.delete()
            horarioSuc = Horario.objects.get(id=horarioID)
            sucursal = horarioSuc.sucursal
            numDiasActual = horarioSuc.numDias
            mensualidad = sucursal.mensualidad
            calculo = (mensualidad)/(numDiasActual*4)
            calculoComision = (10*calculo)/100
            totalDia = calculo + calculoComision
            sucursal.dia = Dec(totalDia)
            sucursal.save()
            url = '/homeSucursal/Perfil/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def editRegistroHorario3(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            registroHorarioID = request.POST['registroHorario']
            registroHorario = RegistroHorario.objects.get(id=registroHorarioID)
            apertura = request.POST['apertura']
            cierre = request.POST['cierre']
            registroHorario.apertura = apertura
            registroHorario.cierre = cierre
            registroHorario.save()
            sucursal = registroHorario.sucursal
            url = '/homeSucursal/Perfil/'
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/homeSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def deleteHorarioSucursal3(request,horario_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            horario = Horario.objects.get(id=horario_id)
        except Horario.DoesNotExist:
            horario = False
        if horario:
            club = horario.sucursal.club
            sucursal = horario.sucursal
            horario.delete()
            sucursal.dia = 0
            sucursal.save()
            try:
                registros = RegistroHorario.objects.filter(sucursal=sucursal)
            except RegistroHorario.DoesNotExist:
                registros = False
            if registros:
                for r in registros:
                    r.delete()
            return HttpResponseRedirect('/homeSucursal/Perfil/')
        else:
            return HttpResponseRedirect('/homeSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def addActividadHorario3(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            actividadClubID = request.POST['actividadClub']
            actividadClub = ActividadClub.objects.get(id=actividadClubID)
            horaInicio = request.POST['horaInicio']
            horaFin = request.POST['horaFin']
            try:
                lunes = request.POST['lunes']
            except MultiValueDictKeyError:
                lunes = False
            try:
                martes = request.POST['martes']
            except MultiValueDictKeyError:
                martes = False
            try:
                miercoles = request.POST['miercoles']
            except MultiValueDictKeyError:
                miercoles = False
            try:
                jueves = request.POST['jueves']
            except MultiValueDictKeyError:
                jueves = False
            try:
                viernes = request.POST['viernes']
            except MultiValueDictKeyError:
                viernes = False
            try:
                sabado = request.POST['sabado']
            except MultiValueDictKeyError:
                sabado = False
            try:
                domingo = request.POST['domingo']
            except MultiValueDictKeyError:
                domingo = False
            if not lunes and not martes and not miercoles and not jueves and not viernes and not sabado and not domingo:
                error = u'Debes seleccionar al menos un día de la semana para el horario a registrar.'
                return render(request,'FitApp/errorHorarioActividad3.html',{'error':error,'club':actividadClub.sucursal.club})
            repetido = False
            try:
                repetido = ActividadHorario.objects.get(actividadClub=actividadClub,horaInicio=horaInicio,horaFin=horaFin,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo)
            except ActividadHorario.DoesNotExist:
                repetido = False
            if not repetido:
                actividadHorario = ActividadHorario(actividadClub=actividadClub,horaInicio=horaInicio,horaFin=horaFin,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo)
                actividadHorario.save()
                return HttpResponseRedirect('/homeSucursal/Perfil/')
                return HttpResponseRedirect(url)
            else:
                error = u'Ya hay un registro de horario para esta actividad con los mismos datos, favor de verificar.'
                return render(request,'FitApp/errorHorarioActividad3.html',{'error':error,'club':actividadClub.sucursal.club})
        else:
            return HttpResponseRedirect('/homeSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def editActividadHorario3(request):
    if not request.user.is_staff and request.user.is_authenticated:
        if request.method == "POST":
            actividadHorarioID = request.POST['actividadHorario']
            actividadHorario = ActividadHorario.objects.get(id=actividadHorarioID)
            horaInicio = request.POST['horaInicio']
            horaFin = request.POST['horaFin']
            try:
                lunes = request.POST['lunes']
            except MultiValueDictKeyError:
                lunes = False
            try:
                martes = request.POST['martes']
            except MultiValueDictKeyError:
                martes = False
            try:
                miercoles = request.POST['miercoles']
            except MultiValueDictKeyError:
                miercoles = False
            try:
                jueves = request.POST['jueves']
            except MultiValueDictKeyError:
                jueves = False
            try:
                viernes = request.POST['viernes']
            except MultiValueDictKeyError:
                viernes = False
            try:
                sabado = request.POST['sabado']
            except MultiValueDictKeyError:
                sabado = False
            try:
                domingo = request.POST['domingo']
            except MultiValueDictKeyError:
                domingo = False
            actividadHorario.horaInicio = horaInicio
            actividadHorario.horaFin = horaFin
            actividadHorario.lunes = lunes
            actividadHorario.martes = martes
            actividadHorario.miercoles = miercoles
            actividadHorario.jueves = jueves
            actividadHorario.viernes = viernes
            actividadHorario.sabado = sabado
            actividadHorario.domingo = domingo
            actividadHorario.save()
            return HttpResponseRedirect('/homeSucursal/Perfil/')
        else:
            return HttpResponseRedirect('/homeSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def deleteActividadHorario3(request,actividadHorario_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            actividadHorario = ActividadHorario.objects.get(id=actividadHorario_id)
        except ActividadHorario.DoesNotExist:
            actividadHorario = False
        if actividadHorario:
            idClub = actividadHorario.actividadClub.sucursal.club.id
            actividadHorario.delete()
            return HttpResponseRedirect('/homeSucursal/Perfil/')
        else:
            return HttpResponseRedirect('/homeSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def sucursalClientes(request):
    if not request.user.is_staff and request.user.is_authenticated:
        user = request.user
        usuario = Usuario.objects.get(user=user)
        sucursal = usuario.sucursal
        try:
            clientes = Cliente.objects.all()
        except Cliente.DoesNotExist:
            clientes = False
        clientesSub = []
        clienteSes = []
        clienteVisitaHoy = []
        clienteSubPuedeVisitar = []
        clienteSesPuedeVisitar = []
        today = str(date.today())
        if clientes:
            for c in clientes:
                try:
                    sub = Subscripcion.objects.filter(sucursal=sucursal,cliente=c).order_by('-id')[:1]
                except Subscripcion.DoesNotExist:
                    sub = False
                if sub:
                    clientesSub.append(sub[0])
                try:
                    ses = Sesion.objects.filter(sucursal=sucursal,cliente=c).order_by('-id')[:1]
                except Sesion.DoesNotExist:
                    ses = False
                if ses:
                    clienteSes.append(ses[0])
                try:
                    visita = Visita.objects.get(sucursal=sucursal,cliente=c,fecha=today)
                except Visita.DoesNotExist:
                    visita = False
                if visita:
                    clienteVisitaHoy.append((c,True))
                else:
                    clienteVisitaHoy.append((c,False))
                try:
                    subsc = Subscripcion.objects.filter(sucursal=sucursal,cliente=c,activa=True)
                except Subscripcion.DoesNotExist:
                    subsc = False
                if subsc:
                    clienteSubPuedeVisitar.append((c,True))
                else:
                    clienteSubPuedeVisitar.append((c,False))
                try:
                    sesi = Sesion.objects.filter(sucursal=sucursal,cliente=c,activo=True)
                except Sesion.DoesNotExist:
                    sesi = False
                if subsc:
                    clienteSesPuedeVisitar.append((c,True))
                else:
                    clienteSesPuedeVisitar.append((c,False))
        return render(request,'FitApp/homeSucursalClientes.html',{'clientes':clientes,'sucursal':sucursal,'clientesSub':clientesSub,'clienteSes':clienteSes,'clienteVisitaHoy':clienteVisitaHoy,'clienteSubPuedeVisitar':clienteSubPuedeVisitar,'clienteSesPuedeVisitar':clienteSesPuedeVisitar})
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def notificacionCliente(request,cliente_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            cliente = False
        if cliente:
            if cliente.playerID:
                playerID = cliente.playerID
                men = "Mensaje."
                head = {
                    "Content-Type": "application/json; charset=utf-8",
                    "Authorization": "Basic NzRlYTM4MmUtMjQ0Yy00ZmVkLWI3NjUtNWFiZDQzODAwZDlh"
                }
                pay = {
                    "app_id": "37b073dd-8ce8-4eb7-9cd4-9235a5a14cad",
                    "include_player_ids": [playerID],
                    "headings": {"en": "Notificación", "es" : "Notificación"},
                    "subtitle": {"en": "Notificación", "es" : "Notificación"},
                    "contents": {"en":men, "es": men}
                }
                try:
                    reqM = requests.post("https://onesignal.com/api/v1/notifications", headers=head, data=json.dumps(pay))
                except:
                    reqM = False
                if reqM:
                    mensaje = u'La notificación ha sido enviada.'
                    return render(request,'FitApp/notificacionEnviada.html',{'mensaje':mensaje})
                else:
                    mensaje = u'La notificación no pudo ser enviada, intente más tarde.'
                    return render(request,'FitApp/errorNotificacion.html',{'mensaje':mensaje})
            else:
                return HttpResponseRedirect('/homeSucursal/Clientes/')
        else:
            return HttpResponseRedirect('/homeSucursal/Clientes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def registrarVisitaSub(request,cliente_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            cliente = False
        if cliente:
            today = str(date.today())
            user = request.user
            usuario = Usuario.objects.get(user=user)
            sucursal = usuario.sucursal
            try:
                visitaR = Visita.objects.get(sucursal=sucursal,cliente=cliente,fecha=today)
            except Visita.DoesNotExist:
                visitaR = False
            if visitaR:
                error = u'El cliente ya tiene una visita registrada hoy.'
                return render(request,'FitApp/errorRegistrarVisita.html',{'error':error})
            else:
                visita = Visita(sucursal=sucursal,cliente=cliente)
                visita.save()
                if cliente.playerID:
                    playerID = cliente.playerID
                    men = "Se ha registrado una visita a la sucursal " + sucursal.nombre + "."
                    head = {
                        "Content-Type": "application/json; charset=utf-8",
                        "Authorization": "Basic NzRlYTM4MmUtMjQ0Yy00ZmVkLWI3NjUtNWFiZDQzODAwZDlh"
                    }
                    pay = {
                        "app_id": "37b073dd-8ce8-4eb7-9cd4-9235a5a14cad",
                        "include_player_ids": [playerID],
                        "headings": {"en": "Notificación", "es" : "Notificación"},
                        "subtitle": {"en": "Notificación", "es" : "Notificación"},
                        "contents": {"en":men, "es": men}
                    }
                    try:
                        reqM = requests.post("https://onesignal.com/api/v1/notifications", headers=head, data=json.dumps(pay))
                    except:
                        reqM = False
                return HttpResponseRedirect('/homeSucursal/Clientes/')
        else:
            return HttpResponseRedirect('/homeSucursal/Clientes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def registrarVisitaSes(request,cliente_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            cliente = False
        if cliente:
            today = str(date.today())
            user = request.user
            usuario = Usuario.objects.get(user=user)
            sucursal = usuario.sucursal
            try:
                visitaR = Visita.objects.get(sucursal=sucursal,cliente=cliente,fecha=today)
            except Visita.DoesNotExist:
                visitaR = False
            if visitaR:
                error = u'El cliente ya tiene una visita registrada hoy.'
                return render(request,'FitApp/errorRegistrarVisita.html',{'error':error})
            else:
                visita = Visita(sucursal=sucursal,cliente=cliente)
                visita.save()
                if cliente.playerID:
                    playerID = cliente.playerID
                    men = "Se ha registrado una visita a la sucursal " + sucursal.nombre + "."
                    head = {
                        "Content-Type": "application/json; charset=utf-8",
                        "Authorization": "Basic NzRlYTM4MmUtMjQ0Yy00ZmVkLWI3NjUtNWFiZDQzODAwZDlh"
                    }
                    pay = {
                        "app_id": "37b073dd-8ce8-4eb7-9cd4-9235a5a14cad",
                        "include_player_ids": [playerID],
                        "headings": {"en": "Notificación", "es" : "Notificación"},
                        "subtitle": {"en": "Notificación", "es" : "Notificación"},
                        "contents": {"en":men, "es": men}
                    }
                    try:
                        reqM = requests.post("https://onesignal.com/api/v1/notifications", headers=head, data=json.dumps(pay))
                    except:
                        reqM = False
                try:
                    sesion = Sesion.objects.get(cliente=cliente,sucursal=sucursal,activo=True)
                except Sesion.DoesNotExist:
                    sesion = False
                if sesion:
                    sesion.sesionesRestantes = int(sesion.sesionesRestantes) - int(1)
                    sesion.save()
                return HttpResponseRedirect('/homeSucursal/Clientes/')
        else:
            return HttpResponseRedirect('/homeSucursal/Clientes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def clienteHistorialVisitas(request,cliente_id):
    if not request.user.is_staff and request.user.is_authenticated:
        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            cliente = False
        if cliente:
            try:
                visitas = Visita.objects.filter(cliente=cliente).order_by('fecha')
            except Visita.DoesNotExist:
                visitas = False
            page = request.GET.get('page', 1)
            paginator = Paginator(visitas,50)
            try:
                visitas = paginator.page(page)
            except PageNotAnInteger:
                visitas = paginator.page(1)
            except EmptyPage:
                visitas = paginator.page(paginator.num_pages)
            return render(request,'FitApp/homeSucursalClienteHistorialVisitas.html',{'cliente':cliente,'visitas':visitas})
        else:
            return HttpResponseRedirect('/homeSucursal/Clientes/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def sucursalVisitas(request):
    if not request.user.is_staff and request.user.is_authenticated:
        today = str(date.today())
        user = request.user
        usuario = Usuario.objects.get(user=user)
        sucursal = usuario.sucursal
        try:
            visitas = Visita.objects.filter(sucursal=sucursal,fecha=today).order_by('-hora')
        except Visita.DoesNotExist:
            visitas = False
        return render(request,'FitApp/homeSucursalVisitas.html',{'sucursal':sucursal,'visitas':visitas,'today':date.today()})
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def pagosSucursal(request):
    if not request.user.is_staff and request.user.is_authenticated:
        user = request.user
        try:
            usuario = Usuario.objects.get(user=user)
        except Usuario.DoesNotExist:
            usuario = False
        if usuario:
            sucursal = usuario.sucursal
            try:
                pagos = PagoSucursal.objects.filter(sucursal=sucursal).order_by('-fecha')
            except PagoSucursal.DoesNotExist:
                pagos = False
            page = request.GET.get('page', 1)
            paginator = Paginator(pagos,50)
            try:
                pagos = paginator.page(page)
            except PageNotAnInteger:
                pagos = paginator.page(1)
            except EmptyPage:
                pagos = paginator.page(paginator.num_pages)
            return render(request,'FitApp/homeSucursalPagos.html',{'sucursal':sucursal,'usuario':usuario,'user':user,'pagos':pagos})
        else:
            return HttpResponseRedirect('/homeSucursal/')
    else:
        logout(request)
        return HttpResponseRedirect('/loginSucursal/')

def logoutSucursal(request):
    logout(request)
    return HttpResponseRedirect('/loginSucursal/')

def RecuperarContrasena(request):
    return render(request,'FitApp/recuperarContrasena.html')

def recuperarContrasenaPte1(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            cliente = Cliente.objects.get(user__email=email)
        except Cliente.DoesNotExist:
            cliente = False
        if cliente:
            token = get_random_string(length=32)
            incidencia = IncidenciaContrasena(correo=email,fecha=datetime.now(),estatus=0,token=token)
            incidencia.save()
            body = "<body><p>Estimado(a) "+cliente.nombre+", hemos recibido una peticion para realizar un cambio de contrasena.</br>Para poder llevar esta accion a cabo debe hacer click en </br><a href='https://www.fitory.com"+"/RecuperarContrasena/incidencia="+str(incidencia.id)+"/"+"'>el siguiente enlace</a>.</br>A continuacion se le proporciona una clave que debe introducir para realizar el cambio de contrasena <span style='color:green'>"+token+"</span><br/>Si usted no solicito este cambio por favor hacer caso omiso a este mensaje.</p></body>"
            email = EmailMultiAlternatives('Solicitud de cambio de contrasena', 'body', 'contacto@fitory.com', [email])
            email.attach_alternative(body, "text/html")
            email.send()
            mensaje = u'Tu solicitud para recuperar contraseña, esta siendo procesada, en breve recibiras instrucciones para llevar a cabo este proceso.'
            return render(request,'FitApp/incidenciaCreada.html',{'mensaje':mensaje})
        else:
            try:
                club = Club.objects.get(user__email=email)
            except Club.DoesNotExist:
                club = False
            if club:
                token = get_random_string(length=32)
                incidencia = IncidenciaContrasena(correo=email,fecha=datetime.now(),estatus=0,token=token)
                incidencia.save()
                body = "<body><p>Estimado(a) "+cliente.nombre+", hemos recibido una peticion para realizar un cambio de contrasena.</br>Para poder llevar esta accion a cabo debe hacer click en </br><a href='https://www.fitory.com"+"/RecuperarContrasena/incidencia="+str(incidencia.id)+"/"+"'>el siguiente enlace</a>.</br>A continuacion se le proporciona una clave que debe introducir para realizar el cambio de contrasena <span style='color:green'>"+token+"</span><br/>Si usted no solicito este cambio por favor hacer caso omiso a este mensaje.</p></body>"
                email = EmailMultiAlternatives('Solicitud de cambio de contrasena', 'body', 'contacto@fitory.com', [email])
                email.attach_alternative(body, "text/html")
                email.send()
                mensaje = u'Tu solicitud para recuperar contraseña, esta siendo procesada, en breve recibiras instrucciones para llevar a cabo este proceso.'
                return render(request,'FitApp/incidenciaCreada.html',{'mensaje':mensaje})
            else:
                try:
                    usuario = Usuario.objects.get(user__email=email)
                except Usuario.DoesNotExist:
                    usuario = False
                if usuario:
                    token = get_random_string(length=32)
                    incidencia = IncidenciaContrasena(correo=email,fecha=datetime.now(),estatus=0,token=token)
                    incidencia.save()
                    body = "<body><p>Estimado(a) "+cliente.nombre+", hemos recibido una peticion para realizar un cambio de contrasena.</br>Para poder llevar esta accion a cabo debe hacer click en </br><a href='https://www.fitory.com"+"/RecuperarContrasena/incidencia="+str(incidencia.id)+"/"+"'>el siguiente enlace</a>.</br>A continuacion se le proporciona una clave que debe introducir para realizar el cambio de contrasena <span style='color:green'>"+token+"</span><br/>Si usted no solicito este cambio por favor hacer caso omiso a este mensaje.</p></body>"
                    email = EmailMultiAlternatives('Solicitud de cambio de contrasena', 'body', 'contacto@fitory.com', [email])
                    email.attach_alternative(body, "text/html")
                    email.send()
                    mensaje = u'Tu solicitud para recuperar contraseña, esta siendo procesada, en breve recibiras instrucciones para llevar a cabo este proceso.'
                    return render(request,'FitApp/incidenciaCreada.html',{'mensaje':mensaje})
                else:
                    error = u'Esta dirección email, no está registrada.'
                    return render(request,'FitApp/errorRecuperarContrasena.html',{'error':error})
    else:
        error = u'Acceso incorrecto.'
        return render(request,'FitApp/errorRecuperarContrasena.html',{'error':error})

def FormularioPassword(request,idIncidencia):
    try:
        incidencia = IncidenciaContrasena.objects.get(id=idIncidencia)
    except IncidenciaContrasena.DoesNotExist:
        incidencia = False
    if incidencia:
        return render(request,'FitApp/formularioRestaurar.html',{'incidencia':incidencia})
    else:
        error = u'Acceso incorrecto'
        return render(request,'FitApp/errorRecuperarContrasena2.html',{'error':error})

def recuperarContrasenaPte2(request):
    if request.method == "POST":
        incidenciaID = request.POST['incidenciaID']
        try:
            incidencia = IncidenciaContrasena.objects.get(id=incidenciaID,estatus=False)
        except IncidenciaContrasena.DoesNotExist:
            incidencia = False
        if incidencia:
            token = request.POST['token']
            password = request.POST['password']
            if incidencia.token == token:
                correo = incidencia.correo
                try:
                    user = User.objects.get(email=correo)
                except User.DoesNotExist:
                    user = False
                if user:
                    user.set_password(password)
                    user.save()
                    incidencia.estatus = True
                    incidencia.save()
                    mensaje = u'Tu contraseña ha sido restablecida.'
                    return render(request,'FitApp/cuentaRestablecida.html',{'mensaje':mensaje})
                else:
                    error = u'Acceso incorrecto'
                    return render(request,'FitApp/errorRecuperarContrasena2.html',{'error':error})
            else:
                error = u'La clave proporcionada no es valida.'
                return render(request,'FitApp/errorRecuperarContrasena3.html',{'error':error,'incidencia':incidencia})
        else:
            error = u'Acceso incorrecto.'
            return render(request,'FitApp/errorRecuperarContrasena2.html',{'error':error})
    else:
        error = u'Acceso incorrecto.'
        return render(request,'FitApp/errorRecuperarContrasena2.html',{'error':error})
            

"""
-----------------------Django Rest Framework (API)-----------------------------------
"""

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by('id')
	serializer_class = UserSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('id','username','email')

class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer
	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			try:
				username = data["username"]
			except MultiValueDictKeyError:
				username = None
			try:
				email = data["email"]
			except MultiValueDictKeyError:
				email = None
			password = data["password"]
			if username and email:
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
			elif username and not email:
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
			elif not username and email:
				userEmail = User.objects.get(email=email)
				userUsername = userEmail.username
				user = authenticate(username=userUsername, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
			return Response(new_data, status=HTTP_200_OK)
		else:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
	def get(self,request,format=None):
		logout(request)
		mensaje = {"mensaje":"Sesion terminada"}
		return Response(mensaje,status=HTTP_200_OK)

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all().order_by('id')
    serializer_class = EstadoSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','nombre')

class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all().order_by('id')
    serializer_class = CiudadSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','estado__id','estado__nombre','nombre')

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all().order_by('id')
    serializer_class = ServicioSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','nombre')

class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all().order_by('id')
    serializer_class = ActividadSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','nombre')

class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all().order_by('id')
    serializer_class = ClubSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','user__id','nombre','fechaIncorporacion','activado','codigoClub','codigoRepresentante','evaluacionPromedio')

class ServicioClubViewSet(viewsets.ModelViewSet):
    queryset = ServicioClub.objects.all().order_by('id')
    serializer_class = ServicioClubSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','sucursal__id','sucursal__nombre','servicio__id','servicio__nombre')

class ActividadClubViewSet(viewsets.ModelViewSet):
    queryset = ActividadClub.objects.all().order_by('id')
    serializer_class = ActividadClubSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','sucursal__id','sucursal__nombre','actividad__id','actividad__nombre')

class ActividadHorarioViewSet(viewsets.ModelViewSet):
    queryset = ActividadHorario.objects.all().order_by('id')
    serializer_class = ActividadHorarioSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','actividadClub__id','horaInicio','horaFin')

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all().order_by('id')
    serializer_class = SucursalSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','club__id','club__nombre','club__activado','nombre','latitud','longitud','calificacion','ibeacon','maximo','minimo','activa','ciudad','estado')

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('id')
    serializer_class = UsuarioSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','sucursal__id','sucursal__nombre','user','nombre','activo')

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all().order_by('sucursal')
    serializer_class = HorarioSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','sucursal__id','sucursal__nombre')

class RegistroHorarioViewSet(viewsets.ModelViewSet):
    queryset = RegistroHorario.objects.all().order_by('id')
    serializer_class = RegistroHorarioSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','sucursal__id','sucursal__nombre')

class FotoViewSet(viewsets.ModelViewSet):
    queryset = Foto.objects.all().order_by('id')
    serializer_class = FotoSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','sucursal__id','sucursal__nombre')

class EvaluacionSucursalViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionSucursal.objects.all().order_by('id')
    serializer_class = EvaluacionSucursalSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','cliente__id','cliente__nombre','sucursal__id','sucursal__nombre','puntaje')

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','user','nombre','apellido','hombre','mujer','fechaIngreso','salud','convivir','vermeBien','diversion','estado__id','estado__nombre','ciudad__id','ciudad__nombre','ubicacion','bluetooth','idFacebook','idGoogle','idCustomer')

class EvaluacionClienteViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionCliente.objects.all().order_by('id')
    serializer_class = EvaluacionClienteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','cliente__id','cliente__nombre','puntaje')

class FavoritoViewSet(viewsets.ModelViewSet):
    queryset = Favorito.objects.all().order_by('id')
    serializer_class = FavoritoSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','cliente__id','cliente__nombre','sucursal__id','sucursal__nombre')

class SesionViewSet(viewsets.ModelViewSet):
    queryset = Sesion.objects.all().order_by('id')
    serializer_class = SesionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','cliente__id','cliente__nombre','sucursal__id','sucursal__nombre','activo')

class SubscripcionViewSet(viewsets.ModelViewSet):
    queryset = Subscripcion.objects.all().order_by('id')
    serializer_class = SubscripcionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','cliente__id','cliente__nombre','sucursal__id','sucursal__nombre','activa')

class SubscripcionFreeViewSet(viewsets.ModelViewSet):
    queryset = SubscripcionFree.objects.all().order_by('id')
    serializer_class = SubscripcionFreeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','cliente__id','cliente__nombre','sucursal__id','sucursal__nombre','activa')

class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all().order_by('id')
    serializer_class = VisitaSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','cliente__id','cliente__nombre','sucursal__id','sucursal__nombre','fecha','hora')

class PagoSucursalViewSet(viewsets.ModelViewSet):
    queryset = PagoSucursal.objects.all().order_by('id')
    serializer_class = PagoSucursalSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id','sucursal__id','sucursal__nombre','fecha','pagar')

class CustomerConektaApiView(APIView):
    serializer_class = CustomerConektaSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CustomerConektaSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class BorrarCustomerConektaApiView(APIView):
    serializer_class = BorrarCustomerConektaSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = BorrarCustomerConektaSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class AddMetodoPagoApiView(APIView):
    serializer_class = addMetodoPagoSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = addMetodoPagoSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class deleteMetodoPagoApiView(APIView):
    serializer_class = deleteMetodoPagoSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = deleteMetodoPagoSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class MetodosPagoApiView(APIView):
    serializer_class = MetodosPagoSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = MetodosPagoSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class SubscripcionMensualApiView(APIView):
    serializer_class = SubscripcionMensualSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SubscripcionMensualSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class CancelarSubscripcionMensualApiView(APIView):
    serializer_class = CancelarSubscripcionMensualSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CancelarSubscripcionMensualSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class ActualizarSubscripcionMensualApiView(APIView):
    serializer_class = ActualizarSubscripcionMensualSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ActualizarSubscripcionMensualSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class CobrarPorSesionApiView(APIView):
    serializer_class = CobrarPorSesionSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CobrarPorSesionSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class ActualizarFotoClienteAPIView(APIView):
    serializer_class = ActualizarFotoClienteSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ActualizarFotoClienteSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class CalcularPromedioEvaluacionesAPIView(APIView):
    serializer_class = CalcularPromedioEvaluacionesSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CalcularPromedioEvaluacionesSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ConsultaFechaAPIView(APIView):
    serializer_class = ConsultaFechaSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ConsultaFechaSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class PerfilSucursalAPIView(APIView):
    serializer_class = PerfilSucursalSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = PerfilSucursalSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class DiasDisponiblesAPIView(APIView):
    serializer_class = DiasDisponiblesSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = DiasDisponiblesSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RegistrarVisitaAPIView(APIView):
    serializer_class = RegistrarVisitaSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegistrarVisitaSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RevisarVisitaAPIView(APIView):
    serializer_class = RevisarVisitaSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RevisarVisitaSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RevisarSubscripcionFreeAPIView(APIView):
    serializer_class = RevisarSubscripcionFreeSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RevisarSubscripcionFreeSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ActivarSubscripcionFreeAPIView(APIView):
    serializer_class = ActivarSubscripcionFreeSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ActivarSubscripcionFreeSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RegistrarCelularAPIView(APIView):
    serializer_class = RegistrarCelularSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegistrarCelularSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class CheckPhoneAPIView(APIView):
    serializer_class = CheckPhoneSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CheckPhoneSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UpdatePhoneAPIView(APIView):
    serializer_class = UpdatePhoneSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UpdatePhoneSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class VerifyPhoneAPIView(APIView):
    serializer_class = VerifyPhoneSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = VerifyPhoneSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class GetSubscriptionsAPIView(APIView):
    serializer_class = GetSubscriptionsSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = GetSubscriptionsSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)