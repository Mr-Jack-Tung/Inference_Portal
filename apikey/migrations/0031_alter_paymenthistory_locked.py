# Generated by Django 5.0.1 on 2024-03-24 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apikey', '0030_rename_current_block_num_paymenthistory_block_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='locked',
            field=models.BooleanField(),
        ),
    ]