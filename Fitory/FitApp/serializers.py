from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import CharField, EmailField, BooleanField, DecimalField
from .models import Estado, Ciudad, Servicio, Actividad, Club, ServicioClub, ActividadClub, ActividadHorario, Sucursal, Foto, EvaluacionSucursal, Cliente, EvaluacionCliente, Favorito, Horario, RegistroHorario, Sesion, Subscripcion, Visita, PagoSucursal, Usuario, SubscripcionFree
from django.db.models import Q
from django.core.exceptions import ValidationError
from random import randint
import decimal
from decimal import Decimal
import time
from datetime import datetime, date, time, timedelta
import conekta
import datetime, calendar
from datetime import datetime, timedelta
import os
from PIL import Image
from django.conf import settings
conekta.api_key = 'key_z1MPjh96QF3wgdMeSLNLWA'
conekta.locale = 'es'
Dec = Decimal
import requests
from dateutil.relativedelta import relativedelta
import json

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id','username','email','password')
	def create(self,validated_data):
		user = super(UserSerializer,self).create(validated_data)
		if 'password' in validated_data:
			user.set_password(validated_data['password'])
			user.save()
		return user
	def update(self, instance, validated_data):
		if 'password' in validated_data:
			password = validated_data['password']
			instance.set_password(password)
			instance.save()
		return instance

class UserLoginSerializer(serializers.ModelSerializer):
	token = CharField(allow_blank=True, read_only=True)
	idUser = CharField(allow_blank=True, read_only=True)
	username = CharField(required=False,allow_blank=True)
	email = EmailField(label="Email Address", required=False, allow_blank=True)
	class Meta:
		model = User
		fields = ('username','email','password','token','idUser')
		extra_kwargs = {"password":
			{"write_only":True}
		}
	def validate(self, data): 
		user_obj = None
		email = data.get("email", None)
		username = data.get("username", None)
		password = data["password"]
		if not email and not username:
			raise ValidationError("A username or email is required to login.")
		user = User.objects.filter(Q(email=email)|Q(username=username)).distinct()
		user = user.exclude(email__isnull=True).exclude(email__iexact='')
		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			raise ValidationError("This username/email is not valid.")
		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError("Incorrect credentials, please try again.")
		data["token"] = "TOK"+str(randint(0,9999))
		data["idUser"] = str(user_obj.id)
		return data

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ('id','nombre')

class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = ('id','estado','nombre')

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ('id','nombre','icono')

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ('id','nombre','icono')

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id','user','nombre','fechaIncorporacion','RFC','banco','tarjetahabiente','numCuenta','paginaWeb','facebook','instagram','twitter','evaluacionPromedio','activado','codigoClub','codigoRepresentante','direccion','telefono','correo','foto','fotocrop','cropURL','Legal','fechaLegal')

class ServicioClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioClub
        fields = ('id','sucursal','servicio')

class ActividadClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadClub
        fields = ('id','sucursal','actividad')

class ActividadHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadHorario
        fields = ('id','actividadClub','horaInicio','horaFin','lunes','martes','miercoles','jueves','viernes','sabado','domingo')

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ('id','club','nombre','descripcion','correo','telefono','estado','ciudad','municipio','calle','numExt','numInt','numInt','colonia','cp','latitud','longitud','calificacion','logo','logocrop','cropURL','ibeacon','maximo','minimo','mensualidad','dia','porcentajeCliente','porcentajeUser','saldo','activa','tips','diasPruebas')

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id','user','sucursal','nombre','activo','Legal','fechaLegal')

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ('id','sucursal','lunes','martes','miercoles','jueves','viernes','sabado','domingo','numDias','tipo')

class RegistroHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroHorario
        fields = ('id','sucursal','dia','apertura','cierre')

class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foto
        fields = ('id','sucursal','archivo')

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id','user','nombre','apellido','telefono','hombre','mujer','fechaIngreso','salud','convivir','vermeBien','diversion','estado','ciudad','ubicacion','bluetooth','idFacebook','idGoogle','idCustomer','playerID','foto','fotocrop','cropURL')

class EvaluacionClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionCliente
        fields = ('id','cliente','puntaje')

class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = ('id','cliente','sucursal')

class EvaluacionSucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionSucursal
        fields = ('id','cliente','sucursal','puntaje')

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = ('id','cliente','sucursal','total','sesiones','sesionesRestantes','caducidad','activo')

class SubscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscripcion
        fields = ('id','cliente','sucursal','totalCobrar','totalGym','fechaSubscripcion','fechaRenovacion','activa')

class SubscripcionFreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscripcionFree
        fields = ('id','cliente','sucursal','fechaSubscripcion','fechaFin','direccion','activa')

class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = ('id','cliente','sucursal','fecha','hora')

class PagoSucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoSucursal
        fields = ('id','sucursal','pagar','numRastreo','fecha')

# Consultar fecha
class ConsultaFechaSerializer(serializers.Serializer):
    fecha = serializers.CharField(allow_blank=True,read_only=True)
    def validate(self,data):
        hoy = str(date.today())
        data["fecha"] = hoy
        return data

# Consultar perfil sucursal
class PerfilSucursalSerializer(serializers.Serializer):
    sucursalID = serializers.CharField(max_length=500,required=True)
    clienteID = serializers.CharField(max_length=500,required=True)
    datos = serializers.JSONField(read_only=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self,data):
        sucursalID = data.get("sucursalID",None)
        clienteID = data.get("clienteID",None)
        if not sucursalID and not clienteID:
            error = "Se requiere un id de cliente y un id de sucursal."
            data["error"] = error
        else:
            try:
                sucursal = Sucursal.objects.get(id=sucursalID)
            except Sucursal.DoesNotExist:
                sucursal = False
            try:
                cliente = Cliente.objects.get(id=clienteID)
            except Cliente.DoesNotExist:
                cliente = False
            if sucursal and cliente:
                datos = []
                try:
                    favorito = Favorito.objects.get(cliente=cliente,sucursal=sucursal)
                except Favorito.DoesNotExist:
                    favorito = False
                try:
                    servicios = ServicioClub.objects.filter(sucursal=sucursal)
                except ServicioClub.DoesNotExist:
                    servicios = False
                try:
                    actividades = ActividadClub.objects.filter(sucursal=sucursal)
                except ActividadClub.DoesNotExist:
                    actividades = False
                try:
                    horario = Horario.objects.get(sucursal=sucursal)
                except Horario.DoesNotExist:
                    horario = False
                try:
                    registros = RegistroHorario.objects.filter(sucursal=sucursal)
                except RegistroHorario.DoesNotExist:
                    registros = False
                logo = sucursal.logo.name
                try:
                    fotos = Foto.objects.filter(sucursal=sucursal)
                except Foto.DoesNotExist:
                    fotos = False
                diasPruebas = 0
                if sucursal.diasPruebas == None:
                    diasPruebas = 0
                else:
                    diasPruebas = sucursal.diasPruebas
                free = False
                try:
                    subGratis = SubscripcionFree.objects.get(cliente=cliente,sucursal=sucursal)
                except SubscripcionFree.DoesNotExist:
                    subGratis = False
                if subGratis:
                    free = False
                else:
                    free = True
                info = {
                    'nombre':sucursal.nombre,
                    'descripcion':sucursal.descripcion,
                    'tips':sucursal.tips,
                    'correo':sucursal.correo,
                    'telefono':sucursal.telefono,
                    'municipio':sucursal.municipio,
                    'calle':sucursal.calle,
                    'numExt':sucursal.numExt,
                    'numInt':sucursal.numInt,
                    'colonia':sucursal.colonia,
                    'cp':sucursal.cp,
                    'calificacion':sucursal.calificacion,
                    'latitud':sucursal.latitud,
                    'longitud':sucursal.longitud,
                    'logo':'https://www.fitory.com/media/'+sucursal.logo.name,
                    'logocrop':sucursal.logocrop,
                    'cropURL':sucursal.cropURL,
                    'mensualidad':sucursal.mensualidad,
                    'dia':sucursal.dia,
                    'diasPruebas':diasPruebas,
                    'free':free,
                    'club':[
                        {
                            'foto':'https://www.fitory.com/media/'+sucursal.club.foto.name,
                            'fotocrop':sucursal.club.fotocrop,
                            'cropURL':sucursal.club.cropURL,
                            'paginaWeb':sucursal.club.paginaWeb,
                            'facebook':sucursal.club.facebook,
                            'instagram':sucursal.club.instagram,
                            'twitter':sucursal.club.twitter
                        }
                    ],
                }
                if favorito:
                    info.update({'favorito':favorito.id})
                else:
                    info.update({'favorito':None})
                if servicios:
                    serviciosSuc = []
                    for s in servicios:
                        serv = {
                            'nombre':s.servicio.nombre,
                            'icono':'https://www.fitory.com/media/'+s.servicio.icono.name
                        }
                        serviciosSuc.append(serv)
                    info.update({'servicios':serviciosSuc})
                else:
                    info.update({'servicios':None})
                if actividades:
                    actividadesSuc = []
                    for a in actividades:
                        try:
                            horarios = ActividadHorario.objects.filter(actividadClub=a)
                        except ActividadHorario.DoesNotExist:
                            horarios = False
                        hAct = []
                        if horarios:
                            for h in horarios:
                                inicio = ''
                                if h.horaInicio:
                                    inicio = h.horaInicio.strftime('%I:%M %p')
                                else:
                                    inicio = ''
                                fin = ''
                                if h.horaFin:
                                    fin = h.horaFin.strftime('%I:%M %p')
                                else:
                                    fin = ''
                                h = {
                                    'inicio':inicio,
                                    'fin':fin,
                                    'lunes':str(h.lunes),
                                    'martes':str(h.martes),
                                    'miercoles':str(h.miercoles),
                                    'jueves':str(h.jueves),
                                    'viernes':str(h.viernes),
                                    'sabado':str(h.sabado),
                                    'domingo':str(h.domingo)
                                }
                                hAct.append(h)
                        else:
                            hAct = []
                        act = {
                            'nombre':a.actividad.nombre,
                            'icono':'https://www.fitory.com/media/'+a.actividad.icono.name,
                            'horarios':hAct
                        }
                        actividadesSuc.append(act)
                    info.update({'actividades':actividadesSuc})
                else:
                    info.update({'actividades':None})
                if horario:
                    horarioSuc = []
                    hor = {
                        'lunes':horario.lunes,
                        'martes':horario.martes,
                        'miercoles':horario.miercoles,
                        'jueves':horario.jueves,
                        'viernes':horario.viernes,
                        'sabado':horario.sabado,
                        'domingo':horario.domingo,
                        'numDias':horario.numDias,
                        'tipo':horario.tipo
                    }
                    horarioSuc.append(hor)
                    info.update({'horario':horarioSuc})
                else:
                    info.update({'horario':None})
                if registros:
                    registroHorario = []
                    for r in registros:
                        reg = {
                            'dia':r.dia,
                            'apertura':r.apertura,
                            'cierre':r.cierre
                        }
                        registroHorario.append(reg)
                    info.update({'registroHorario':registroHorario})
                else:
                    info.update({'registroHorario':None})
                if fotos:
                    galeria = []
                    for f in fotos:
                        archivo = 'https://www.fitory.com/media/'+f.archivo.name
                        galeria.append(archivo)
                    info.update({'galeria':galeria})
                else:
                    info.update({'galeria':None})
                datos.append(info)
                data["datos"] = datos
            else:
                error = "Los id proporcionados de cliente y sucursal, no coinciden con los datos registrados."
                data["error"] = error
        return data

