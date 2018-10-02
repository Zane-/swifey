# Generated by Django 2.1 on 2018-10-01 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('seller_status', models.BooleanField(default=True)),
                ('email', models.CharField(max_length=30)),
                ('university', models.CharField(max_length=100)),
            ],
        ),
    ]
