# Generated by Django 5.0.7 on 2024-08-01 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0015_rename_modify_date_post_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='updated_at',
        ),
    ]
