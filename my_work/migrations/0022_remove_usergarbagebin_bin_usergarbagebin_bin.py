# Generated by Django 5.0 on 2024-04-01 09:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_work', '0021_usergarbagebin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergarbagebin',
            name='bin',
        ),
        migrations.AddField(
            model_name='usergarbagebin',
            name='bin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='my_work.garbagebin'),
        ),
    ]
