# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-07-19 15:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import image_cropping.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='...', max_length=100)),
                ('icono', models.ImageField(default='default/actividad.jpg', upload_to='actividades/')),
            ],
        ),
        migrations.CreateModel(
            name='ActividadClub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Actividad')),
            ],
        ),
        migrations.CreateModel(
            name='ActividadHorario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horaInicio', models.TimeField(blank=True, default=None, null=True)),
                ('horaFin', models.TimeField(blank=True, default=None, null=True)),
                ('lunes', models.BooleanField(default=False)),
                ('martes', models.BooleanField(default=False)),
                ('miercoles', models.BooleanField(default=False)),
                ('jueves', models.BooleanField(default=False)),
                ('viernes', models.BooleanField(default=False)),
                ('sabado', models.BooleanField(default=False)),
                ('domingo', models.BooleanField(default=False)),
                ('actividadClub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.ActividadClub')),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='...', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='...', max_length=100)),
                ('apellido', models.CharField(default='...', max_length=100)),
                ('telefono', models.CharField(default='...', max_length=100)),
                ('hombre', models.BooleanField(default=False)),
                ('mujer', models.BooleanField(default=False)),
                ('fechaIngreso', models.DateField(auto_now_add=True, verbose_name='Fecha')),
                ('salud', models.BooleanField(default=False)),
                ('convivir', models.BooleanField(default=False)),
                ('vermeBien', models.BooleanField(default=False)),
                ('diversion', models.BooleanField(default=False)),
                ('ubicacion', models.BooleanField(default=False)),
                ('bluetooth', models.BooleanField(default=False)),
                ('idFacebook', models.CharField(default='...', max_length=100)),
                ('idGoogle', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('idCustomer', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('playerID', models.CharField(blank=True, default=None, max_length=900, null=True)),
                ('foto', models.ImageField(default='default/perfil.png', upload_to='clientes/')),
                ('fotocrop', image_cropping.fields.ImageRatioField('foto', '200x200', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='fotocrop')),
                ('cropURL', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('ciudad', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='FitApp.Ciudad')),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='...', max_length=100)),
                ('fechaIncorporacion', models.DateField(auto_now_add=True, verbose_name='Fecha')),
                ('RFC', models.CharField(default='...', max_length=100)),
                ('banco', models.CharField(default='...', max_length=100)),
                ('tarjetahabiente', models.CharField(default='...', max_length=100)),
                ('numCuenta', models.CharField(default='...', max_length=100)),
                ('paginaWeb', models.CharField(default='...', max_length=100)),
                ('facebook', models.CharField(default='...', max_length=100)),
                ('instagram', models.CharField(default='...', max_length=100)),
                ('twitter', models.CharField(default='...', max_length=100)),
                ('evaluacionPromedio', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('activado', models.BooleanField(default=False)),
                ('codigoClub', models.CharField(default='...', max_length=100)),
                ('codigoRepresentante', models.CharField(default='...', max_length=100)),
                ('direccion', models.CharField(default='...', max_length=100)),
                ('telefono', models.CharField(default='...', max_length=100)),
                ('correo', models.CharField(default='...', max_length=100)),
                ('foto', models.ImageField(default='default/club.png', upload_to='clubes/')),
                ('fotocrop', image_cropping.fields.ImageRatioField('foto', '200x200', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='fotocrop')),
                ('Legal', models.BooleanField(default=False)),
                ('fechaLegal', models.DateField(blank=True, default=None, null=True, verbose_name='Fecha acepto terminos')),
                ('cropURL', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='...', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluacionCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje', models.IntegerField(default=0)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluacionSucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje', models.IntegerField(default=0)),
                ('cliente', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='FitApp.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='FitApp.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.ImageField(default='default/foto.png', upload_to='fotos/')),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lunes', models.BooleanField(default=False)),
                ('martes', models.BooleanField(default=False)),
                ('miercoles', models.BooleanField(default=False)),
                ('jueves', models.BooleanField(default=False)),
                ('viernes', models.BooleanField(default=False)),
                ('sabado', models.BooleanField(default=False)),
                ('domingo', models.BooleanField(default=False)),
                ('numDias', models.IntegerField(default=0)),
                ('tipo', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncidenciaContrasena',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.EmailField(default='example@example.com', max_length=254)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('estatus', models.IntegerField(default=0)),
                ('token', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='PagoSucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagar', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('numRastreo', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('fecha', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha Pago')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroHorario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('apertura', models.TimeField(blank=True, null=True)),
                ('cierre', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='...', max_length=100)),
                ('icono', models.ImageField(default='default/servicio.png', upload_to='servicios/')),
            ],
        ),
        migrations.CreateModel(
            name='ServicioClub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('sesiones', models.IntegerField(default=0)),
                ('sesionesRestantes', models.IntegerField(default=0)),
                ('caducidad', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha')),
                ('activo', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Subscripcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalCobrar', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('totalGym', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('fechaSubscripcion', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha Subscripcion')),
                ('fechaRenovacion', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha Renovacion')),
                ('direccion', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('activa', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='SubscripcionFree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaSubscripcion', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha Subscripcion')),
                ('fechaFin', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha Fin')),
                ('direccion', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('activa', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='...', max_length=100)),
                ('descripcion', models.TextField(blank=True, max_length=1000, null=True)),
                ('correo', models.CharField(default='...', max_length=100)),
                ('telefono', models.CharField(default='...', max_length=100)),
                ('municipio', models.CharField(default='...', max_length=100)),
                ('calle', models.CharField(default='...', max_length=100)),
                ('numExt', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('numInt', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('colonia', models.CharField(default='...', max_length=100)),
                ('cp', models.CharField(default='...', max_length=100)),
                ('latitud', models.CharField(default='...', max_length=100)),
                ('longitud', models.CharField(default='...', max_length=100)),
                ('calificacion', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('ibeacon', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('maximo', models.IntegerField(default=0)),
                ('minimo', models.IntegerField(default=0)),
                ('mensualidad', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('dia', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('porcentajeCliente', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('porcentajeUser', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('activa', models.BooleanField(default=False)),
                ('logo', models.ImageField(default='default/logo.jpg', upload_to='logos/')),
                ('logocrop', image_cropping.fields.ImageRatioField('logo', '200x200', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='logocrop')),
                ('cropURL', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('tips', models.TextField(blank=True, max_length=1000, null=True)),
                ('diasPruebas', models.IntegerField(default=0)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Ciudad')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Club')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Estado')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='...', max_length=100)),
                ('activo', models.BooleanField(default=False)),
                ('Legal', models.BooleanField(default=False)),
                ('fechaLegal', models.DateField(blank=True, default=None, null=True, verbose_name='Fecha acepto terminos')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal')),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='Fecha')),
                ('hora', models.TimeField(auto_now_add=True, verbose_name='Hora')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Cliente')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal')),
            ],
        ),
        migrations.AddField(
            model_name='subscripcionfree',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal'),
        ),
        migrations.AddField(
            model_name='subscripcion',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal'),
        ),
        migrations.AddField(
            model_name='sesion',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal'),
        ),
        migrations.AddField(
            model_name='servicioclub',
            name='sucursal',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal'),
        ),
        migrations.AddField(
            model_name='registrohorario',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal'),
        ),
        migrations.AddField(
            model_name='pagosucursal',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal'),
        ),
        migrations.AddField(
            model_name='horario',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal'),
        ),
        migrations.AddField(
            model_name='foto',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal'),
        ),
        migrations.AddField(
            model_name='favorito',
            name='sucursal',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal'),
        ),
        migrations.AddField(
            model_name='evaluacionsucursal',
            name='sucursal',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='FitApp.Estado'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ciudad',
            name='estado',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='FitApp.Estado'),
        ),
        migrations.AddField(
            model_name='actividadclub',
            name='sucursal',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='FitApp.Sucursal'),
        ),
    ]
