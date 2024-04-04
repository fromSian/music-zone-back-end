from rest_framework import serializers
from .models import Artist, Album, Artist, Song, Playlist, PlayRecord


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "create_time": {"read_only": True},
            "update_time": {"read_only": True},
        }


class AlbumWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "create_time": {"read_only": True},
            "update_time": {"read_only": True},
        }


class AlbumWithSongReadSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(many=True)
    songs = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = "__all__"

    def get_songs(self, obj):
        songs = Song.objects.filter(album=obj)
        serializer = SongReadSerializer(songs, many=True)
        return serializer.data


class AlbumReadSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(many=True)

    class Meta:
        model = Album
        fields = "__all__"
        # exclude = ("artist",)


class SongReadSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(many=True)
    album = AlbumReadSerializer()

    class Meta:
        model = Song
        fields = "__all__"


class SongWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "create_time": {"read_only": True},
            "update_time": {"read_only": True},
        }


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        exclude = ("songs",)


class PlayRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayRecord
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "count": {"read_only": True},
            "create_time": {"read_only": True},
            "update_time": {"read_only": True},
        }

    def validate_target_id(self, value):
        if (
            Artist.objects.filter(id=value).exists()
            or Album.objects.filter(id=value).exists()
            or Song.objects.filter(id=value).exists()
            or Playlist.objects.filter(id=value).exists()
        ):
            return value
        else:
            raise serializers.ValidationError("not valid target_id")
