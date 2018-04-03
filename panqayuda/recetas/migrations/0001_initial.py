# Generated by Django 2.0.3 on 2018-03-22 17:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('materiales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, null=True)),
                ('cantidad', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1, 'Debes seleccionar un número entero mayor a 0.')])),
                ('duration', models.DurationField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='RecetaInventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1, 'Debes seleccionar un número entero mator a 0.')])),
                ('ocupados', models.IntegerField(blank=True, default=0)),
                ('fecha_cad', models.DateTimeField(blank=True, null=True)),
                ('estatus', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recetas.Receta')),
            ],
        ),
        migrations.CreateModel(
            name='RelacionRecetaMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=5, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(1e-06, 'Debes seleccionar una cantidad mayor a 0.')])),
                ('status', models.IntegerField(default=1)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiales.Material')),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recetas.Receta')),
            ],
        ),
        migrations.AddField(
            model_name='receta',
            name='material',
            field=models.ManyToManyField(through='recetas.RelacionRecetaMaterial', to='materiales.Material'),
        ),
    ]