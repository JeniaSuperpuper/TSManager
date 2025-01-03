# Generated by Django 5.1.1 on 2024-11-14 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('create', models.DateField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('AC', 'Active'), ('AR', 'Archive')], default='AC', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('GR', 'Grooming'), ('IP', 'In Progress'), ('DV', 'Dev'), ('DN', 'Done')], default='GR', max_length=2)),
                ('priority', models.CharField(choices=[('LW', 'Low'), ('AR', 'Average'), ('HG', 'High')], default='LW', max_length=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('term', models.DateField()),
                ('responsible_for_test', models.CharField(max_length=100)),
            ],
        ),
    ]
