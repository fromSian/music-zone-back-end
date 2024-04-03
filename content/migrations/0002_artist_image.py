# Generated by Django 5.0.3 on 2024-04-03 09:24

import content.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='artist/%Y/%m/%d', validators=[content.models.validate_artist_image_content_type, content.models.validate_artist_image_size]),
        ),
    ]
