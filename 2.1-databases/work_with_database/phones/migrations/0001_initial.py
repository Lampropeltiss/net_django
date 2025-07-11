# Generated by Django 5.2.3 on 2025-06-11 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField(null=True)),
                ('image', models.CharField(null=True)),
                ('release_date', models.DateField(null=True)),
                ('lte_exists', models.BooleanField(null=True)),
                ('slug', models.SlugField()),
            ],
        ),
    ]
