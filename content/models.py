from django.db import models
import uuid
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# Create your models here.

"""max_upload_size:
2.5MB - 2621440
5MB - 5242880
10MB - 10485760
20MB - 20971520
50MB - 5242880
100MB 104857600
250MB - 214958080
500MB - 429916160
"""


def validate_artist_image_size(file):
    max_upload_size = 2621440
    if file.size > max_upload_size:
        raise ValidationError(
            _("%(value)s is larger than 2.5MB"),
            params={"value": file},
        )


def validate_artist_image_content_type(file):
    content_types = [
        "image/jpg",
        "image/jpeg",
        "image/gif",
        "image/png",
        "image/svg+xml",
    ]
    if file.content_type not in content_types:
        raise ValidationError(
            _("%(value)s is not the valid type"),
            params={"value": file.content_type},
        )


class Artist(models.Model):
    id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, primary_key=True
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    name = models.CharField(
        verbose_name="艺人名称",
        max_length=255,
        blank=False,
        db_index=True,
        validators=[],
    )
    image = models.FileField(
        upload_to="artist/%Y/%m/%d",
        max_length=100,
        blank=True,
        null=True,
        validators=[validate_artist_image_content_type, validate_artist_image_size],
    )
