# Generated by Django 5.1.1 on 2024-11-14 16:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project'),
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.task'),
        ),
    ]
