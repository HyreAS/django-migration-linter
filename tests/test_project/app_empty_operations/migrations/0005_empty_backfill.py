from __future__ import annotations

from django.db import migrations


def backfill_slug(apps, schema_editor):
    TestModel = apps.get_model("app_empty_operations", "TestModel")
    for obj in TestModel.objects.filter(slug__isnull=True):
        obj.slug = "default"
        obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ("app_empty_operations", "0004_merge"),
    ]

    # BAD: the backfill function was never added to operations
    operations = []
