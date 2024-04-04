from django.db import models
import uuid
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.

"""max_upload_size:
2.5MB - 2621440
5MB - 5242880
10MB - 10485760
20MB - 20971520
50MB - 52428800
100MB 104857600
250MB - 214958080
500MB - 429916160
"""


def validate_image_size(file):
    max_upload_size = 2621440
    if file.size > max_upload_size:
        raise ValidationError(
            _("%(value)s is larger than 2.5MB"),
            params={"value": file},
        )


def validate_image_content_type(file):
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
        validators=[validate_image_content_type, validate_image_size],
    )

    def __str__(self):
        return self.name


class Album(models.Model):
    id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, primary_key=True
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    name = models.CharField(
        verbose_name="专辑名称",
        max_length=255,
        blank=False,
        db_index=True,
        validators=[],
    )
    image = models.FileField(
        upload_to="album/%Y/%m/%d",
        max_length=100,
        blank=True,
        null=True,
        validators=[validate_image_content_type, validate_image_size],
    )
    # an album can be associated with many artists, and an artist can have many albums
    artist = models.ManyToManyField(Artist, related_name="album_artist")

    def __str__(self):
        return self.name


def validate_song_content_type(file):
    content_types = [
        "audio/x-m4a",
        "audio/mp3",
        "audio/mp4",
        "audio/flac",
        "audio/wav",
        "audio/webm",
        "audio/ogg",
        "audio/flac",
    ]
    if file.content_type not in content_types:
        raise ValidationError(
            _("%(value)s is not the valid type"),
            params={"value": file.content_type},
        )


def validate_song_size(file):
    max_upload_size = 52428800
    print(file.size)
    if file.size > max_upload_size:
        raise ValidationError(
            _("%(value)s is larger than 50MB"),
            params={"value": file},
        )


class Song(models.Model):
    id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, primary_key=True
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    name = models.CharField(
        verbose_name="歌曲名称",
        max_length=255,
        blank=False,
        db_index=True,
    )
    audio = models.FileField(
        upload_to="songs/%Y/%m/%d",
        verbose_name="音频",
        blank=False,
        null=False,
        validators=[validate_song_content_type, validate_song_size],
    )
    # an album can have many songs, but a song only can be associated with on album
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist = models.ManyToManyField(Artist, related_name="song_artist")
    track = models.PositiveIntegerField(blank=False, verbose_name="曲序")

    def __str__(self):
        return self.name


class Playlist(models.Model):
    id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, primary_key=True
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    name = models.CharField(
        verbose_name="歌单名称",
        max_length=255,
        blank=False,
        db_index=True,
        validators=[],
    )
    image = models.FileField(
        upload_to="album/%Y/%m/%d",
        max_length=100,
        blank=True,
        null=True,
        validators=[validate_image_content_type, validate_image_size],
    )
    songs = models.ManyToManyField(Song, related_name="playlist_song")

    def __str__(self):
        return self.name


class PlayRecord(models.Model):
    id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, primary_key=True
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    TYPE_CHOICES = [
        ("PLAYLIST", "Playlist"),
        ("ALBUM", "Album"),
        ("SONG", "Song"),
        ("ARTIST", "Artist"),
    ]
    type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, blank=False, verbose_name="播放内容类型"
    )
    target_id = models.UUIDField(blank=False, verbose_name="播放内容id")

    count = models.PositiveIntegerField(blank=False, verbose_name="播放次数", default=1)

    def __str__(self):
        return self.name


# recevie sender
@receiver(post_delete, sender=Artist)
def delete_nouse_record(sender, instance, **kwargs):
    playRecords = PlayRecord.objects.filter(target_id=instance.id)
    playRecords.delete()
