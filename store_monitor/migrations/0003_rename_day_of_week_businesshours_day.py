# Generated by Django 4.2.7 on 2023-11-13 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store_monitor", "0002_remove_storereport_timestamp_utc_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="businesshours",
            old_name="day_of_week",
            new_name="day",
        ),
    ]
