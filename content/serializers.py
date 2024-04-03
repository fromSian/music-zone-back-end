from rest_framework import serializers
from .models import Artist, Album, Artist, Song


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


class AlbumReadSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(many=True)
    songs = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = "__all__"

    def get_songs(self, obj):
        songs = Song.objects.filter(album=obj)
        serializer = SongReadSerializer(songs, many=True)
        return serializer.data


class AlbumForSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        # fields = "__all__"
        exclude = ("artist",)


class SongReadSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(many=True)
    album = AlbumForSongSerializer()

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
