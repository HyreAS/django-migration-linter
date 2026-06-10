from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_empty_operations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="testmodel",
            name="description",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
