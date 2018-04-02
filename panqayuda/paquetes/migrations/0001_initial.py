import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recetas', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=70)),
                ('precio', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05, 'El precio del paquete debe ser mayor a 0.')])),
                ('estatus', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaqueteInventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Debes seleccionar un número entero mayor a 0.')])),
                ('fecha_cad', models.DateTimeField(blank=True, null=True)),
                ('estatus', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paquetes.Paquete')),
            ],
        ),
        migrations.CreateModel(
            name='RecetasPorPaquete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Debes seleccionar un número entero mayor a 0.')])),
                ('estatus', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paquetes.Paquete')),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recetas.Receta')),
            ],
        ),
        migrations.AddField(
            model_name='paquete',
            name='recetas',
            field=models.ManyToManyField(through='paquetes.RecetasPorPaquete', to='recetas.Receta'),
        ),
    ]
