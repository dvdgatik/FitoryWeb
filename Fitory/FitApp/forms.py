from django import forms
from django.forms import ModelForm, Textarea,SelectDateWidget
from image_cropping import ImageCropWidget,ImageRatioField
from .models import Estado, Ciudad, Servicio, Actividad, Club, ServicioClub, ActividadClub, ActividadHorario, Sucursal, Foto, EvaluacionSucursal, Cliente, EvaluacionCliente, Favorito, Horario, RegistroHorario, Sesion, Subscripcion, Visita, PagoSucursal, Usuario

class cropFotoClub(forms.ModelForm):
    class Meta:
        model = Club
        fields = {'foto','fotocrop'}
        widgets = {
            'foto': ImageCropWidget,'fotocrop':ImageRatioField('foto','200x200'),
        }

class cropLogoSucursal(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = {'logo','logocrop'}
        widgets = {
            'logo': ImageCropWidget,'logocrop':ImageRatioField('logo','200x200'),
        }

class cropFotoCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = {'foto','fotocrop'}
        widgets = {
            'foto': ImageCropWidget,'fotocrop':ImageRatioField('foto','200x200'),
        }