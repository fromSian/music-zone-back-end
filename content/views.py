from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from .models import Artist, Album, Song, Playlist, PlayRecord
from .serializers import (
    ArtistSerializer,
    ArtistWithAlbumSerializer,
    AlbumWriteSerializer,
    AlbumReadSerializer,
    AlbumWithSongReadSerializer,
    SongWriteSerializer,
    SongReadSerializer,
    PlaylistSerializer,
    PlayRecordSerializer,
    SongSearchSerializer,
    AlbumSearchSerializer,
    PlaylistSearchSerializer,
)
from .filter import PlayRecordFilter
from rest_framework import status
import re
from django.db.models import Q

# Create your views here.


class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArtistWithAlbumSerializer
        else:
            return ArtistSerializer


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AlbumWithSongReadSerializer
        elif self.action == "list":
            return AlbumReadSerializer
        else:
            return AlbumWriteSerializer


class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return SongReadSerializer
        else:
            return SongWriteSerializer


class PlaylistViewSet(ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    @action(detail=True, methods=["get"])
    def query_songs(self, request, pk):
        playlist = self.get_object()

        songs_queryset = playlist.songs.get_queryset().order_by("id")

        page = self.paginate_queryset(queryset=songs_queryset)

        if page is not None:
            serializer = SongReadSerializer(
                page, many=True, context={"request": request}
            )

            return self.get_paginated_response(serializer.data)

        serializer = SongReadSerializer(
            songs_queryset, many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def add_song(self, request, pk):
        song_id = request.data.get("song")
        playlist = self.get_object()
        try:
            playlist.songs.add(song_id)
            return Response("success", status=status.HTTP_200_OK)
        except Exception:
            return Response("failed", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def remove_song(self, request, pk):
        song_id = request.data.get("song")
        playlist = self.get_object()
        try:
            playlist.songs.remove(song_id)
            return Response("success", status=status.HTTP_200_OK)
        except Exception:
            return Response("failed", status=status.HTTP_400_BAD_REQUEST)


def add_count(target_id, type):
    obj = None
    if PlayRecord.objects.filter(target_id=target_id).exists():
        obj = PlayRecord.objects.get(target_id=target_id)
        obj.count = obj.count + 1
        obj.save()
    else:
        obj = PlayRecord.objects.create(target_id=target_id, type=type, count=1)
    return obj


class PlayRecordViewSet(ListModelMixin, GenericViewSet):
    queryset = PlayRecord.objects.all()
    serializer_class = PlayRecordSerializer
    filterset_class = PlayRecordFilter

    @action(detail=False, methods=["post"])
    def add(self, request):
        serializer = self.get_serializer(data=request.data)
        target_id = request.data.get("target_id")
        type = request.data.get("type")
        if serializer.is_valid():
            obj = add_count(target_id, type)
            read = PlayRecordSerializer(obj)
            return Response(read.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        top = request.query_params.get("top")
        order = request.query_params.get("order", "")
        queryset = self.filter_queryset(self.get_queryset())

        order_list = order.split(",")

        re_compile = re.compile("[-,+]")
        for o in order_list:
            o = o.strip()
            _o = re_compile.sub("", o)
            if _o not in [field.name for field in PlayRecord._meta.get_fields()]:
                order_list.remove(o)

        if len(order_list):
            queryset = queryset.order_by(", ".join(order_list))[:top]
        else:
            queryset = queryset[:top]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@api_view(http_method_names=["GET"])
def get_love_playlist(request):
    playlist = Playlist.objects.all().first()
    if playlist:
        serialzer = PlaylistSerializer(playlist)
        return Response(serialzer.data, status=status.HTTP_200_OK)
    else:
        return Response(False, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["POST"])
def search(request):
    keyword = request.data.get("keyword")
    songs = Song.objects.filter(
        Q(name__icontains=keyword) | Q(description__icontains=keyword)
    )
    songs_serializer = SongSearchSerializer(songs, many=True)

    albums = Album.objects.filter(
        Q(name__icontains=keyword) | Q(description__icontains=keyword)
    )
    albums_serializer = AlbumSearchSerializer(albums, many=True)

    playlists = Playlist.objects.filter(
        Q(name__icontains=keyword) | Q(description__icontains=keyword)
    )
    playlists_serializer = PlaylistSearchSerializer(playlists, many=True)

    return Response(
        {
            "total": len(songs_serializer.data)
            + len(albums_serializer.data)
            + len(playlists_serializer.data),
            "songs": songs_serializer.data,
            "albums": albums_serializer.data,
            "playlists": playlists_serializer.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(http_method_names=["POST"])
def clear(request):
    Playlist.objects.all().delete()
    Song.objects.all().delete()
    Album.objects.all().delete()
    Artist.objects.all().delete()
    return Response("success")
