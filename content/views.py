from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Artist, Album, Song
from .serializers import (
    ArtistSerializer,
    AlbumWriteSerializer,
    AlbumReadSerializer,
    SongWriteSerializer,
    SongReadSerializer,
)

# Create your views here.


@api_view(["GET"])
def test(resquest):
    return Response("success")


class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
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
