# Generated by Django 2.0.2 on 2018-03-02 03:23

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
                ('cantidad', models.IntegerField()),
                ('duration', models.DurationField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='RelacionRecetaMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField()),
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
