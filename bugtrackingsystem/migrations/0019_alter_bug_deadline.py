# Generated by Django 5.1 on 2024-09-20 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugtrackingsystem', '0018_alter_bug_unique_together_bug_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='deadline',
            field=models.DateField(),
        ),
    ]
