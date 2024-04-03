# Generated by Django 5.0.3 on 2024-04-03 12:08

import content.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_album_song'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='audio',
            field=models.FileField(default=django.utils.timezone.now, upload_to='', validators=[content.models.validate_image_content_type, content.models.validate_image_size], verbose_name='音频'),
            preserve_default=False,
        ),
    ]