# Consultar dias disponibles
class DiasDisponiblesSerializer(serializers.Serializer):
    sucursalID = serializers.CharField(max_length=500,required=True)
    diasDisponibles = serializers.IntegerField(read_only=True)
    diasRestantes = serializers.IntegerField(read_only=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self,data):
        sucursalID = data.get("sucursalID",None)
        try:
            sucursal = Sucursal.objects.get(id=sucursalID)
        except Sucursal.DoesNotExist:
            sucursal = False
        if not sucursalID:
            error = 'Se requiere un id de sucursal.'
            data["error"] = error
        else:
            try:
                sucursal = Sucursal.objects.get(id=sucursalID)
            except Sucursal.DoesNotExist:
                sucursal = False
        if not sucursal:
            error = "No se encontro sucursal con el id proporcionado."
            data["error"] = error        
        else: 
            try:
                horario = Horario.objects.get(sucursal=sucursal)
            except Horario.DoesNotExist:
                horario = False
            if not horario:
                error = "Sucursal sin horario disponible."
                data["error"] = error  
            else:                  
                # now = datetime.strptime("19/1/1 16:30", "%y/%m/%d %H:%M")  
                now = datetime.now() + timedelta(days=1)           
                monthDays = calendar.monthrange(now.year,now.month)[1]                
                start_date = date(now.year, now.month, now.day)
                end_date = date(now.year, now.month, monthDays)
                counter = 0
                for single_date in daterange(start_date, end_date):
                    if single_date.strftime("%A") == "Monday":
                        if horario.lunes:
                            counter += 1
                    elif single_date.strftime("%A") == "Tuesday":
                        if horario.martes:
                            counter += 1
                    elif single_date.strftime("%A") == "Wednesday":
                        if horario.miercoles:
                            counter += 1
                    elif single_date.strftime("%A") == "Thursday":
                        if horario.jueves:
                            counter += 1
                    elif single_date.strftime("%A") == "Friday":
                        if horario.viernes:
                            counter += 1
                    elif single_date.strftime("%A") == "Saturday":
                        if horario.sabado:
                            counter += 1
                    elif single_date.strftime("%A") == "Sunday":
                        if horario.domingo:
                            counter += 1
                now = now - timedelta(days=1)        
                data["diasRestantes"] = calendar.monthrange(now.year,now.month)[1]-now.day
                data["diasDisponibles"] = counter
           
        return data

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

