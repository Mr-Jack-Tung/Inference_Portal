# Generated by Django 5.1 on 2024-08-28 02:06

import django.db.models.deletion
import pgvector.django.vector
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0017_delete_embeddingdatasetrecord"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmbeddingDatasetRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("system_prompt", models.TextField()),
                ("prompt", models.TextField(blank=True, max_length=128000, null=True)),
                (
                    "response",
                    models.TextField(blank=True, max_length=128000, null=True),
                ),
                ("evaluation", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "embedding",
                    pgvector.django.vector.VectorField(
                        blank=True, dimensions=384, null=True
                    ),
                ),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="server.dataset"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]