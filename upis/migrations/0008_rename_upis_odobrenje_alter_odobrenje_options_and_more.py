# Generated by Django 5.2 on 2025-04-21 14:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("upis", "0007_merge_20250421_1415"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Upis",
            new_name="Odobrenje",
        ),
        migrations.AlterModelOptions(
            name="odobrenje",
            options={"verbose_name": "Odobrenje", "verbose_name_plural": "Odobrenja"},
        ),
        migrations.AlterField(
            model_name="korisnik",
            name="password",
            field=models.CharField(
                default="default_pass", max_length=128, verbose_name="password"
            ),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name="odobrenje",
            table="odobrenja",
        ),
    ]
