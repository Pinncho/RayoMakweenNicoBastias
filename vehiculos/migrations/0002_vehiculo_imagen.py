# Generated by Django 4.1.4 on 2023-06-02 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculo',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes', verbose_name='Imagen'),
        ),
    ]
