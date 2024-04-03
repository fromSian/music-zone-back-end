from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Artist
from .serializers import ArtistSerializer

# Create your views here.


@api_view(["GET"])
def test(resquest):
    return Response("success")


class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
