# Generated by Django 5.1 on 2024-09-12 23:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugtrackingsystem', '0013_assignment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('deadline', models.DateField()),
                ('types', models.CharField(choices=[('Bug', 'Bug'), ('Feature', 'Feature Request')], max_length=50)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'), ('Closed', 'Closed')], max_length=50)),
                ('assigned_developers', models.ManyToManyField(related_name='bugs', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_bugs', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtrackingsystem.project')),
            ],
        ),
    ]
