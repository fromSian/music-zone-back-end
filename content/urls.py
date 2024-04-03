from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("artists", views.ArtistViewSet, basename="artists")

router.register("albums", views.AlbumViewSet, basename="albums")


router.register("songs", views.SongViewSet, basename="songs")


router.register("playlists", views.PlaylistViewSet, basename="playlists")

urlpatterns = []
urlpatterns = urlpatterns + router.urls
