# Generated by Django 5.0.1 on 2024-05-01 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0010_remove_customtemplate_model_delete_agentinstruct_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='llm',
            old_name='price',
            new_name='input_price',
        ),
        migrations.RenameField(
            model_name='promptresponse',
            old_name='cost',
            new_name='input_cost',
        ),
        migrations.AddField(
            model_name='llm',
            name='output_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='promptresponse',
            name='number_input_tokens',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='promptresponse',
            name='number_output_tokens',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='promptresponse',
            name='output_cost',
            field=models.FloatField(default=0.0),
        ),
    ]