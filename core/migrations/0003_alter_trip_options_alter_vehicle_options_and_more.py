# Generated by Django 5.1.2 on 2025-03-09 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_clan_options_alter_message_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trip',
            options={},
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={},
        ),
        migrations.RemoveIndex(
            model_name='trip',
            name='core_trip_status_41c948_idx',
        ),
    ]
