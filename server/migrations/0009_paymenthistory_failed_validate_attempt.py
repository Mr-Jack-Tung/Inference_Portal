# Generated by Django 5.1 on 2024-08-25 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0008_paymenthistory_extra_data_paymenthistory_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymenthistory",
            name="failed_validate_attempt",
            field=models.SmallIntegerField(default=0),
        ),
    ]
