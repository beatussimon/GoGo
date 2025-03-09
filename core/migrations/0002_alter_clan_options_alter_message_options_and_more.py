# Generated by Django 5.1.2 on 2025-03-09 22:03

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clan',
            options={'ordering': ['name'], 'verbose_name': 'Clan', 'verbose_name_plural': 'Clans'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created_at'], 'verbose_name': 'Notification', 'verbose_name_plural': 'Notifications'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at'], 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AlterModelOptions(
            name='trip',
            options={'ordering': ['-departure'], 'verbose_name': 'Trip', 'verbose_name_plural': 'Trips'},
        ),
        migrations.AlterModelOptions(
            name='triprating',
            options={'ordering': ['-id'], 'verbose_name': 'Trip Rating', 'verbose_name_plural': 'Trip Ratings'},
        ),
        migrations.AlterModelOptions(
            name='triprequest',
            options={'ordering': ['-preferred_date'], 'verbose_name': 'Trip Request', 'verbose_name_plural': 'Trip Requests'},
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'ordering': ['reg_number'], 'verbose_name': 'Vehicle', 'verbose_name_plural': 'Vehicles'},
        ),
        migrations.AlterModelOptions(
            name='verificationrequest',
            options={'ordering': ['-submitted_at'], 'verbose_name': 'Verification Request', 'verbose_name_plural': 'Verification Requests'},
        ),
        migrations.RemoveField(
            model_name='trip',
            name='exotic_items',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='start_coords',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='waypoints',
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])]),
        ),
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='post_videos/', validators=[django.core.validators.FileExtensionValidator(['mp4', 'mov', 'avi'])]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_pics/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])]),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['read'], name='core_notifi_read_bfd411_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['status'], name='core_trip_status_41c948_idx'),
        ),
        migrations.AddIndex(
            model_name='triprequest',
            index=models.Index(fields=['status'], name='core_tripre_status_dfba42_idx'),
        ),
        migrations.AddIndex(
            model_name='verificationrequest',
            index=models.Index(fields=['status'], name='core_verifi_status_610efc_idx'),
        ),
    ]
