# Generated by Django 3.0.8 on 2020-07-29 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0003_auto_20200729_0756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='development_db',
            old_name='developmentband_settings',
            new_name='developmentBandSettings',
        ),
    ]