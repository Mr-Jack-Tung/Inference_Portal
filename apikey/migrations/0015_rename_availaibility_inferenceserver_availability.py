# Generated by Django 5.0.1 on 2024-02-20 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apikey', '0014_rename_availibility_inferenceserver_availaibility'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inferenceserver',
            old_name='availaibility',
            new_name='availability',
        ),
    ]
