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


class ArtistWithAlbumSerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "create_time": {"read_only": True},
            "update_time": {"read_only": True},
        }

    def get_albums(self, obj):
        albums = Album.objects.filter(artist=obj)
        serializer = AlbumReadSerializer(albums, many=True)
        return serializer.data


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
        fields = (
            "id",
            "name",
            "duration",
            "track",
            "description",
            "artist",
            "album",
            "create_time",
            "update_time",
        )


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
    detail = serializers.SerializerMethodField()

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

    def get_detail(self, obj):
        if obj.type == "PLAYLIST":
            detail_instance = Playlist.objects.filter(id=obj.target_id).first()
            serializer_class = PlaylistSerializer
        elif obj.type == "SONG":
            detail_instance = Song.objects.filter(id=obj.target_id).first()
            serializer_class = SongReadSerializer
        elif obj.type == "ALBUM":
            detail_instance = Album.objects.filter(id=obj.target_id).first()
            serializer_class = AlbumReadSerializer
        elif obj.type == "ARTIST":
            detail_instance = Artist.objects.filter(id=obj.target_id).first()
            serializer_class = ArtistSerializer

        if detail_instance:
            serializer = serializer_class(detail_instance)
            return serializer.data
        else:
            return None