# Conekta
class CustomerConektaSerializer(serializers.Serializer):
    clienteID = serializers.CharField(max_length=500,required=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    mensaje = serializers.CharField(allow_blank=True,read_only=True)
    customerID = serializers.CharField(allow_blank=True,read_only=True)
    def validate(self,data):
        clienteID = data.get("clienteID",None)
        if not clienteID:
            error = "Se requiere un id de cliente."
            data["error"] = error
        else:
            try:
                cliente = Cliente.objects.get(id=clienteID)
            except Cliente.DoesNotExist:
                cliente = False
            if not cliente:
                error = "El id proporcionado no esta relacionado a los registros de clientes."
                data["error"] = error
            else:
                if not cliente.idCustomer:
                    try:
                        customer = conekta.Customer.create({
                            'name':cliente.nombre,
                            'email':cliente.user.email
                        })
                    except conekta.ConektaError as e:
                        error = e.message
                        data["error"] = error
                        customer = False
                    if customer:
                        cliente.idCustomer = customer.id
                        cliente.save()
                        mensaje = 'Customer creado correctamente.'
                        data["mensaje"] = mensaje
                        data["customerID"] = customer.id
        return data

class BorrarCustomerConektaSerializer(serializers.Serializer):
    clienteID = serializers.CharField(max_length=500,required=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    mensaje = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self,data):
        clienteID = data.get("clienteID",None)
        if not clienteID:
            error = "Se requiere un id de cliente."
            data["error"] = error
        else:
            try:
                cliente = Cliente.objects.get(id=clienteID)
            except Cliente.DoesNotExist:
                cliente = False
            if not cliente:
                error = "El id proporcionado no esta relacionado a los registros de clientes."
                data["error"] = error
            else:
                if cliente.idCustomer:
                    customerID = cliente.idCustomer
                    customer = False
                    try:
                        customer = conekta.Customer.find(customerID)
                    except:
                        customer = False
                    if customer:
                        customer.delete()
                        data["mensaje"] = "Customer borrado."
                        cliente.idCustomer = None
                        cliente.save()
                    else:
                        error = "No hay customer."
                        data["error"] = error
                else:
                    error = "El cliente no tiene id de customer."
                    data["error"] = error
        return data

class addMetodoPagoSerializer(serializers.Serializer):
    clienteID = serializers.CharField(max_length=500,required=True)
    token = serializers.CharField(max_length=500, required=True)
    nuevoMetodo = serializers.CharField(allow_blank=True, read_only=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self,data):
        clienteID = data.get("clienteID",None)
        token = data.get("token",None)
        if not token:
            error = "Se requiere un token de seguridad."
            data["error"] = error
        if not clienteID:
            error = "Se requiere un id de cliente."
            data["error"] = error
        else:
            try:
                cliente = Cliente.objects.get(id=clienteID)
            except Cliente.DoesNotExist:
                cliente = False
            if not cliente:
                error = "Id de cliente proporcionado no coincide con los registros de clientes."
                data["error"] = error
            else:
                if cliente.idCustomer:
                    customerID = cliente.idCustomer
                    customer = conekta.Customer.find(customerID)
                    customer = False
                    try:
                        customer = conekta.Customer.find(customerID)
                    except:
                        customer = False
                    if customer:
                        try:
                            source = customer.createPaymentSource({
                                "type":"card",
                                "token_id":token
                            })
                        except conekta.ConektaError as e:
                            error = e.message
                            data["error"] = error
                            source = False
                        if source:
                            data["nuevoMetodo"] = source.id
                    else:
                        error = "No existe customer relacionado al cliente."
                        data["error"] = error
                else:
                    error = "El cliente no tiene id de customer."
                    data["error"] = error
        return data

class MetodosPagoSerializer(serializers.Serializer):
    clienteID = serializers.CharField(max_length=500,required=True)
    metodos = serializers.JSONField(read_only=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self,data):
        clienteID = data.get("clienteID",None)
        if not clienteID:
            error = "Se requiere un id de cliente."
            data["error"] = error
        else:
            try:
                cliente = Cliente.objects.get(id=clienteID)
            except Cliente.DoesNotExist:
                cliente = False
            if not cliente:
                error = "Id de cliente proporcionado no coincide con los registros de clientes."
                data["error"] = error
            else:
                if cliente.idCustomer:
                    customerID = cliente.idCustomer
                    customer = conekta.Customer.find(customerID)
                    customer = False
                    try:
                        customer = conekta.Customer.find(customerID)
                    except:
                        customer = False
                    if customer:
                        listaMetodos = []
                        metodosPago = False
                        try:
                            metodosPago = customer.payment_sources
                        except:
                            metodosPago = False
                        if metodosPago:
                            for m in metodosPago:
                                tarjeta = {'id':m.id,'last4':m.last4,'brand':m.brand}
                                listaMetodos.append(tarjeta)
                            data["metodos"] = listaMetodos
                        else:
                            error = "El customer del cliente no tiene metodos de pago registrados."
                            data["error"] = error
                    else:
                        error = "No existe customer relacionado al cliente."
                        data["error"] = error
                else:
                    error = "El cliente no tiene id de customer."
                    data["error"] = error
        return data

class deleteMetodoPagoSerializer(serializers.Serializer):
    clienteID = serializers.CharField(max_length=500,required=True)
    metodoID = serializers.CharField(max_length=500,required=True)
    mensaje = serializers.CharField(allow_blank=True, read_only=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self,data):
        clienteID = data.get("clienteID",None)
        metodoID=data.get("metodoID",None)
        if not metodoID:
            error = "Se requiere un id de metodo de pago."
            data["error"] = error
        if not clienteID:
            error = "Se requiere un id de cliente."
            data["error"] = error
        else:
            try:
                cliente = Cliente.objects.get(id=clienteID)
            except Cliente.DoesNotExist:
                cliente = False
            if not cliente:
                error = "Id de cliente proporcionado no coincide con los registros de clientes."
                data["error"] = error
            else:
                if cliente.idCustomer:
                    customerID = cliente.idCustomer
                    customer = False
                    try:
                        customer = conekta.Customer.find(customerID)
                    except:
                        customer = False
                    if customer:
                        metodosPago = False
                        try:
                            metodosPago = customer.payment_sources
                        except:
                            metodosPago = False
                        if metodosPago:
                            for m in metodosPago:
                                if m.id == metodoID:
                                    m.delete()
                                    data["mensaje"] = 'Tarjeta eliminada.'
                        else:
                            error = "El customer del cliente no tiene metodos de pago registrados."
                            data["error"] = error
                    else:
                        error = "No existe customer relacionado al cliente."
                        data["error"] = error
                else:
                    error = "El cliente no tiene id de customer."
                    data["error"] = error
        return data

# class SubscripcionMensualSerializer(serializers.Serializer):
#     clienteID = serializers.CharField(max_length=500,required=True)
#     sucursalID = serializers.CharField(max_length=500,required=True)
#     mensaje = serializers.CharField(allow_blank=True, read_only=True)
#     error = serializers.CharField(allow_blank=True, read_only=True)
#     def validate(self,data):
#         clienteID = data.get("clienteID",None)
#         sucursalID = data.get("sucursalID",None)
#         if not clienteID:
#             error = "Se requiere un id de cliente."
#             data["error"] = error
#         if not sucursalID:
#             error = "Se requiere un id de sucursal."
#             data["error"] = error
#         if clienteID and sucursalID:
#             try:
#                 cliente = Cliente.objects.get(id=clienteID)
#             except Cliente.DoesNotExist:
#                 cliente = False
#             try:
#                 sucursal = Sucursal.objects.get(id=sucursalID)
#             except Sucursal.DoesNotExist:
#                 sucursal = False
#             if not cliente and not sucursal:
#                 error = "No hay cliente que coincida con el id de cliente proporcionado, y no hay sucursal que coincida con el id de sucursal proporcionada."
#                 data["error"] = error
#             elif cliente and not sucursal:
#                 error = "No hay sucursal que coincida con el id de sucursal proporcionada."
#                 data["error"] = error
#             elif not cliente and sucursal:
#                 error = "No hay cliente que coincida con el id de cliente proporcionado."
#                 data["error"] = error
#             elif cliente and sucursal:
#                 if cliente.idCustomer:
#                     customerID = cliente.idCustomer
#                     customer = conekta.Customer.find(customerID)
#                     customer = False
#                     try:
#                         customer = conekta.Customer.find(customerID)
#                     except:
#                         customer = False
#                     if customer:
#                         metodosPago = False
#                         try:
#                             metodosPago = customer.payment_sources
#                         except:
#                             metodosPago = False
#                         if metodosPago:
#                             subscripcion = False
#                             try:
#                                 subscripcion = customer.subscription
#                             except:
#                                 subscripcion = False
#                             if not subscripcion:
#                                 idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id)
#                                 try:
#                                     planConektaSucursal = conekta.Plan.find(idPlan)
#                                 except:
#                                     planConektaSucursal = False
#                                 if planConektaSucursal:
#                                     nuevaSubscripcion = False
#                                     try:
#                                         nuevaSubscripcion = customer.createSubscription({"plan":idPlan})
#                                     except:
#                                         nuevaSubscripcion = False
#                                     if nuevaSubscripcion:
#                                         totalCobrar = Dec(sucursal.mensualidad)
#                                         hoy = date.today()
#                                         fechaRenovacion = hoy + relativedelta(months=1)
#                                         totalGym = totalCobrar * Dec(0.9)
#                                         subscripcion = Subscripcion(cliente=cliente,sucursal=sucursal,totalCobrar=totalCobrar,totalGym=totalGym,fechaRenovacion=fechaRenovacion,activa=True)
#                                         subscripcion.save()
#                                         mensaje = 'Subscripcion creada exitosamente.'
#                                         data["mensaje"] = mensaje
#                                     else:
#                                         error = 'No se pudo crear la subscripcion.'
#                                         data["error"] = error
#                                 else:
#                                     error = 'No existe un plan registrado para esta sucursal.'
#                                     data["error"] = error
#                             else:
#                                 idPlan = "Plan_Suc"+str(sucursal.id)+'_Club_'+str(sucursal.club.id)
#                                 try:
#                                     planConektaSucursal = conekta.Plan.find(idPlan)
#                                 except:
#                                     planConektaSucursal = False
#                                 if planConektaSucursal:
#                                     try:
#                                         subscripcionUpdate = customer.subscription.update({
#                                             "plan":idPlan
#                                         })
#                                     except:
#                                         subscripcionUpdate = False
#                                     if subscripcionUpdate:
#                                         try:
#                                             subscripcionesCliente = Subscripcion.objects.filter(cliente=cliente)
#                                         except Subscripcion.DoesNotExist:
#                                             subscripcionesCliente = False
#                                         if subscripcionesCliente:
#                                             for s in subscripcionesCliente:
#                                                 s.activa = False
#                                                 s.save()
#                                         totalCobrar = Dec(sucursal.mensualidad)
#                                         hoy = date.today()
#                                         fechaRenovacion = hoy + relativedelta(months=1)
#                                         totalGym = totalCobrar * Dec(0.9)
#                                         subscripcion = Subscripcion(cliente=cliente,sucursal=sucursal,totalCobrar=totalCobrar,totalGym=totalGym,fechaRenovacion=fechaRenovacion,activa=True)
#                                         subscripcion.save()
#                                         mensaje = 'Subscripcion actualizada exitosamente.'
#                                         data["mensaje"] = mensaje
#                                     else:
#                                         error = 'No se pudo actualizar la subscripcion'
#                                         data['error'] = error
#                                 else:
#                                     error = 'No hay plan con ese id'
#                                     data['error'] = error
#                         else:
#                             error = "El customer del cliente no tiene metodos de pago registrados."
#                             data["error"] = error
#                     else:
#                         error = "No existe customer relacionado al cliente."
#                         data["error"] = error
#                 else:
#                     error = "El cliente no tiene id de customer."
#                     data["error"] = error
#         return data

class SubscripcionMensualSerializer(serializers.Serializer):
    clienteID = serializers.CharField(max_length=500,required=True)
    sucursalID = serializers.CharField(max_length=500,required=True)
    direccion = serializers.CharField(max_length=500)
    mensaje = serializers.CharField(allow_blank=True, read_only=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self,data):
        clienteID = data.get("clienteID",None)
        sucursalID = data.get("sucursalID",None)
        direccion = data.get("direccion",None)
        if not clienteID:
            error = "Se requiere un id de cliente."
            data["error"] = error
        if not sucursalID:
            error = "Se requiere un id de sucursal."
            data["error"] = error
        if not direccion:
            error = "Se requiere una direccion."
            data["error"] = error
        if clienteID and sucursalID and direccion:
            try:
                cliente = Cliente.objects.get(id=clienteID)
            except Cliente.DoesNotExist:
                cliente = False
            try:
                sucursal = Sucursal.objects.get(id=sucursalID)
            except Sucursal.DoesNotExist:
                sucursal = False
            if cliente and sucursal:
                if cliente.idCustomer:
                    customerID = cliente.idCustomer
                    customer = False
                    try:
                        customer = conekta.Customer.find(customerID)
                    except:
                        customer = False
                    if customer:
                        try:
                            subscripciones = Subscripcion.objects.get(cliente=cliente,activa=True,sucursal=sucursal)
                        except Subscripcion.DoesNotExist:
                            subscripciones = False
                        if not subscripciones:
                            totalCobrar = Dec(sucursal.mensualidad)
                            cincoPorCiento = (totalCobrar * 5)/100
                            totalCobrar = totalCobrar + cincoPorCiento
                            hoy = date.today()
                            fechaRenovacion = hoy + relativedelta(months=1)
                            totalGym = Dec(sucursal.mensualidad) * Dec(0.9)
                            totalCentavos = (int(totalCobrar)*100)
                            name = 'Subscripcion mensual'
                            errorCon = ''
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
                            except conekta.ConektaError as e:
                                cargo = False
                                errorCon = e
                            if cargo:
                                subscripcion = Subscripcion(cliente=cliente,sucursal=sucursal,totalCobrar=totalCobrar,totalGym=totalGym,fechaRenovacion=fechaRenovacion,activa=True)
                                subscripcion.save()
                                mensaje = 'Subscripcion creada exitosamente.'
                                data["mensaje"] = mensaje
                            else:
                                error = "No pudo crearse el cargo de la subscripcion."
                                data["error"] = error
                        else:
                            error = "Ya tienes una subscripcion en esta sucursal"
                            data["error"] = error
                    else:
                        error = "No existe customer relacionado al cliente."
                        data["error"] = error
                else:
                    error = "El cliente no tiene id de customer."
                    data["error"] = error
            elif cliente and not sucursal:
                error = "No se pudo crear la subscripcion, ya que no hay sucursal con el id proporcionado."
                data["error"] = error
            elif not cliente and sucursal:
                error = "No se pudo crear la subscripcion, ya que no hay cliente con el id proporcionado."
                data["error"] = error
            else:
                error = "No se pudo crear la subscripcion, ya que no hay cliente con el id proporcionado, ni sucursal con el id proporcionado."
                data["error"] = error
        else:
            error = "Se requiere enviar juntos id cliente, id sucursal y direccion"
            data["error"] = error
        return data

class CancelarSubscripcionMensualSerializer(serializers.Serializer):
    clienteID = serializers.CharField(max_length=500,required=True)
    subscripcionID = serializers.CharField(max_length=500,required=True)
    mensaje = serializers.CharField(allow_blank=True, read_only=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self,data):
        clienteID = data.get("clienteID",None)
        subscripcionID = data.get("subscripcionID",None)
        if not clienteID:
            error = "Se requiere un id de cliente."
            data["error"] = error
        else:
            try:
                cliente = Cliente.objects.get(id=clienteID)
            except Cliente.DoesNotExist:
                cliente = False
            if not cliente:
                error = "Id de cliente proporcionado no coincide con los registros de clientes."
                data["error"] = error
            else:
                if not subscripcionID:
                    error = "Se requiere un id de subscripcion."
                    data["error"] = error
                else:
                    try:
                        subscripcion = Subscripcion.objects.get(id=subscripcionID)
                    except Subscripcion.DoesNotExist:
                        subscripcion = False
                    if subscripcion:
                        subscripcion.activa = False
                        subscripcion.save()
                        mensaje = "Subscripcion cancelada exitosamente"
                        data["mensaje"] = mensaje
                    else:
                        error = "No existe registro de subscripcion con el id proporcionado."
                        data["error"] = error
        return data

class ActualizarSubscripcionMensualSerializer(serializers.Serializer):
    clienteID = serializers.CharField(max_length=500,required=True)
    metodoPagoID = serializers.CharField(max_length=500,required=True)
    mensaje = serializers.CharField(allow_blank=True, read_only=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self,data):
        clienteID = data.get("clienteID",None)
        metodoPagoID = data.get("metodoPagoID",None)
        if not clienteID:
            error = "Se requiere un id de cliente."
            data["error"] = error
        else:
            try:
                cliente = Cliente.objects.get(id=clienteID)
            except Cliente.DoesNotExist:
                cliente = False
            if not cliente:
                error = "Id de cliente proporcionado no coincide con los registros de clientes."
                data["error"] = error
            else:
                if cliente.idCustomer:
                    customerID = cliente.idCustomer
                    customer = False
                    try:
                        customer = conekta.Customer.find(customerID)
                    except:
                        customer = False
                    if customer:
                        subscripcion = False
                        try:
                            subscripcion = customer.subscription
                        except:
                            subscripcion = False
                        if subscripcion:
                            plan = subscripcion.id
                            if metodoPagoID:
                                try:
                                    subscripcionUpdate = customer.subscription.update({
                                        "plan":plan,
                                        "card":metodoPagoID
                                    })
                                except:
                                    subscripcionUpdate = False
                                if subscripcionUpdate:
                                    mensaje = "Subscripcion actualizada exitosamente"
                                    data["mensaje"] = mensaje
                                else:
                                    error = "No se pudo actualizar el metodo de pago para su subscripcion."
                                    data["error"] = error
                            else:
                                error = "Se requiere un id de metodo de pago."
                                data["error"] = error
                        else:
                            error = "El cliente no tiene una subscripcion."
                            data["error"]
                    else:
                        error = "No existe customer relacionado al cliente."
                        data["error"] = error
                else:
                    error = "El cliente no tiene id de customer."
                    data["error"] = error
        return data

class CobrarPorSesionSerializer(serializers.Serializer):
    clienteID = serializers.CharField(max_length=500,required=True)
    metodoPagoID = serializers.CharField(max_length=500,required=True)
    sucursalID = serializers.CharField(max_length=500,required=True)
    numeroSesiones = serializers.CharField(max_length=500,required=True)
    mensaje = serializers.CharField(allow_blank=True, read_only=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self, data):
        clienteID = data.get("clienteID",None)
        metodoPagoID = data.get("metodoPagoID",None)
        sucursalID = data.get("sucursalID",None)
        numeroSesiones = data.get("numeroSesiones",None)
        if not clienteID:
            error = "Se requiere un id de cliente."
            data["error"] = error
        if not sucursalID:
            error = "Se requiere un id de sucursal."
            data["error"] = error
        if not metodoPagoID:
            error = "Se requiere un id de metodo de pago."
            data["error"] = error
        if not numeroSesiones:
            error = "Se requiere un numero de sesiones."
            data["error"] = error
        if clienteID and sucursalID and metodoPagoID and numeroSesiones:
            try:
                cliente = Cliente.objects.get(id=clienteID)
            except Cliente.DoesNotExist:
                cliente = False
            if not cliente:
                error = "Id de cliente proporcionado no coincide con los registros de clientes."
                data["error"] = error
            else:
                if cliente.idCustomer:
                    customerID = cliente.idCustomer
                    customer = False
                    try:
                        customer = conekta.Customer.find(customerID)
                    except:
                        customer = False
                    if customer:
                        if sucursalID:
                            try:
                                sucursal = Sucursal.objects.get(id=sucursalID)
                            except Sucursal.DoesNotExist:
                                sucursal = False
                            if sucursal:
                                precioDia = Dec(sucursal.dia)
                                if precioDia > 0:
                                    numeroSesiones = int(numeroSesiones)
                                    total = precioDia * numeroSesiones
                                    totalCentavos = int(float(total)) * 100
                                    name = 'Subscripcion por '+str(numeroSesiones)+' sesiones.'
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
                                                    "payment_source_id":metodoPagoID,
							                        "type": "card"
                                                }
                                            }]
                                        })
                                    except:
                                        cargo = False
                                    if cargo:
                                        mensaje = "Cargo creado exitosamente"
                                        data["mensaje"] = mensaje
                                    else:
                                        error = "No se pudo crear el cargo."
                                        data["error"] = error
                                else:
                                    error = "Precio por sesion no establecido para esta sucursal."
                                    data["error"] = error
                            else:
                                error = "El id de sucursal proporcionado no coincide con los registros."
                                data["error"] = error
                        else:
                            error = "El id de sucursal proporcionado no coincide con los registros."
                            data["error"] = error
                    else:
                        error = "El cliente no tiene id de customer."
                        data["error"] = error
                else:
                    error = "El cliente no tiene id de customer."
                    data["error"] = error
        else:
            error = "Favor de ingresar todos los datos requeridos."
            data["error"] = error
        return data

