# Generated by Django 4.2.7 on 2023-11-13 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store_monitor", "0003_rename_day_of_week_businesshours_day"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="storereport",
            name="downtime_last_day",
        ),
        migrations.RemoveField(
            model_name="storereport",
            name="downtime_last_hour",
        ),
        migrations.RemoveField(
            model_name="storereport",
            name="downtime_last_week",
        ),
        migrations.RemoveField(
            model_name="storereport",
            name="store_id",
        ),
        migrations.RemoveField(
            model_name="storereport",
            name="uptime_last_day",
        ),
        migrations.RemoveField(
            model_name="storereport",
            name="uptime_last_hour",
        ),
        migrations.RemoveField(
            model_name="storereport",
            name="uptime_last_week",
        ),
        migrations.AddField(
            model_name="storereport",
            name="data",
            field=models.JSONField(default=[]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="storereport",
            name="report_id",
            field=models.CharField(max_length=10, unique=True),
        ),
    ]