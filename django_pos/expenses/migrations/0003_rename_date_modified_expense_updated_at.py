# Generated by Django 5.2.3 on 2025-06-28 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_rename_date_added_expense_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='date_modified',
            new_name='updated_at',
        ),
    ]