class ActualizarFotoClienteSerializer(serializers.Serializer):
    mensaje = serializers.CharField(allow_blank=True, read_only=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    fotoUrl = serializers.CharField(allow_blank=True, read_only=True)
    clienteID = serializers.CharField(max_length=5000, required = True)
    foto = serializers.ImageField(use_url='clientes/',required = True)
    def validate(self, data):
        clienteID = data.get("clienteID",None)
        foto = data.get("foto", None)
        if not clienteID:
            error = "Se requiere un id de cliente"
            data["error"] = error
        else: 
            try:
                cliente = Cliente.objects.get(id=clienteID)
            except Cliente.DoesNotExist:
                cliente = False
            if not cliente:
                error = "Id de cliente proporcionado no coincide con los registros de clientes."
                data["error"] = error
            else:
                fotoActual = cliente.foto.name
                if not fotoActual == 'default/perfil.png':
                    os.remove(cliente.foto.path)
                cliente.foto = foto
                cliente.save()        
                data['mensaje'] = "Foto de perfil actualizada correctamente."
                data['fotoUrl'] = cliente.foto.name                                 
        return data
    
class CalcularPromedioEvaluacionesSerializer(serializers.Serializer):
    idSucursal = serializers.IntegerField(max_value=None, min_value=None,required=True)
    calificacionSucursal = serializers.CharField(allow_blank=True, read_only=True)
    calificacionClub = serializers.CharField(allow_blank=True, read_only=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self, data):
        idSucursal = data.get("idSucursal",None)
        if not idSucursal:
            error = "Se requiere un id de sucursal."
            data["error"] = error
        else:
            try:
                sucursal = Sucursal.objects.get(id=idSucursal)
            except Sucursal.DoesNotExist:
                sucursal = False
            if not sucursal:
                error = "El id de sucursal no coincide con los registros."
                data["error"] = error
            else:
                try:
                    evaluaciones1Estrella = EvaluacionSucursal.objects.filter(sucursal=sucursal,puntaje=1)
                except EvaluacionSucursal.DoesNotExist:
                    evaluaciones1Estrella = False
                numEv1Estrella = Decimal(len(evaluaciones1Estrella))
                try:
                    evaluaciones2Estrella = EvaluacionSucursal.objects.filter(sucursal=sucursal,puntaje=2)
                except EvaluacionSucursal.DoesNotExist:
                    evaluaciones2Estrella = False
                numEv2Estrella = Decimal(len(evaluaciones2Estrella))
                try:
                    evaluaciones3Estrella = EvaluacionSucursal.objects.filter(sucursal=sucursal,puntaje=3)
                except EvaluacionSucursal.DoesNotExist:
                    evaluaciones3Estrella = False
                numEv3Estrella = Decimal(len(evaluaciones3Estrella))
                try:
                    evaluaciones4Estrella = EvaluacionSucursal.objects.filter(sucursal=sucursal,puntaje=4)
                except EvaluacionSucursal.DoesNotExist:
                    evaluaciones4Estrella = False
                numEv4Estrella = Decimal(len(evaluaciones4Estrella))
                try:
                    evaluaciones5Estrella = EvaluacionSucursal.objects.filter(sucursal=sucursal,puntaje=5)
                except EvaluacionSucursal.DoesNotExist:
                    evaluaciones5Estrella = False
                numEv5Estrella = Decimal(len(evaluaciones5Estrella))
                totalEvaluacionesSucursal = Decimal(numEv1Estrella + numEv2Estrella + numEv3Estrella + numEv4Estrella + numEv5Estrella)
                if totalEvaluacionesSucursal > 0:
                    sumatoriaEstrellas = (1*numEv1Estrella)+(2*numEv2Estrella)+(3*numEv3Estrella)+(4*numEv4Estrella)+(5*numEv5Estrella)
                    promedioSucursal = (sumatoriaEstrellas)/totalEvaluacionesSucursal
                    sucursal.calificacion = promedioSucursal
                    sucursal.save()
                    data['calificacionSucursal'] = promedioSucursal
                else:
                    error = 'El numero de evaluaciones es 0, no puede calcularse el promedio.'
                    data["error"] = error
                club = sucursal.club
                try:
                    evaluaciones1EstrellaClub = EvaluacionSucursal.objects.filter(sucursal__club=club,puntaje=1)
                except EvaluacionSucursal.DoesNotExist:
                    evaluaciones1EstrellaClub = False
                numEv1EstrellaClub = Decimal(len(evaluaciones1EstrellaClub))
                try:
                    evaluaciones2EstrellaClub = EvaluacionSucursal.objects.filter(sucursal__club=club,puntaje=2)
                except EvaluacionSucursal.DoesNotExist:
                    evaluaciones2EstrellaClub = False
                numEv2EstrellaClub = Decimal(len(evaluaciones2EstrellaClub))
                try:
                    evaluaciones3EstrellaClub = EvaluacionSucursal.objects.filter(sucursal__club=club,puntaje=3)
                except EvaluacionSucursal.DoesNotExist:
                    evaluaciones3EstrellaClub = False
                numEv3EstrellaClub = Decimal(len(evaluaciones3EstrellaClub))
                try:
                    evaluaciones4EstrellaClub = EvaluacionSucursal.objects.filter(sucursal__club=club,puntaje=4)
                except EvaluacionSucursal.DoesNotExist:
                    evaluaciones4EstrellaClub = False
                numEv4EstrellaClub = Decimal(len(evaluaciones4EstrellaClub))
                try:
                    evaluaciones5EstrellaClub = EvaluacionSucursal.objects.filter(sucursal__club=club,puntaje=5)
                except EvaluacionSucursal.DoesNotExist:
                    evaluaciones5EstrellaClub = False
                numEv5EstrellaClub = Decimal(len(evaluaciones5EstrellaClub))
                totalEvaluacionesClub = Decimal(numEv1EstrellaClub+numEv2EstrellaClub+numEv3EstrellaClub+numEv4EstrellaClub+numEv5EstrellaClub)
                if totalEvaluacionesClub > 0:
                    sumatoriaEstrellasClub = (1*numEv1EstrellaClub)+(2*numEv2EstrellaClub)+(3*numEv3EstrellaClub)+(4*numEv4EstrellaClub)+(5*numEv5EstrellaClub)
                    promedioClub = (sumatoriaEstrellasClub)/totalEvaluacionesClub
                    club.evaluacionPromedio = promedioClub
                    club.save()
                    data['calificacionClub'] = promedioClub
                else:
                    error = 'El numero de evaluaciones es 0, no puede calcularse el promedio.'
                    data["error"] = error
        return data

# API para registrar la visita de un cliente
# @params idCliente, idSucursal
# @returns message, error
class RegistrarVisitaSerializer(serializers.Serializer):
    idCliente = serializers.IntegerField(max_value=None, min_value=None,required=True)
    idSucursal = serializers.IntegerField(max_value=None, min_value=None,required=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    message = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self, data):
        idCliente = data.get("idCliente",None)
        idSucursal = data.get("idSucursal",None)
        
        try:
            today = str(date.today())
            cliente = Cliente.objects.get(id=idCliente)
            sucursal = Sucursal.objects.get(id=idSucursal)   
            
            try:
                visitaRegistrada = Visita.objects.get(sucursal=sucursal,cliente=cliente,fecha=today)                               

            except Visita.DoesNotExist:
                visitaRegistrada = False

            if visitaRegistrada:
                data['message'] = "El cliente ya cuenta con una visita registrada"                   

            else: 
                try:
                    subscripcion = Subscripcion.objects.get(cliente=cliente,sucursal=sucursal,activa=True)

                except Subscripcion.DoesNotExist:
                    subscripcion = False                

                if subscripcion:

                    if subscripcion.fechaRenovacion<date.today():
                        data['message'] = "Cliente sin subscripcion mensual vigente"
                        subscripcion.activa = False
                        subscripcion.save()

                    else:
                        visita = Visita(sucursal=sucursal,cliente=cliente)
                        visita.save()                         
                        data['message'] = "Visita registrada"                    

                else: 
                    try:
                        sesion = Sesion.objects.get(cliente=cliente,sucursal=sucursal,activo=True)

                    except Sesion.DoesNotExist:
                        sesion = False
                    
                    if sesion:                        

                        if sesion.sesionesRestantes>0:                            

                            if sesion.caducidad<date.today():
                                data['message'] = "Cliente sin sesiones vigentes"
                                sesion.activo = False
                                sesion.save()
                            else:
                                visita = Visita(sucursal=sucursal,cliente=cliente)
                                visita.save()
                                sesion.sesionesRestantes = int(sesion.sesionesRestantes) - int(1)
                                sesion.save()                        
                                data['message'] = "Visita registrada"

                        else:
                            data['message'] = "Cliente sin sesiones restantes"
                            sesion.activo = False
                            sesion.save()

                    else:
                        try:
                            subscripcionF = SubscripcionFree.objects.get(cliente=cliente,sucursal=sucursal,activa=True)

                        except SubscripcionFree.DoesNotExist:
                            subscripcionF = False
                        
                        if subscripcionF:
                            if subscripcionF.fechaFin<date.today():
                                subscripcionF.activa = False
                                subscripcionF.save()
                                data['message'] = "Cliente sin sesiones"
                            else:
                                visita = Visita(sucursal=sucursal,cliente=cliente)
                                visita.save()                         
                                data['message'] = "Visita registrada" 
                        else:      
                            data['message'] = "Cliente sin sesiones"

        except Exception as e:
            error = 'El id del cliente o sucursal no se encuentra(n) registrado(s)'        
            data['error'] = error

        return data

# visita = Visita(sucursal=sucursal,cliente=cliente)
                # visita.save()

# API para revisar si un cliente ya tiene registrada la asistencia en una sucursal
# @params idCliente, beacon, maximo, minimo
# @returns  idSucursal, visita, error
class RevisarVisitaSerializer(serializers.Serializer):
    idCliente = serializers.IntegerField(max_value=None, min_value=None,required=True)
    beacon = serializers.CharField(max_length=100,required=True)
    maximo = serializers.IntegerField(max_value=None, min_value=None,required=True)
    minimo = serializers.IntegerField(max_value=None, min_value=None,required=True)
    error = serializers.CharField(allow_blank=True, read_only=True)
    idSucursal = serializers.IntegerField(max_value=None, min_value=None,read_only=True)
    visita = serializers.BooleanField(read_only=True)
    def validate(self, data):
        maximo = data.get("maximo",None)
        minimo = data.get("minimo",None)
        beacon = data.get("beacon",None)
        idCliente = data.get("idCliente",None)
        try:
            cliente = Cliente.objects.get(id=idCliente)
            today = str(date.today())
            sucursal = Sucursal.objects.get(maximo=maximo,minimo=minimo,ibeacon=beacon)
            idSucursal = sucursal.id
            data['idSucursal'] = idSucursal
            try:
                visitaRegistrada = Visita.objects.get(sucursal=sucursal,cliente=cliente,fecha=today)               
                if visitaRegistrada:
                    visita = True                   
                    data['visita'] = visita
                else: 
                    visita = False
                    data['visita'] = visita
            except Visita.DoesNotExist:
                visita = False
                data['visita'] = visita         
        except Exception as e:
            error = 'El id del cliente o sucursal no se encuentra(n) registrado(s)'        
            data['error'] = error

        return data


class  RevisarSubscripcionFreeSerializer(serializers.Serializer):
    idCliente = serializers.IntegerField(max_value=None, min_value=None,required=True)
    idSucursal = serializers.IntegerField(max_value=None, min_value=None,required=True)
    msg = serializers.CharField(allow_blank=True, read_only=True)
    mostrar = serializers.BooleanField(read_only=True)

    def validate(self, data):
        idCliente = data.get("idCliente",None)
        idSucursal = data.get("idSucursal",None)
        try:        
            cliente = Cliente.objects.get(id=idCliente)            
        except Cliente.DoesNotExist:            
            msg = u'Cliente no registrado'
            data['msg'] = msg
            return data

        try:        
            sucursal = Sucursal.objects.get(id=idSucursal,activa=True)    
            if sucursal.diasPruebas == '' or sucursal.diasPruebas == 0 or sucursal.diasPruebas == None:
                msg = u'Sucursal sin dias de prueba'
                data['mostrar'] = False
                data['msg'] = msg
                return data                
        except Sucursal.DoesNotExist:            
            msg = u'Sucursal no registrada'
            data['msg'] = msg
            return data

        try: 
            suscripcion = Subscripcion.objects.filter(cliente=idCliente)
        except Subscripcion.DoesNotExist:
            suscripcion = False

        try: 
            sesiones = Sesion.objects.filter(cliente=idCliente)
        except Sesion.DoesNotExist:
            sesiones = False

        try: 
            suscripcionF = SubscripcionFree.objects.filter(cliente=idCliente,sucursal=sucursal)
        except SubscripcionFree.DoesNotExist:
            suscripcionF = False


        if sesiones or suscripcion or suscripcionF:
                msg = u'Cliente ya ha realizado alguna compra. No aplica promocion'
                data['msg'] = msg
                data['mostrar'] = False
                return data
        else:                            
            # print abs(ingreso-datetime.now()).days 
            data['mostrar'] = True
            return data                        




class  ActivarSubscripcionFreeSerializer(serializers.Serializer):
    idCliente = serializers.IntegerField(max_value=None, min_value=None,required=True)
    idSucursal = serializers.IntegerField(max_value=None, min_value=None,required=True)
    msg = serializers.CharField(allow_blank=True, read_only=True)    
    
    def validate(self, data):
        idCliente = data.get("idCliente",None)
        idSucursal = data.get("idSucursal",None)
        try:        
            cliente = Cliente.objects.get(id=idCliente)   
            if cliente.telefono == '' or cliente.telefono == 0 or cliente.telefono == None or cliente.telefono == "...":
                msg = u'Usuario sin celular registrado'
                data['msg'] = msg
                return data                      
        except Cliente.DoesNotExist:            
            msg = u'Cliente no registrado'
            data['msg'] = msg
            return data
        
        try:        
            sucursal = Sucursal.objects.get(id=idSucursal,activa=True)  
            if sucursal.diasPruebas == '' or sucursal.diasPruebas == 0 or sucursal.diasPruebas == None:
                msg = u'Sucursal sin dias de prueba'
                data['msg'] = msg
                return data 
            targetURL = "https://api.smsmasivos.com.mx/auth"
            body = {'apikey':"d40b8b72851957ad4f4382f5860027086f7a777e"}
            r = requests.post(url = targetURL, data = body)
            response = json.loads(r.text)
            token = response['token']   

            targetURL = "https://api.smsmasivos.com.mx/protected/json/phones/verification/start"
            headers = {
            'token':token
            }
            body = {
            'phone_number':cliente.telefono,
            'country_code':"52"
            }
            r = requests.post(url = targetURL, data = body, headers = headers)
            response = json.loads(r.text)        
            data["mensaje"] = response["message"]
            data["code"] = response["code"]
            code = response["code"]        
            if code == "verification_04":                             
                try:
                    horario = Horario.objects.get(sucursal=sucursal)
                    try: 
                        suscripcionF = SubscripcionFree.objects.get(cliente=idCliente,sucursal=sucursal)
                    except SubscripcionFree.DoesNotExist:
                        suscripcionF = False

                    if suscripcionF:
                        msg = u'Subscripcion gratuita ya activada'
                        data['msg'] = msg
                        return data    
                    now = datetime.now() + timedelta(days=1) 
                    later = datetime.now() + relativedelta(months=2)
                    # monthDays = calendar.monthrange(now.year,now.month)[1]                
                    start_date = date(now.year, now.month, now.day)
                    end_date = date(later.year, later.month, later.day)            
                    counter = 0
                    for single_date in daterange(start_date, end_date):
                        if single_date.strftime("%A") == "Monday":
                            if horario.lunes:
                                counter += 1                        
                        elif single_date.strftime("%A") == "Tuesday":
                            if horario.martes:
                                counter += 1
                        elif single_date.strftime("%A") == "Wednesday":
                            if horario.miercoles:
                                counter += 1
                        elif single_date.strftime("%A") == "Thursday":
                            if horario.jueves:
                                counter += 1
                        elif single_date.strftime("%A") == "Friday":
                            if horario.viernes:
                                counter += 1
                        elif single_date.strftime("%A") == "Saturday":
                            if horario.sabado:
                                counter += 1
                        elif single_date.strftime("%A") == "Sunday":
                            if horario.domingo:
                                counter += 1
                        if counter == sucursal.diasPruebas:
                            vigencia = single_date      
                            subscripcionFree = SubscripcionFree(cliente=cliente,sucursal=sucursal,activa=True,fechaFin=vigencia)
                            subscripcionFree.save()
                            data['msg'] = "Paquete gratuito activado"
                            return data                
                except Horario.DoesNotExist:
                    msg = u'Sucursal sin horario disponible.'
                    data['msg'] = msg
                    return data
                    # today = str(date.today())                                           
                    # ingreso = datetime(cliente.fechaIngreso.year, cliente.fechaIngreso.month, cliente.fechaIngreso.day) 
                    # month = ingreso + timedelta(days=30)             
                    # if abs(ingreso-datetime.now()).days<=30:                    
                    #     data['mostrar'] = True
                    #     return data
                    # else:                    
                    #     data['mostrar'] = False
                    #     return data
            else:
                msg = u'Usuario no verificado'
                data['msg'] = msg
                return data                           
        except Sucursal.DoesNotExist:            
            msg = u'Sucursal no registrada'
            data['msg'] = msg
            return data        
        
        msg = u'Sucursal sin dias de prueba'
        data['msg'] = msg
        return data   

# API para registrar un celular que no exista en la agenda
# Recibe social_media y social_media_code son opcionales y solo para registro con redes sociales(FACEBOOK GOOGLE)
class RegistrarCelularSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    mensaje = serializers.CharField(allow_blank=True, read_only=True)        
    correo = serializers.CharField(max_length=100)    
    password = serializers.CharField(max_length=100)
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    celular = serializers.CharField(allow_blank=True,max_length=10)
    hombre = serializers.BooleanField(default=False)
    mujer = serializers.BooleanField(default=False)
    social_media = serializers.CharField(allow_blank=True,max_length=10)
    social_media_code = serializers.CharField(allow_blank=True,max_length=100)
    def validate(self, data):        
        correo = data.get("correo",None)
        celular = data.get("celular",None)
        password = data.get("password",None)
        nombre = data.get("nombre",None)
        apellido = data.get("apellido",None)
        hombre = data.get("hombre",None)
        mujer = data.get("mujer",None)
        social_media = data.get("social_media",None)
        social_media_code = data.get("social_media_code",None)        
        if correo is None:
            data['mensaje'] = "Ingrese un correo"
            return data
        if password is None:
            data['mensaje'] = "Ingrese un password"
            return data
        if nombre is None:
            data['mensaje'] = "Ingrese un nombre"
            return data
        if apellido is None:
            data['mensaje'] = "Ingrese un apellido"
            return data          
        try:
            user = User.objects.get(username=correo)            
        except User.DoesNotExist:
            user = False
        if user:
            try:
                cliente = Cliente.objects.get(user=user)
            except Cliente.DoesNotExist:
                cliente = False

            if cliente:
                if social_media == "FACEBOOK":
                    cliente.idFacebook = social_media_code
                    cliente.save()
                    data["success"] = True
                    data['mensaje'] = u"Log in actualizado"
                    return data
                elif social_media == "GOOGLE":
                    cliente.idGoogle = social_media_code
                    cliente.save()
                    data["success"] = True
                    data['mensaje'] = u"Log in actualizado"
                    return data    
                else:
                    data['mensaje'] = u"El usuario ya se encuentra registrado"
                    return data    
            else:
                data['mensaje'] = "Usuario sin cliente"
                return data    
            data['mensaje'] = u"Error al actualizar log in"
            return data    
            
        targetURL = "https://api.smsmasivos.com.mx/auth"
        body = {'apikey':"d40b8b72851957ad4f4382f5860027086f7a777e"}
        r = requests.post(url = targetURL, data = body)
        response = json.loads(r.text)
        token = response['token']                
        try:     
            user = User.objects.create_user(username=correo, email=correo)
            user.set_password(password)
            user.save()
        except Exception as e:
            data["mensaje"] = e.message                
            return data
        try:                                 
            if social_media == "FACEBOOK":
                cliente = Cliente(user=user,nombre=nombre,apellido=apellido,hombre=hombre,mujer=mujer,idFacebook=social_media_code)
            elif social_media == "GOOGLE":
                cliente = Cliente(user=user,nombre=nombre,apellido=apellido,hombre=hombre,mujer=mujer,idGoogle=social_media_code)            
            else:
                cliente = Cliente(user=user,nombre=nombre,apellido=apellido,hombre=hombre,mujer=mujer,telefono=celular)
            
            cliente.save()

            try:        
                if celular is None or celular == "" or celular == "...":
                    customer = conekta.Customer.create({
                        'name':cliente.nombre,
                        'email':cliente.user.email,                        
                    })   
                else:
                    customer = conekta.Customer.create({
                        'name':cliente.nombre,
                        'email':cliente.user.email,
                        'phone':celular
                    })                
                if customer:
                    if celular is None or celular == "":
                        cliente.idCustomer = customer.id
                        cliente.save()  
                        data['mensaje'] = "Usuario registrado"
                        data["success"] = True
                        return data
                    else:                        
                        targetURL = "https://api.smsmasivos.com.mx/protected/json/phones/verification/start"
                        headers = {
                            'token':token
                        }
                        body = {
                            'phone_number':celular,
                            'country_code': "52",
                        }
                        req = requests.post(url = targetURL, data = body, headers = headers)
                        response = json.loads(req.text)
                        code = response['code']
                        if code == "verification_04":
                            customer = conekta.Customer.find(customer.id)
                            customer.delete()
                            user.delete()
                            data["success"] = False
                            data["mensaje"] = response['message']                                                                     
                            return data  
                        cliente.idCustomer = customer.id
                        cliente.save()  
                        data["success"] = True
                        data["mensaje"] = response['message']                                         
                        return data                                         
                else:            
                    data["success"] = False
                    data["mensaje"] = "No se pudo crear el customer"
                    customer = conekta.Customer.find(customer.id)
                    customer.delete()
                    user.delete()
                    return data        
            except conekta.ConektaError as e:
                data["mensaje"] = e.message
                user.delete()
                return data
            except Exception as e:
                data["mensaje"] = e.message
                customer = False
                customer = conekta.Customer.find(customer.id)
                customer.delete()
                user.delete()
                return data

        except Exception as e:
            data["mensaje"] = e.message                
            user.delete()
            return data       

        data["success"] = False
        data["mensaje"] = u'Error al agregar el celular'
        return data

    
class  CheckPhoneSerializer(serializers.Serializer):        
    code = serializers.CharField(allow_blank=True, read_only=True) 
    celular = serializers.CharField(allow_blank=True,max_length=10)
    def validate(self, data):        
        celular = data.get("celular",None)

        if celular is None or celular == "" or celular == "...":            
            data["code"] = 'verification_00'
            return data

        targetURL = "https://api.smsmasivos.com.mx/auth"
        body = {'apikey':"d40b8b72851957ad4f4382f5860027086f7a777e"}
        r = requests.post(url = targetURL, data = body)
        response = json.loads(r.text)
        token = response['token']   

        targetURL = "https://api.smsmasivos.com.mx/protected/json/phones/verification/start"
        headers = {
        'token':token
        }
        body = {
        'phone_number':celular,
        'country_code':"52"
        }
        r = requests.post(url = targetURL, data = body, headers = headers)
        response = json.loads(r.text)        
        data["mensaje"] = response["message"]
        data["code"] = response["code"]

        return data

class  UpdatePhoneSerializer(serializers.Serializer):        
    success = serializers.BooleanField(read_only=True)
    mensaje = serializers.CharField(allow_blank=True, read_only=True)        
    code = serializers.CharField(allow_blank=True, read_only=True) 
    celular = serializers.CharField(max_length=10,required=True)
    idCliente = serializers.IntegerField(max_value=None, min_value=None,required=True)        
    def validate(self, data):        
        celular = data.get("celular",None)
        idCliente = data.get("idCliente",None)              

        try:
            cliente = Cliente.objects.get(id=idCliente)
        except Cliente.DoesNotExist:
            cliente = False
        
        if not cliente:
            data["mensaje"] = "Cliente no encontrado"
            data["celular"] = celular
            data["success"] = False    
            return data
            

        targetURL = "https://api.smsmasivos.com.mx/auth"
        body = {'apikey':"d40b8b72851957ad4f4382f5860027086f7a777e"}
        r = requests.post(url = targetURL, data = body)
        response = json.loads(r.text)
        token = response['token']   

        targetURL = "https://api.smsmasivos.com.mx/protected/json/phones/verification/start"
        headers = {
        'token':token
        }
        body = {
        'phone_number':celular,
        'country_code':"52"
        }
        r = requests.post(url = targetURL, data = body, headers = headers)
        response = json.loads(r.text)        
        data["mensaje"] = response["message"]
        code = response["code"]
        # code = "verification_01"
        data["code"] = response["code"]

        if code == "verification_04":
            data["success"] = False
            data["celular"] = celular
            return data    
        cliente.telefono = celular
        cliente.save()
        if code == "verification_01" or code == "verification_03":
            data["success"] = True
            data["celular"] = celular
            return data    
        else: 
            data["success"] = False
            data["celular"] = celular
            return data    
        

class  VerifyPhoneSerializer(serializers.Serializer):  
    success = serializers.BooleanField(read_only=True)    
    mensaje = serializers.CharField(allow_blank=True, read_only=True)          
    code = serializers.CharField(allow_blank=True, read_only=True) 
    sms_code = serializers.CharField(max_length=100,required=True)
    celular = serializers.CharField(max_length=10,required=True)
    def validate(self, data):        
        celular = data.get("celular",None)
        sms_code = data.get("sms_code",None)
        
        targetURL = "https://api.smsmasivos.com.mx/auth"
        body = {'apikey':"d40b8b72851957ad4f4382f5860027086f7a777e"}
        r = requests.post(url = targetURL, data = body)
        response = json.loads(r.text)
        token = response['token']   

        targetURL = "https://api.smsmasivos.com.mx/protected/json/phones/verification/check"
        headers = {
        'token':token
        }
        body = {
        'phone_number':celular,
        'verification_code':sms_code
        }
        r = requests.post(url = targetURL, data = body, headers = headers)
        response = json.loads(r.text)   
        code = response["code"]        
        data["code"] = code
        data["mensaje"] = response["message"]
        if code == "validation_01":
            data["success"] = True
            return data
        else:
            data["success"] = False
            return data 

class GetSubscriptionsSerializer(serializers.Serializer):        
    mensaje = serializers.CharField(allow_blank=True, read_only=True) 
    idCliente = serializers.IntegerField(max_value=None, min_value=None,required=True)
    subscripciones = serializers.JSONField(read_only=True)
    sesiones = serializers.JSONField(read_only=True)
    subscripcionesGratis = serializers.JSONField(read_only=True)      
    def validate(self, data):        
        idCliente = data.get("idCliente",None)
        results = {}              
        subscripcionesList = []
        sesionesList = []
        subscripcionesGratisList = []    
        try:
            cliente = Cliente.objects.get(id=idCliente)
        except Cliente.DoesNotExist:
            cliente = False
        if cliente:
            # Obtener subscripciones
            subscripciones = Subscripcion.objects.filter(cliente=idCliente,activa=True,sucursal__activa=True,sucursal__club__activado=True)            
            for subscripcion in subscripciones:
                if subscripcion.fechaRenovacion>=date.today():
                    if subscripcion.sucursal.numInt is None or subscripcion.sucursal.numInt == "None":
                        direccion = subscripcion.sucursal.calle + ' ' + subscripcion.sucursal.numExt + ' ' + subscripcion.sucursal.colonia + ' ' + subscripcion.sucursal.cp
                    else:
                        direccion = direccion = subscripcion.sucursal.calle + ' ' + subscripcion.sucursal.numInt + ' ' + subscripcion.sucursal.colonia + ' ' + subscripcion.sucursal.cp
                    
                    s = {
                        'id':subscripcion.id,
                        'cliente':subscripcion.cliente.id,
                        'sucursal':subscripcion.sucursal.id,   
                        'sucursalNombre':subscripcion.sucursal.nombre,
                        'sucursalTelefono':subscripcion.sucursal.telefono,     
                        'sucursalLatitud':subscripcion.sucursal.latitud,               
                        'sucursalLongitud':subscripcion.sucursal.longitud,
                        'sucursalCorreo':subscripcion.sucursal.correo,       
                        'sucursalDireccion':direccion,
                        'fechaSubscripcion':subscripcion.fechaSubscripcion,
                        'fechaRenovacion':subscripcion.fechaRenovacion,
                        'direccion':subscripcion.direccion,
                        'activa':subscripcion.activa,
                        'totalCobrar':subscripcion.totalCobrar,
                        'totalGym':subscripcion.totalGym
                    }
                    subscripcionesList.append(s)
            sesiones = Sesion.objects.filter(cliente=idCliente,activo=True,sucursal__activa=True,sucursal__club__activado=True)            
            for sesion in sesiones:
                if sesion.sesionesRestantes>0 and sesion.caducidad>=date.today():
                    if sesion.sucursal.numInt is None or sesion.sucursal.numInt == "None":
                        direccion = sesion.sucursal.calle + ' ' + sesion.sucursal.numExt + ' ' + sesion.sucursal.colonia + ' ' + sesion.sucursal.cp
                    else:
                        direccion = sesion.sucursal.calle + ' ' + sesion.sucursal.numInt + ' ' + sesion.sucursal.colonia + ' ' + sesion.sucursal.cp
                    
                    s = {
                        'id':sesion.id,
                        'cliente':sesion.cliente.id,
                        'sucursal':sesion.sucursal.id,
                        'sucursalNombre':sesion.sucursal.nombre,
                        'sucursalTelefono':sesion.sucursal.telefono,     
                        'sucursalLatitud':sesion.sucursal.latitud,               
                        'sucursalLongitud':sesion.sucursal.longitud,
                        'sucursalCorreo':sesion.sucursal.correo,
                        'sucursalDireccion':direccion,          
                        'total':sesion.total,
                        'sesiones':sesion.sesiones,
                        'sesionesRestantes':sesion.sesionesRestantes,
                        'caducidad':sesion.caducidad,
                        'activo':sesion.activo
                    }
                    sesionesList.append(s)
            subscripcionesGratis = SubscripcionFree.objects.filter(cliente=idCliente,activa=True,sucursal__activa=True,sucursal__club__activado=True)            
            for subscripcionGratis in subscripcionesGratis:
                if subscripcionGratis.fechaFin>=date.today():
                
                    if subscripcionGratis.sucursal.numInt is None or subscripcionGratis.sucursal.numInt == "None":
                        direccion = subscripcionGratis.sucursal.calle + ' ' + subscripcionGratis.sucursal.numExt + ' ' + subscripcionGratis.sucursal.colonia + ' ' + subscripcionGratis.sucursal.cp
                    else:
                        direccion = subscripcionGratis.sucursal.calle + ' ' + subscripcionGratis.sucursal.numInt + ' ' + subscripcionGratis.sucursal.colonia + ' ' + subscripcionGratis.sucursal.cp
                        
                    s = {
                        'id':subscripcionGratis.id,
                        'cliente':subscripcionGratis.cliente.id,
                        'sucursal':subscripcionGratis.sucursal.id,
                        'sucursalNombre':subscripcionGratis.sucursal.nombre,
                        'sucursalTelefono':subscripcionGratis.sucursal.telefono,     
                        'sucursalLatitud':subscripcionGratis.sucursal.latitud,               
                        'sucursalLongitud':subscripcionGratis.sucursal.longitud,
                        'sucursalCorreo':subscripcionGratis.sucursal.correo,
                        'sucursalDireccion':direccion,          
                        'fechaSubscripcion':subscripcionGratis.fechaSubscripcion,
                        'fechaFin':subscripcionGratis.fechaFin,
                        'direccion':subscripcionGratis.direccion,
                        'activa':subscripcionGratis.activa
                    }
                    subscripcionesGratisList.append(s)
                
            data['subscripciones'] = subscripcionesList
            data['sesiones'] = sesionesList
            data['subscripcionesGratis'] = subscripcionesGratisList
            data['mensaje'] = cliente.nombre
            return data
        else:
            data['mensaje'] = "El cliente no se encuentra registrado"
            return data