# Generated by Django 4.2.16 on 2025-04-22 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvedrequest',
            name='parking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parking', to='parking.parking'),
        ),
    ]
