# Generated by Django 5.2 on 2025-04-21 14:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("upis", "0008_rename_upis_odobrenje_alter_odobrenje_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="odobrenje",
            old_name="objasnjenje_odobrenja",
            new_name="objasnjenje",
        ),
        migrations.RenameField(
            model_name="odobrenje",
            old_name="vrijeme_odobrenja",
            new_name="vrijeme",
        ),
        migrations.AddField(
            model_name="odobrenje",
            name="smjer",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="student",
                to="upis.smjer",
            ),
            preserve_default=False,
        ),
    ]
