# Generated by Django 3.0.5 on 2020-05-12 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0005_auto_20200512_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleapplication_db',
            name='delta_x',
            field=models.DecimalField(decimal_places=0, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='sampleapplication_db',
            name='delta_y',
            field=models.DecimalField(decimal_places=0, max_digits=6, null=True),
        ),
    ]