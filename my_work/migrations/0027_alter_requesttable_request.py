# Generated by Django 5.0 on 2024-04-04 11:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_work', '0026_remove_collectionrequest_public_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requesttable',
            name='request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R_name', to='my_work.collectionrequest'),
        ),
    ]
