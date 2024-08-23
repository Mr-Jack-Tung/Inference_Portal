# Generated by Django 5.1 on 2024-08-23 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0003_alter_apikey_integrated_address_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paymenthistory",
            name="payment_id",
        ),
        migrations.AddField(
            model_name="paymenthistory",
            name="country",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="paymenthistory",
            name="currency",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="paymenthistory",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="paymenthistory",
            name="payment_intent",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="paymenthistory",
            name="payment_method_type",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="paymenthistory",
            name="payment_status",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name="paymenthistory",
            name="stripe_payment_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="paymenthistory",
            name="type",
            field=models.PositiveSmallIntegerField(
                choices=[(1, "Stripe"), (2, "XMR")], default=1
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="paymenthistory",
            name="user_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="paymenthistory",
            name="xmr_payment_id",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="paymenthistory",
            name="crypto",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="server.crypto",
            ),
        ),
        migrations.AlterField(
            model_name="paymenthistory",
            name="integrated_address",
            field=models.CharField(blank=True, max_length=106, null=True),
        ),
        migrations.AlterField(
            model_name="paymenthistory",
            name="locked",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="paymenthistory",
            name="transaction_hash",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
