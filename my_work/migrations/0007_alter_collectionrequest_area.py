# Generated by Django 5.0 on 2024-03-19 06:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_work', '0006_alter_collectionrequest_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionrequest',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_work.area'),
        ),
    ]
