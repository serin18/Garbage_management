# Generated by Django 5.0.4 on 2024-04-14 13:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_work", "0028_alter_requesttable_request"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requesttable",
            name="user",
            field=models.ForeignKey(
                default=20,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="R_request",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
