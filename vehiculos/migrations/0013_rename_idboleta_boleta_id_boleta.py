# Generated by Django 4.1.7 on 2023-06-25 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculos', '0012_detalle_boleta_id_boleta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boleta',
            old_name='idBoleta',
            new_name='id_boleta',
        ),
    ]
