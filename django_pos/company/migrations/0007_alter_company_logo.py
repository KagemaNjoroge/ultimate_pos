# Generated by Django 5.2.3 on 2025-06-27 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_remove_branch_city_alter_branch_branch_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, default='static/default.png', null=True, upload_to='company/logos/'),
        ),
    ]
