# Generated by Django 5.2.3 on 2025-07-06 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_scope_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Раздел', 'verbose_name_plural': 'Разделы'},
        ),
    ]
