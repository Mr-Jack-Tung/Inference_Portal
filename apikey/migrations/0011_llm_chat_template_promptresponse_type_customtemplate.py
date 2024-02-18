# Generated by Django 5.0.1 on 2024-02-17 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apikey', '0010_promptresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='llm',
            name='chat_template',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='promptresponse',
            name='type',
            field=models.TextField(default='prompt'),
        ),
        migrations.CreateModel(
            name='CustomTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name', models.CharField(max_length=300)),
                ('template', models.TextField(default='')),
                ('model', models.ManyToManyField(to='apikey.llm')),
            ],
        ),
    ]