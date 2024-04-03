from django.db import models
import uuid
from django.utils import timezone

# Create your models here.


class Artist(models.Model):
    id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, primary_key=True
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    name = models.CharField(
        verbose_name="艺人名称", max_length=255, blank=False, db_index=True
    )
