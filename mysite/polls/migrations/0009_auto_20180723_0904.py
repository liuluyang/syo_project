# Generated by Django 2.0.7 on 2018-07-23 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_delete_te'),
    ]

    operations = [
        migrations.RenameField(
            model_name='img',
            old_name='tag',
            new_name='tags',
        ),
    ]