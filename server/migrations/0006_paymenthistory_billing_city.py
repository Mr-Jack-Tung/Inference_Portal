# Generated by Django 5.1 on 2024-08-23 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0005_remove_paymenthistory_country_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymenthistory",
            name="billing_city",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
