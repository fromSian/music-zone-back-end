from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("artists", views.ArtistViewSet, basename="artists")

router.register("albums", views.AlbumViewSet, basename="albums")


router.register("songs", views.SongViewSet, basename="songs")


urlpatterns = []
urlpatterns = urlpatterns + router.urls
