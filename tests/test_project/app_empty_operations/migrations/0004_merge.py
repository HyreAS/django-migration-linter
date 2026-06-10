from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app_empty_operations", "0002_branch_a"),
        ("app_empty_operations", "0003_branch_b"),
    ]

    operations = []
