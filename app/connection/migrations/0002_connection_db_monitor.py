# Generated by Django 3.0.3 on 2020-03-20 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
        ('connection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection_db',
            name='monitor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Monitor_Db'),
        ),
    ]