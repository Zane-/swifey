# Generated by Django 2.1 on 2018-11-26 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('user_id', models.IntegerField()),
                ('authenticator', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('date_created', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=1000)),
                ('user_id', models.IntegerField()),
                ('listing_type', models.CharField(choices=[('S', 'Swipe'), ('M', 'Meal Exchange'), ('I', 'Item')], max_length=1)),
                ('num_swipes', models.IntegerField()),
                ('last_modified', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=256)),
                ('university', models.CharField(max_length=100)),
                ('has_meal_plan', models.BooleanField(default=False)),
                ('date_joined', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
